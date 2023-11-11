import requests
import json
from datetime import datetime
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, urlunparse
from discord_embed import discord_embed


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

    # loop through items in feed in reverse order (older first)
    for i, item in enumerate(reversed(items[:5])):
        item_date = datetime.strptime(item.find("pubDate").text.replace("GMT", "+0000"), "%a, %d %b %Y %H:%M:%S %z")  # Thu, 09 Nov 2023 16:25:33 GMT
        # a more recent date is considered _greater_ than an older date
        if item_date <= last_item_date:
            continue

        post_title = items[i].find("title").text
        post_url = items[i].find("link").text
        post_description = items[i].find("description").text
        enclosure = items[i].find("enclosure").get("url") if items[i].find("enclosure") != None else ""

        output = discord_embed(post_title, post_url, post_description, enclosure)

        for webhook in feed["webhooks"]:
            requests.post(webhook, json={"embeds": output})

    return {"last_item_date": items[0].find("pubDate").text}  # we assume that the first item is the newest one
