from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from xml.sax import SAXParseException
import dateutil.parser
import feedparser

from embed import Embed
from utils import get_favicon_url


class Feed(ABC):
    def __init__(self, url: str, webhooks: list[str], embed_color: Optional[str] = None):
        self.url: str = url
        self.webhooks: list[str] = webhooks
        self.embed_color: int = int(embed_color if embed_color is not None else "738adb", 16)

        self.etag: Optional[str] = None
        self.last_modified: Optional[str] = None
        self.status_code: Optional[int] = None
        self.redirected_url: str = self.url  # updated only if the feed has been redirected

        self.feed_title: str
        self.feed_link: str
        self.feed_description: str
        self.feed_avatar_url: str

        self.posts: list[Post]
        self.last_post_date: datetime

    def parse(self, etag: Optional[str] = None, last_modified: Optional[str] = None) -> bool:
        feed_data: feedparser.FeedParserDict = feedparser.parse(
            self.url, etag=etag, modified=last_modified
        )

        # provide a more fitting error message if something went wrong
        if feed_data.get("bozo") and isinstance(feed_data.get("bozo_exception"), SAXParseException):
            raise ValueError(
                f"Failed to parse feed {self.url} ({feed_data.get('status', 'is the path and file valid?')})"
            )

        if (code := feed_data.get("status")) and isinstance(code, int):
            self.status_code = code

        # if the feed has not been modified since the last request, we can skip parsing it
        if self.status_code == 304:  # 304 = Not Modified
            return False

        # on a redirect, 'status' will contain the redirect code, not the final status code
        # so we need to check manually if the feed has been modified
        # Moved Permanently (301), Found (302), Temporary Redirect (307), Permanent Redirect (308)
        if self.status_code in (301, 302, 307, 308) and (etag or last_modified):
            if (new_url := feed_data.get("href")) and isinstance(new_url, str):
                self.redirected_url = new_url

            if etag and etag == feed_data.get("etag"):
                return False

            if (new_modified := feed_data.get("modified")) and isinstance(new_modified, str):
                new_modified = dateutil.parser.parse(new_modified)
                if last_modified and dateutil.parser.parse(last_modified) == new_modified:
                    return False

        # update etag or last_modified if the server provided new ones
        if (new_etag := feed_data.get("etag")) and isinstance(new_etag, str):
            self.etag = new_etag

        elif (new_modified := feed_data.get("modified")) and isinstance(new_modified, str):
            self.last_modified = new_modified

        # --- extract feed data ---

        channel, entries = feed_data.get("feed"), feed_data.get("entries")

        if not isinstance(channel, dict):
            raise TypeError(f"Failed to extract feed data from {self.url}")

        if not isinstance(entries, list):
            raise TypeError(f"Failed to extract posts from feed {self.url}")

        if not entries:
            raise ValueError(f"No posts found in feed {self.url}")

        self.feed_title: str = channel.get("title", "Untitled")
        self.feed_link: str = channel.get("link", "")
        self.feed_description: str = channel.get("description", "")
        self.feed_avatar_url: str = channel.get("image", {}).get("url")
        if not self.feed_avatar_url:
            self.feed_avatar_url = get_favicon_url(self.feed_link)

        self.posts: list[Post] = [Post(item) for item in entries[:25]]  # upper limit just in case
        self.last_post_date: datetime = max((item.post_pub_date) for item in self.posts)

        return True

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
