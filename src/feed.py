import requests
import xml.etree.ElementTree as ET


class Feed:
    def __init__(self, feed_config):
        self.feed_config = feed_config

    def load(self):
        response = self.fetch()
        if "error" in response:
            return response["error"]
        content = self.parse(response["content"])
        return content

    def fetch(self):
        response = requests.get(self.feed_config["url"], headers={"User-Agent": "Hi, I am a bot!"})
        if response.status_code != 200:
            return {"error": response.status_code}

        return {"content": response.content}

    def parse(self, content):
        try:
            root = ET.fromstring(content.decode("utf-8"))
            return {"root": root}
        except ET.ParseError:
            return {"error": "ParseError"}


class TwitterFeed(Feed):
    def __init__(self, url, webgooks, include_retweets=False):
        # super().__init__(feed_config)
        pass


# feed = TwitterFeed({"url": "https://www.reddit.com/r/Python/.rss"}).load()
