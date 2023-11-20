import requests
from feed import Feed


class Sender:
    def __init__(self, feed: Feed):
        if not isinstance(feed, Feed):
            raise TypeError("'feed' must be an instance of Feed")
        self.feed = feed

    def send(self):
        for webhook in self.feed.webhooks:
            requests.post(webhook, {"content": self.feed.load().sanitize().content})
