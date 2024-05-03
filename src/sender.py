from dateutil.parser import parse
import requests
from feed import Feed


class Sender:
    def __init__(self):
        self.feeds = []

    def add(self, feed: Feed):
        self.feeds.append(feed)

    def sort_embeds(self):
        embed_list = []
        for feed in self.feeds:
            for embed in feed.new_embedded_posts:
                embed_list.append({"embeds": embed, "feed": feed})
        embed_list.sort(key=lambda x: x["feed"].latest_timestamp)
        return embed_list

    def send_embeds(self):
        for sorted_embeds in self.sort_embeds():
            for webhook in sorted_embeds["feed"].webhooks:
                res = requests.post(
                    webhook,
                    json={"embeds": sorted_embeds["embeds"]},
                    headers={"Content-Type": "application/json"},
                )

                # TODO - handle rate limit
                if res.status_code == 429:
                    print(f"Rate limit exceeded for webhook {webhook}")
                    retry_after = res.headers.get("retry_after")
                    if retry_after:
                        # time.sleep(int(retry_after))
                        # threading.Timer(int(retry_after), send_request, args=[data]).start()
                        pass

                if res.status_code >= 300:
                    raise Exception(
                        f"**Status code {res.status_code}** ({res.reason})\n**Feed**: {sorted_embeds.feed.url}\n**Webhook: **{webhook}\n**Payload**:\n```json\n{res.request.body}```"
                    )
