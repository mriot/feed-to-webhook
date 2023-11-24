from abc import ABC, abstractmethod
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, urlunparse
from dateutil.parser import parse
from discord_embed import discord_embed


class Feed(ABC):
    def __init__(self, url, webhooks):
        self.url = url
        self.webhooks = webhooks
        self.latest_timestamp = None
        self.feed_items = []
        self.content = []

        self._error = None
        self._payload = {}
        self._feed_root = None

    @abstractmethod
    def sanitize(self):
        return self

    def load(self):
        self._fetch()
        self._parse()
        self._feed_items()
        return self

    def _fetch(self):
        response = requests.get(self.url, headers={"User-Agent": "Hi, I am a bot!"})
        if 200 < response.status_code >= 300:
            self._error = response.status_code
            raise Exception(response.status_code)  # TODO: fetch exception
        self._payload = response.content

    def _parse(self):
        try:
            if not isinstance(self._payload, bytes):
                raise ET.ParseError
            root = ET.fromstring(self._payload.decode())
            self._feed_root = root
            self.latest_timestamp = root.findtext("channel/item/pubDate")  # TODO: still needed?
        except ET.ParseError as e:
            self._error = str(e)

    def _feed_items(self):
        if not self._feed_root or not isinstance(self._feed_root, ET.Element):
            raise Exception("Root element not found")
        items = self._feed_root.findall("channel/item")
        self.feed_items = [FeedItem(item) for item in reversed(items[:5])]


###############
## FEED ITEM ##
###############
class FeedItem():
    def __init__(self, item):
        self.root = item

    def get_pubdate(self):
        pubdate = self.root.findtext("pubDate")
        if not pubdate:
            return None
        return parse(pubdate)


##################
## TWITTER FEED ##
##################
class TwitterFeed(Feed):
    def __init__(self, url, webhooks, include_retweets=True):
        super().__init__(url, webhooks)
        self.include_retweets = include_retweets

    def sanitize(self):
        if not self._feed_root or not isinstance(self._feed_root, ET.Element):
            raise Exception("Root element not found")

        items = self.feed_items

        # TODO: error handling if name not found
        feed_owner = self._feed_root.findtext("channel/title") or "Unknown"  # username / @username
        feed_owner_accountname = feed_owner.split(" / ")[-1]  # @username
        feed_owner_link = "https://twitter.com/" + feed_owner_accountname.replace("@", "")

        for item in reversed(items[:5]):
            post_author = item.root.findtext("dc:creator", default="", namespaces={"dc": "http://purl.org/dc/elements/1.1/"})  # @username
            post_author_link = "https://twitter.com/" + post_author.replace("@", "")
            post_url = item.root.findtext("link")
            is_retweet = feed_owner.find(post_author) == -1

            if is_retweet and not self.include_retweets:
                continue

            post_url = urlunparse(urlparse(post_url)._replace(netloc="fxtwitter.com"))

            if is_retweet:
                output = f"♻️ [{feed_owner_accountname}](<{feed_owner_link}>) retweeted [{post_author}](<{post_author_link}>)\n{post_url}"
            else:
                output = f"📢 [{feed_owner_accountname}](<{feed_owner_link}>) tweeted \n{post_url}"

            self.content.append(output)

        return self


##############
## RSS FEED ##
##############
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
