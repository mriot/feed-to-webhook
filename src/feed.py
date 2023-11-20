from abc import ABC, abstractmethod
import requests
import xml.etree.ElementTree as ET


class Feed(ABC):
    def __init__(self, url, webhooks, include_retweets):
        self.url = url
        self.webhooks = webhooks
        self.include_retweets = include_retweets

        self.payload = {}
        self.content = ""

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
            self.payload = {"error": response.status_code}
            raise Exception(response.status_code)
        self.payload = {"content": response.content}

    def _parse(self):
        try:
            payload = self.payload.get("content")
            if not isinstance(payload, bytes):
                raise ET.ParseError
            root = ET.fromstring(payload.decode())
            self.payload = {"root": root}
        except ET.ParseError as e:
            self.payload = {"error": str(e)}


class TwitterFeed(Feed):
    def __init__(self, url, webhooks, include_retweets):
        super().__init__(url, webhooks, include_retweets)

    def sanitize(self):
        root = self.payload.get("root")
        if not root or not isinstance(root, ET.Element):
            raise Exception("Root element not found")

        items = root.findall("channel/item")

        feed_owner = (root.find("channel/title") or ET.Element("")).text  # username / @username
        feed_owner_accountname = feed_owner.split(" / ")[-1]  # @username
        feed_owner_link = "https://twitter.com/" + feed_owner_accountname.replace("@", "")

        # if is_retweet:
        #     output = f"♻️ [{feed_owner_accountname}](<{feed_owner_link}>) retweeted [{post_author}](<{post_author_link}>)\n{post_url}"
        # else:
        #     output = f"📢 [{feed_owner_accountname}](<{feed_owner_link}>) tweeted \n{post_url}"

        self.content = "blub"

        return self
