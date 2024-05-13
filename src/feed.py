from abc import ABC, abstractmethod
from datetime import datetime
import json
from typing import Optional
import dateutil.parser
import feedparser
import requests

from embed import Embed
from utils import get_favicon_url


class Feed(ABC):
    def __init__(self, url: str, webhooks: list[str], embed_color: Optional[str] = None):
        self.url: str = url
        self.webhooks: list[str] = webhooks
        self.embed_color: int = int(embed_color if embed_color is not None else "738adb", 16)

        res = requests.get(self.url, timeout=5)

        res.raise_for_status()

        feed_data: feedparser.FeedParserDict = feedparser.parse(res.text)

        # attempt to fix encoding issues by forcing utf-8
        if feed_data.get("bozo_exception") and res.encoding != "utf-8":
            res.encoding = "utf-8"
            feed_data = feedparser.parse(res.text)

            # raise if we still can't parse the feed
            if feed_data.get("bozo_exception"):
                raise ValueError(
                    f"Failed to parse feed from URL {self.url}\n{feed_data.get('bozo_exception')}"
                )

        channel = feed_data.get("feed")
        entries = feed_data.get("entries")

        # might be a list of FeedParserDicts - should be a single dict
        if not isinstance(channel, dict):
            raise TypeError(f"Failed to extract feed data from {self.url}")

        if not isinstance(entries, list):
            raise TypeError(f"Failed to extract posts from feed {self.url}")

        if not entries:
            raise ValueError(
                f"No posts found in feed {self.url}\n{json.dumps(feed_data, indent=2)}"
            )

        self.feed_title: str = channel.get("title", "Untitled")
        self.feed_description: str = channel.get("description", "")
        self.feed_link: str = channel.get("link", "")
        self.feed_avatar_url: str = channel.get("image", {}).get("url")
        if not self.feed_avatar_url:
            self.feed_avatar_url = get_favicon_url(self.feed_link)

        self.posts: list[Post] = [Post(item) for item in entries[:25]]  # upper limit just in case
        self.latest_timestamp: datetime = max((item.post_pub_date) for item in self.posts)

    def remove_old_posts(self, timestamp: datetime) -> None:
        self.posts: list[Post] = [post for post in self.posts if post.post_pub_date > timestamp]

    @abstractmethod
    def generate_embeds(self) -> list[Embed]:
        pass


class Post:
    def __init__(self, item):
        self.post_link: str = item.get("link", "")
        self.post_title: str = item.get("title", "")
        self.post_pub_date: datetime = dateutil.parser.parse(item.get("published"))
        self.post_author: str = item.get("author", "")
        self.post_description: str = item.get("description", "")
        self.post_media: list = item.get("media_content", [])
        self.post_content: list = item.get("content", [])
