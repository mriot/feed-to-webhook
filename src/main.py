import json
import requests
from sender import Sender
from rss_feed import RssFeed
from timestamps import Timestamps
from file_handler import JsonFile
import traceback
import time

from utils import FeedConfigError


def main():
    START_TIME = time.time()

    config = JsonFile("config.json", False).read()
    timestamps = Timestamps()
    sender = Sender()

    if feeds := config.get("feeds"):
        if not isinstance(feeds, list):
            raise TypeError("Key 'feeds' must be a list of feed objects.")
    else:
        raise KeyError("Could not find the mandatory key 'feeds' in the config file.")

    for feed_config in feeds:
        # feed config validation
        if missing_keys := [key for key in ["url", "webhooks"] if key not in feed_config]:
            raise FeedConfigError(f"{' and '.join(missing_keys)} not found", feed_config)

        if url := feed_config.get("url"):
            if not isinstance(url, str):
                raise FeedConfigError("Feed URL must be a string", feed_config)
        else:
            raise FeedConfigError("No URL configured", feed_config)

        if webhooks := feed_config.get("webhooks"):
            if not isinstance(webhooks, list):
                raise FeedConfigError("Webhooks must be a list of URLs.", feed_config)
        else:
            raise FeedConfigError("No webhooks configured", feed_config)

        feed = RssFeed(url, webhooks, feed_config.get("embed_color"))

        # removes posts that are older than the last time we checked
        # feed.remove_old_posts(timestamps.get(feed.url))
        feed.remove_old_posts(timestamps.get(feed.url))

        # always update - also ensures that new feeds are added to the timestamps file
        timestamps.update(feed.url, feed.latest_timestamp)

        # skip if no new posts
        if not feed.posts:
            continue

        feed.make_embeds()
        sender.add(feed)

    sender.send_embeds()

    timestamps.write()

    END_TIME = time.time()
    print(f"Execution time: {round(END_TIME - START_TIME, 1)} seconds")


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        tb = traceback.TracebackException.from_exception(err).stack[-1]
        err_msg = f"Error raised in '{tb.filename}' at line {tb.lineno} in function '{tb.name}'"

        if isinstance(err, FeedConfigError):
            err_msg = f"```{json.dumps(err.feed_config, indent=2)}``` \n {err_msg}"

        print(f"ERROR: {err}\n{err_msg}")

        # also send the error to the error webhook if it is configured
        if errhook := JsonFile("config.json", False).read().get("error_webhook"):
            requests.post(
                errhook,
                json={
                    "embeds": [
                        {
                            "title": f"ERROR:  {err}",
                            "description": err_msg,
                            "color": 16711680,
                        }
                    ]
                },
                headers={"Content-Type": "application/json"},
            )
