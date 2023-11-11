import requests
from datetime import datetime
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, urlunparse


def rss_feed(feed):
    response = requests.get(feed["url"], headers={"User-Agent": "Hi, I am a bot!"})

    if (response.status_code != 200):
        return {"error": response.status_code}

    root = ET.fromstring(response.content.decode("utf-8"))
    items = root.findall("channel/item")

    feed_owner = root.find("channel/title").text
    feed_description = root.find("channel/description").text
    feed_owner_link = root.find("channel/link").text

    # first run of script only gets the newest item date and returns it
    if feed.get("last_item_date") == None:
        return {"last_item_date": items[0].find("pubDate").text}

    # get last item date from config for comparison
    last_item_date = datetime.strptime(feed.get("last_item_date").replace("GMT", "+0000"), "%a, %d %b %Y %H:%M:%S %z")
