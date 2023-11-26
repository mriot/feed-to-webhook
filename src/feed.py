from abc import ABC, abstractmethod
from dateutil.parser import parse
import feedparser


class FeedItem():
    def __init__(self, item):
        self.item_root = item

    def get_pubdate(self):
        return parse(self.item_root.get("published"), ignoretz=True)  # datetime object

    def get_author(self):
        return self.item_root.get("author")


class Feed(ABC):
    def __init__(self, url, webhooks):
        self.url = url
        self.webhooks = webhooks

        self.feed_data_dict = feedparser.FeedParserDict()
        self.feed_items = []
        self.latest_timestamp = None
        self.final_items_to_be_posted = []  # populated by prepare_content()

    @abstractmethod
    def prepare_content(self):
        return self

    def load(self):
        self.feed_data_dict = feedparser.parse(self.url)

        # TODO
        if self.feed_data_dict.get("bozo_exception"):
            raise Exception(f"Malformed feed data {self.feed_data_dict.get('bozo_exception')}")

        self.latest_timestamp = self.feed_data_dict.get("items", [])[0].get("published")
        self._make_feed_items()
        return self

    def _make_feed_items(self):
        items = self.feed_data_dict.get("items", [])
        self.feed_items = [FeedItem(item) for item in reversed(items[:5])]
