import requests
from feed import Feed


class Sender:
    def __init__(self):
        self.feeds = []

    def add(self, feed: Feed):
        self.feeds.append(feed)

    def sort_embeds(self):
        # embeds = []
        # for feed in self.feeds:
        #     embeds.extend(feed.final_items_to_be_posted)
        # embeds.sort(key=lambda x: x[0]['timestamp'])
        # return embeds
        embeds = []
        for feed in self.feeds:
            embeds.extend({"feed": feed, "embeds": feed.final_items_to_be_posted})
        embeds.sort(key=lambda x: x["feed"]['latest_timestamp'])
        return embeds

    def send_embeds(self):
        for embed in self.sort_embeds():
            for webhook in embed.feed.webhooks:
                res = requests.post(webhook, json={"embeds": embed.embeds}, headers={"Content-Type": "application/json"})

                # TODO - handle rate limit
                if res.status_code == 429:
                    print(f"Rate limit exceeded for webhook {webhook}")
                    retry_after = res.headers.get('retry_after')
                    if retry_after:
                        # time.sleep(int(retry_after))
                        # threading.Timer(int(retry_after), send_request, args=[data]).start()
                        pass

                if res.status_code > 299:
                    raise Exception(f"**Status code {res.status_code}** ({res.reason})\n**Feed**: {embed.feed.url}\n**Webhook: **{webhook}\n**Payload**:\n```json\n{res.request.body}```")

    # DEPRECATED
    def send(self):
        posts = self.feed.prepare_content().final_items_to_be_posted
        for post in posts:
            for webhook in self.feed.webhooks:
                res = requests.post(webhook, {"content": post})
                if res.status_code > 299:
                    raise Exception(f"Webhook '{webhook}' responded with status code {res.status_code} and message '{res.reason}'")

     # DEPRECATED
    def send_json(self):
        posts = self.feed.prepare_content().final_items_to_be_posted
        for post in posts:
            for webhook in self.feed.webhooks:
                res = requests.post(webhook, json={"embeds": post}, headers={"Content-Type": "application/json"})
                if res.status_code > 299:
                    raise Exception(f"**Status code {res.status_code}** ({res.reason})\n**Feed**: {self.feed.url}\n**Webhook: **{webhook}\n**Payload**:\n```json\n{res.request.body}```")
