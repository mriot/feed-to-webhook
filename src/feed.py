from abc import ABC, abstractmethod
from dateutil.parser import parse
import feedparser


class FeedItem():
    def __init__(self, item):
        self.item_root = item

    def get_pubdate(self):
        return parse(self.item_root.get("published"))  # datetime object

    def get_author(self):
        return self.item_root.get("author")


class Feed(ABC):
    def __init__(self, url, webhooks):
        self.url = url
        self.webhooks = webhooks

        self.feed_data_dict = feedparser.FeedParserDict()
        self.feed_items = []
        self.latest_timestamp = None
        self.final_items_to_be_posted = []  # populated by make_embeds()

        # self.load()

    @abstractmethod
    def make_embeds(self):
        return self

    def load(self):
        self.feed_data_dict = feedparser.parse(self.url)

        if self.feed_data_dict.get("bozo_exception"):
            raise Exception(f"Failed to parse feed from URL {self.url}\n{self.feed_data_dict.get('bozo_exception')}")

        self.latest_timestamp = self.feed_data_dict.get("items", [])[0].get("published")
        self._make_feed_items()
        return self

    def remove_old_posts(self, timestamps):
        self.feed_items = [post for post in self.feed_items if post.get_pubdate() > timestamps.get(self.url)]

    def _make_feed_items(self):
        items = self.feed_data_dict.get("items", [])
        self.feed_items = [FeedItem(item) for item in reversed(items[:5])]
