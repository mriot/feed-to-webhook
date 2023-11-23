import requests
from feed import Feed


class Sender:
    def __init__(self, feed: Feed):
        if not isinstance(feed, Feed):
            raise TypeError("'feed' must be an instance of Feed")
        self.feed = feed

    def send(self):
        posts = self.feed.sanitize().content
        for post in posts:
            for webhook in self.feed.webhooks:
                requests.post(webhook, {"content": post})

    def send_json(self):
        posts = self.feed.sanitize().content
        for post in posts:
            for webhook in self.feed.webhooks:
                requests.post(webhook, json={"embeds": post})
