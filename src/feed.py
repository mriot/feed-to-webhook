from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
from dateutil.parser import parse
import feedparser


class FeedItem():
    def __init__(self, item):
        self.item_root = item
        # print("\n", self.item_root)

    def get_pubdate(self):
        return parse(self.item_root.get("published"))  # datetime object

    def get_author(self):
        return self.item_root.get("author")


class Feed(ABC):
    def __init__(self, url, webhooks):
        self.url = url
        self.webhooks = webhooks

        self.feed_root = {}
        self.feed_items = []
        self.latest_timestamp = None
        self.final_items_to_be_posted = []  # populated by prepare_content()

    @abstractmethod
    def prepare_content(self):
        return self

    def load(self):
        self.feed_root = feedparser.parse(self.url)

        if not isinstance(self.feed_root, feedparser.FeedParserDict):
            raise Exception(f"Root element not found in feed {self.url}")

        self.latest_timestamp = self.feed_root.entries[0].published
        self._make_feed_items()

        print(type(self.feed_root))
        temp = self.feed_root.get('title', 'No title')
        print(temp)

        return self

    def _make_feed_items(self):
        items = self.feed_root.get("items", [])
        self.feed_items = [FeedItem(item) for item in reversed(items[:5])]
