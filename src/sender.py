import json
import time

import requests

from exceptions import WebhookHTTPError, WebhookRateLimitError
from feed import Feed


class Sender:
    def __init__(self):
        self.feeds: list[Feed] = []

    def add(self, feed: Feed) -> None:
        self.feeds.append(feed)

    def sort_embeds(self) -> list[dict]:
        embed_list: list[dict] = []
        for feed in self.feeds:
            for embed in feed.generate_embeds():
                embed_list.append({"embed": embed.build(), "feed": feed})
        embed_list.sort(key=lambda x: x["feed"].last_post_date)
        return embed_list

    def send(self) -> None:
        MAX_RETRY_LIMIT: int = 3

        for sorted_embed in self.sort_embeds():
            for webhook in sorted_embed["feed"].webhooks:
                try:
                    for counter in range(MAX_RETRY_LIMIT):
                        res = requests.post(
                            webhook,
                            json={"embeds": sorted_embed["embed"]},
                            headers={"Content-Type": "application/json"},
                            timeout=5,
                        )

                        # Rate limit handling
                        if res.status_code == 429:
                            print(f"Rate limit reached for webhook {webhook}")
                            retry_after = min(int(res.headers.get("retry_after", 1)), 5)
                            print(
                                f"Retrying in {retry_after} seconds. {counter+1}/{MAX_RETRY_LIMIT}"
                            )

                            time.sleep(int(retry_after))
                            continue

                        # Check for any other error codes
                        if res.status_code >= 400:
                            raise WebhookHTTPError(
                                title=f"Could not send message - {res.status_code} ({res.reason})",
                                feed_url=sorted_embed["feed"].url,
                                webhook_url=webhook,
                                response=json.dumps(res.json(), indent=2),
                                payload=json.dumps(sorted_embed["embed"], indent=2),
                            )

                        break  # if we reach this point, the request was successful
                        ###########################################################
                    else:
                        # we could not make it past the rate limit for some reason
                        raise WebhookRateLimitError(
                            feed_url=sorted_embed["feed"].url, webhook_url=webhook
                        )

                # catch any exceptions that might have occurred during the request
                except WebhookHTTPError as err:
                    err.report()
                    continue  # try the next webhook
