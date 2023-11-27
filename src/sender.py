import requests
from feed import Feed


class Sender:
    def __init__(self, feed: Feed):
        if not isinstance(feed, Feed):
            raise TypeError("'feed' must be an instance of Feed")
        self.feed = feed

    def send(self):
        posts = self.feed.prepare_content().final_items_to_be_posted
        for post in posts:
            for webhook in self.feed.webhooks:
                res = requests.post(webhook, {"content": post})
                print(f"Status Code: {res.status_code}, Message: {res.reason}")

    def send_json(self):
        posts = self.feed.prepare_content().final_items_to_be_posted
        for post in posts:
            for webhook in self.feed.webhooks:
                res = requests.post(webhook, json={"embeds": post}, headers={"Content-Type": "application/json"})
                print(f"Status Code: {res.status_code}, Message: {res.reason}")