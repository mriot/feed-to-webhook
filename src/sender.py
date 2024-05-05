import json
import time

import requests

from feed import Feed
from utils import WebhookHTTPError


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
        MAX_RETRY_LIMIT = 3

        for sorted_embeds in self.sort_embeds():
            for webhook in sorted_embeds["feed"].webhooks:
                for counter in range(MAX_RETRY_LIMIT):
                    res = requests.post(
                        webhook,
                        json={"embeds": sorted_embeds["embeds"]},
                        headers={"Content-Type": "application/json"},
                        timeout=5,
                    )

                    # Rate limit handling
                    if res.status_code == 429:
                        print(f"Rate limit reached for webhook {webhook}")
                        retry_after = min(int(res.headers.get("retry_after", 1)), 5)
                        print(f"Retrying in {retry_after} seconds. {counter+1}/{MAX_RETRY_LIMIT}")

                        time.sleep(int(retry_after))
                        continue

                    # Check for any other error codes
                    if res.status_code >= 300:
                        raise WebhookHTTPError(
                            f"Status code {res.status_code} ({res.reason})",
                            f"Feed: {sorted_embeds.get("feed").url}\n"
                            f"Webhook: {webhook}\nResponse:",
                            json.dumps(res.json(), indent=2)
                        )

                    break  # if we reach this point, the request was successful
                else:
                    # we could not make it past the rate limit for some reason
                    raise WebhookHTTPError(
                        f"Rate limit exceeded: {res.status_code} ({res.reason})",
                        f"Feed: {sorted_embeds.get("feed").url}\n"
                        f"Webhook: {webhook}",
                        json.dumps(res.json(), indent=2)
                    )
