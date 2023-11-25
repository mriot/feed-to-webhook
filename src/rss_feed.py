from urllib.parse import urlparse, urlunparse
import xml.etree.ElementTree as ET
from discord_embed import discord_embed
from feed import Feed, FeedItem


class RssFeed(Feed):
    # TODO: add embed color param
    def __init__(self, url, webhooks, summarize=True):
        super().__init__(url, webhooks)
        self.summarize = summarize

    def summarize_text(self):
        pass

    def sanitize(self):
        if not self._feed_root or not isinstance(self._feed_root, ET.Element):
            raise Exception("Root element not found")

        items = self._feed_root.findall("channel/item")

        feed_owner = self._feed_root.findtext("channel/title")
        feed_description = self._feed_root.findtext("channel/description")
        feed_owner_link = self._feed_root.findtext("channel/link")

        for item in reversed(items[:5]):
            data = {
                "feed_owner": feed_owner,
                "feed_description": feed_description,
                "feed_owner_link": feed_owner_link,
                "post_title": item.findtext("title"),
                "post_url": item.findtext("link"),
                "post_description": item.findtext("description"),
                # "post_date": item_date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                # "enclosure": item.find("enclosure").get("url") if item.find("enclosure") != None else "",
                # "color": int(feed.get("embed_color", "0"), 16)
            }

            output = discord_embed(data)

            self.content.append(output)

        return self
