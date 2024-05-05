import time

from file_handler import JsonFile
from rss_feed import RssFeed
from sender import Sender
from timestamps import Timestamps
from utils import FeedConfigError, handle_error_reporting


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
        try:
            # -- start of config validation --
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

            # -- end of config validation --

            feed = RssFeed(url, webhooks, feed_config.get("embed_color"))

            # removes posts that are older than the last time we checked
            feed.remove_old_posts(timestamps.get(feed.url))

            # always update - also ensures that new feeds are added to the timestamps file
            timestamps.update(feed.url, feed.latest_timestamp)

            # skip feed if no new posts
            if not feed.posts:
                continue

            feed.make_embeds()
            sender.add(feed)

        # TODO - add more specific error handling
        except Exception as feed_err:
            handle_error_reporting(feed_err)

    sender.send_embeds()

    timestamps.write()

    END_TIME = time.time()
    print(f"Execution time: {round(END_TIME - START_TIME, 1)} seconds")


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        handle_error_reporting(err)
