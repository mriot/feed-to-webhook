import os
import yaml
import requests
from datetime import datetime, timedelta
from urllib.parse import urlparse, urlunparse
import xml.etree.ElementTree as ET


def fxify_twitter_url(link):
    parsed_url = urlparse(link)
    modified_url = parsed_url._replace(netloc="fxtwitter.com")
    fixed_url = urlunparse(modified_url)
    return fixed_url


def twitter_feed(feed):
    response = requests.get(feed["url"], headers={"User-Agent": "Hi, I am a bot!"})

    if (response.status_code != 200):
        return {"error": response.status_code}

    root = ET.fromstring(response.content.decode("utf-8"))
    items = root.findall("channel/item")

    feed_owner = root.find("channel/title").text  # username / @username
    feed_owner_accountname = feed_owner.split(" / ")[-1]  # @username
    feed_owner_link = "https://twitter.com/" + feed_owner_accountname.replace("@", "")

    # TODO
    if feed.get("last_item_date") == None:
        return {"last_item_date": items[0].find("pubDate").text}

    last_item_date = datetime.strptime(feed.get("last_item_date").replace('GMT', '+0000'), "%a, %d %b %Y %H:%M:%S %z")  # Thu, 09 Nov 2023 16:25:33 GMT

    for i, item in enumerate(items):
        if i == 3:
            break

        item_date = datetime.strptime(item.find("pubDate").text.replace('GMT', '+0000'), "%a, %d %b %Y %H:%M:%S %z")  # Thu, 09 Nov 2023 16:25:33 GMT
        if item_date < last_item_date:  # item date is older than last item date
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

    return {"last_item_date": items[0].find("pubDate").text}  # todo item 0 might not be the newest item


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

    config_file.seek(0)
    config_file.truncate()
    yaml.dump(config, config_file)

    # for rfeed in config["twitter_feeds"]:
    #     if (result.get("error")):
    #         requests.post(config["error_webhook"], {"content": f"Error {str(result['error'])} while fetching rss feed {tfeed['url']}"})
    #     else:
    #         # todo update config
    #         pass

    config_file.close()


if __name__ == "__main__":
    main()
