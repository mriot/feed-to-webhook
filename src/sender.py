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
                if res.status_code > 299:
                    raise Exception(f"Webhook '{webhook}' responded with status code {res.status_code} and message '{res.reason}'")

    def send_json(self):
        posts = self.feed.prepare_content().final_items_to_be_posted
        for post in posts:
            for webhook in self.feed.webhooks:
                res = requests.post(webhook, json={"embeds": post}, headers={"Content-Type": "application/json"})
                if res.status_code > 299:
                    raise Exception(f"**Status code {res.status_code}** ({res.reason})\n**Feed**: {self.feed.url}\n**Webhook: **{webhook}\n**Payload**:\n```json\n{res.request.body}```")
