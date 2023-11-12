import requests
from datetime import datetime
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, urlunparse


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
    for item in reversed(items[:5]):
        item_date = datetime.strptime(item.find("pubDate").text.replace("GMT", "+0000"), "%a, %d %b %Y %H:%M:%S %z")  # Thu, 09 Nov 2023 16:25:33 GMT
        # a more recent date is considered _greater_ than an older date
        if item_date <= last_item_date:
            continue

        post_author = item.find("dc:creator", {"dc": "http://purl.org/dc/elements/1.1/"}).text  # @username
        post_author_link = "https://twitter.com/" + post_author.replace("@", "")
        post_url = item.find("link").text
        is_retweet = feed_owner.find(post_author) == -1

        if is_retweet and feed["include_retweets"] == False:
            continue

        post_url = urlunparse(urlparse(post_url)._replace(netloc="fxtwitter.com"))

        if is_retweet:
            output = f"♻️ [{feed_owner_accountname}](<{feed_owner_link}>) retweeted [{post_author}](<{post_author_link}>)\n{post_url}"
        else:
            output = f"📢 [{feed_owner_accountname}](<{feed_owner_link}>) tweeted \n{post_url}"

        for webhook in feed["webhooks"]:
            requests.post(webhook, {"content": output})

    return {"last_item_date": items[0].find("pubDate").text}  # we assume that the first item is the newest one
