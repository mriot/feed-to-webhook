import requests
import json
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, urlunparse
from discord_embed import discord_embed


def rss_feed(feed, last_item_date):
    response = requests.get(feed["url"], headers={"User-Agent": "Hi, I am a bot!"})

    if (response.status_code != 200):
        return {"error": response.status_code, "last_item_date": last_item_date}

    root = ET.fromstring(response.content.decode("utf-8"))
    items = root.findall("channel/item")

    feed_owner = root.find("channel/title").text
    feed_description = root.find("channel/description").text
    feed_owner_link = root.find("channel/link").text

    # first run of script only gets the newest item date and returns it
    if last_item_date == None:
        return {"last_item_date": items[0].find("pubDate").text}

    # get last item date from config for comparison
    last_item_date = datetime.strptime(last_item_date.replace("GMT", "+0000"), "%a, %d %b %Y %H:%M:%S %z")

    # loop through items in feed in reverse order (older first)
    for item in reversed(items[:5]):
        item_date = datetime.strptime(item.find("pubDate").text.replace("GMT", "+0000"), "%a, %d %b %Y %H:%M:%S %z")  # Thu, 09 Nov 2023 16:25:33 GMT
        # a more recent date is considered _greater_ than an older date
        if item_date <= last_item_date:
            continue

        data = {
            "feed_owner": feed_owner,
            "feed_description": feed_description,
            "feed_owner_link": feed_owner_link,
            "post_title": item.find("title").text,
            "post_url": item.find("link").text,
            "post_description": item.find("description").text,
            "post_date": item_date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "enclosure": item.find("enclosure").get("url") if item.find("enclosure") != None else "",
            "color": int(feed.get("embed_color", "0"), 16)
        }

        output = discord_embed(data)

        for webhook in feed.get("webhooks", []):
            requests.post(webhook, json={"embeds": output})

    return {"last_item_date": items[0].find("pubDate").text}  # we assume that the first item is the newest one
