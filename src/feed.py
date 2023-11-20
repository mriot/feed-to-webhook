from abc import ABC, abstractmethod
import requests
import xml.etree.ElementTree as ET


class Feed(ABC):
    def __init__(self, url, webhooks, include_retweets):
        self.url = url
        self.webhooks = webhooks
        self.include_retweets = include_retweets

        self.payload = {}
        self.root_element = None

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
            self.root_element = root
        except ET.ParseError as e:
            self.payload = {"error": str(e)}


# TODO - implement
class TwitterFeed(Feed):
    def __init__(self, url, webhooks, include_retweets):
        super().__init__(url, webhooks, include_retweets)

    def sanitize(self):
        if self.root_element is None:
            raise Exception("No root element found")
        tweets = []
        for tweet in self.root_element.findall("channel/item"):
            title = tweet.find("title").text
            link = tweet.find("link").text
            description = tweet.find("description").text
            tweets.append({
                "title": title,
                "link": link,
                "description": description
            })
        self.payload = {"content": tweets}
        return self
