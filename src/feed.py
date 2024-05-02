from abc import ABC, abstractmethod
from dateutil.parser import parse
import feedparser


class Feed(ABC):
    def __init__(self, url, webhooks):
        self.url = url
        self.webhooks = webhooks

        self.title = ""
        self.description = ""
        self.link = ""
        self.avatar_url = ""

        self.feed_items = []
        self.latest_timestamp = None
        self.new_feed_items = []  # populated by make_embeds()

    @abstractmethod
    def make_embeds(self):
        return self

    def load(self):
        feed_data = feedparser.parse(self.url)

        if feed_data.get("bozo_exception"):
            raise Exception(
                f"Failed to parse feed from URL {self.url}\n{feed_data.get('bozo_exception')}"
            )

        self._gather_feed_data(feed_data)

    def _gather_feed_data(self, data):
        channel = data.get("feed")  # information about the feed itself
        entries = data.get("entries")  # data about the actual feed items

        self.title = channel.get("title", "Untitled")
        self.description = channel.get("description", "")
        self.link = channel.get("link", "")
        self.avatar_url = channel.get("image", {}).get("url", "")

        self.feed_items = self._make_feed_items(entries)
        self.latest_timestamp = max((item.pub_date) for item in self.feed_items)

    def remove_old_posts(self, timestamps):
        self.feed_items = [
            post for post in self.feed_items if post.pub_date > timestamps.get(self.url)
        ]

    def _make_feed_items(self, entries):
        if not entries:
            raise Exception(f"Failed to extract feed items from {self.url}")
        return [FeedItem(item) for item in entries[:20]]
        # note: upper limit just in case


class FeedItem:
    def __init__(self, item):
        self.link = item.get("link", "")
        self.title = item.get("title", "")
        self.pub_date = parse(item.get("published"))
        self.description = item.get("description", "")
        self.author = item.get("author", "")
        self.media = item.get("media_content", [])
