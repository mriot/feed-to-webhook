from abc import ABC, abstractmethod
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, urlunparse
from dateutil.parser import parse
from discord_embed import discord_embed


class FeedItem():
    def __init__(self, item):
        self.root = item

    def get_pubdate(self):
        pubdate = self.root.findtext("pubDate")
        if not pubdate:
            return None
        return parse(pubdate)


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
