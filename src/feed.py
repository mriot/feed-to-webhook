from abc import ABC, abstractmethod
import requests
import xml.etree.ElementTree as ET


class Feed(ABC):
    def __init__(self, url, webhooks):
        self.url = url
        self.webhooks = webhooks
        self.latest_timestamp = None
        self.content = ""

        self._error = None
        self._payload = {}
        self._feed_root = None

    @abstractmethod
    def sanitize(self):
        return self

    def load(self):
        self._fetch()
        self._parse()
        return self

    def _fetch(self):
        response = requests.get(self.url, headers={"User-Agent": "Hi, I am a bot!"})
        if 200 < response.status_code >= 300:
            self._error = response.status_code
            raise Exception(response.status_code)
        self._payload = response.content

    def _parse(self):
        try:
            if not isinstance(self._payload, bytes):
                raise ET.ParseError
            root = ET.fromstring(self._payload.decode())
            self._feed_root = root
            self.latest_timestamp = root.findtext("channel/item/pubDate")
        except ET.ParseError as e:
            self._error = str(e)

    # def _feed_items(self):
    #     items = self._feed_root.findall("channel/item")
    #     self.feed_items = [FeedItem(item) for item in reversed(items[:5])]


# class FeedItem():
#     def __init__(self, item):
#         self.item = item
#     pass


class TwitterFeed(Feed):
    def __init__(self, url, webhooks, include_retweets):
        super().__init__(url, webhooks)
        self.include_retweets = include_retweets

    def sanitize(self):
        if not self._feed_root or not isinstance(self._feed_root, ET.Element):
            raise Exception("Root element not found")

        items = self._feed_root.findall("channel/item")

        feed_owner = self._feed_root.findtext("channel/title")  # username / @username
        # feed_owner_accountname = feed_owner.split(" / ")[-1]  # @username
        # feed_owner_link = "https://twitter.com/" + feed_owner_accountname.replace("@", "")

        # if is_retweet:
        #     output = f"♻️ [{feed_owner_accountname}](<{feed_owner_link}>) retweeted [{post_author}](<{post_author_link}>)\n{post_url}"
        # else:
        #     output = f"📢 [{feed_owner_accountname}](<{feed_owner_link}>) tweeted \n{post_url}"

        self.content = f"blub {feed_owner}"

        return self
