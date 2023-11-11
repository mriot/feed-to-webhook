import os
import yaml
import requests
from datetime import datetime, timedelta
from urllib.parse import urlparse, urlunparse
import xml.etree.ElementTree as ET


def discord_embed(feed):
    pass


def twitter_feed(feed):
    response = requests.get(feed["url"], headers={"User-Agent": "Hi, I am a bot!"})

    if (response.status_code != 200):
        return {"error": response.status_code}

    root = ET.fromstring(response.content.decode("utf-8"))
    items = root.findall("channel/item")

    feed_owner = root.find("channel/title").text  # username / @username
    feed_owner_accountname = feed_owner.split(" / ")[-1]  # @username
    feed_owner_link = "https://twitter.com/" + feed_owner_accountname.replace("@", "")

    # first run of script only gets the newest item date and returns it
    if feed.get("last_item_date") == None:
        return {"last_item_date": items[0].find("pubDate").text}

    # get last item date from config for comparison
    last_item_date = datetime.strptime(feed.get("last_item_date").replace("GMT", "+0000"), "%a, %d %b %Y %H:%M:%S %z")  # Thu, 09 Nov 2023 16:25:33 GMT

    # loop through items in feed in reverse order (older first)
    for i, item in enumerate(reversed(items[:5])):
        item_date = datetime.strptime(item.find("pubDate").text.replace("GMT", "+0000"), "%a, %d %b %Y %H:%M:%S %z")  # Thu, 09 Nov 2023 16:25:33 GMT
        # a more recent date is considered _greater_ than an older date
        if item_date <= last_item_date:
            continue

        post_author = items[i].find("dc:creator", {"dc": "http://purl.org/dc/elements/1.1/"}).text  # @username
        post_author_link = "https://twitter.com/" + post_author.replace("@", "")
        post_url = items[i].find("link").text
        is_retweet = feed_owner.find(post_author) == -1

        if is_retweet and feed["include_retweets"] == False:
            continue

        post_url = urlunparse(urlparse(post_url)._replace(netloc="fxtwitter.com"))

        if is_retweet:
            output = f"♻️ [{feed_owner_accountname}]({feed_owner_link}) retweeted [{post_author}]({post_author_link})\n{post_url}"
        else:
            output = f"📢 [{feed_owner_accountname}]({feed_owner_link}) tweeted \n{post_url}"

        for webhook in feed["webhooks"]:
            requests.post(webhook, {"content": output})

    return {"last_item_date": items[0].find("pubDate").text}  # we assume that the first item is the newest one


def rss_feed(feeds, config_file):
    pass


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_dir, "config.yaml")

    config_file = open(config_path, "r+")
    config = yaml.safe_load(config_file)

    for i, tfeed in enumerate(config["twitter_feeds"]):
        result = twitter_feed(tfeed)  # return error or last item date
        if (result.get("error")):
            requests.post(config["error_webhook"], {"content": f"Error {str(result['error'])} while fetching twitter feed {tfeed['url']}"})
        else:
            config["twitter_feeds"][i]["last_item_date"] = result["last_item_date"]

    # for rfeed in config["twitter_feeds"]:
    #     if (result.get("error")):
    #         requests.post(config["error_webhook"], {"content": f"Error {str(result['error'])} while fetching rss feed {tfeed['url']}"})
    #     else:
    #         # todo update config
    #         pass

    # todo make this nicer
    config_file.seek(0)
    config_file.truncate()
    yaml.safe_dump(config, config_file, sort_keys=False)

    config_file.close()


if __name__ == "__main__":
    main()
