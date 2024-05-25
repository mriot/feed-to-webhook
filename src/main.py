import logging
import time

from exceptions import (
    ConfigError,
    CustomBaseException,
    FeedConfigError,
    FeedParseError,
    NoItemsInFeedError,
)
from file_handler import JsonFile
from rss_feed import RssFeed
from sender import Sender
from timestamps import Timestamps


def main():
    START_TIME = time.time()

    config = JsonFile("config.json", False).read()
    timestamps = Timestamps()
    sender = Sender()

    if not (feeds := config.get("feeds")) or not isinstance(feeds, list):
        raise ConfigError(
            "Config format is incorrect",
            "Key 'feeds' is required and must be a list of feed objects.",
        )

    timestamps.remove_unconfigured_entries([feed.get("url") for feed in feeds])

    for feed_config in feeds:
        try:
            if not (url := feed_config.get("url")) or not isinstance(url, str):
                raise FeedConfigError("Feed URL is not configured properly", feed_config)

            if not (webhooks := feed_config.get("webhooks")) or not isinstance(webhooks, list):
                raise FeedConfigError("Webhooks are not configured properly", feed_config)

            feed = RssFeed(
                url,
                webhooks,
                feed_config.get("embed_color"),
                feed_config.get("icon_url"),
            )

            if not feed.parse(
                timestamps.get_etag(feed.url),
                timestamps.get_last_modified(feed.url),
            ):
                continue  # skip feed if the server said it hasn't been modified

            feed.remove_old_posts(timestamps.get_last_post_date(feed.url))

            # always update - ensures that new feeds are added to the timestamps file
            timestamps.update(feed.url, feed.last_post_date, feed.etag, feed.last_modified)

            if not feed.posts:
                continue  # skip feed if no new posts are found

            sender.add(feed)

        except FeedParseError as feed_error:
            feed_error.report()
            continue
        except NoItemsInFeedError as no_items_error:
            no_items_error.log(logging.WARNING)
            continue

    sender.send()

    timestamps.write()

    END_TIME = time.time()
    print(f"Execution time: {round(END_TIME - START_TIME, 1)} seconds")


if __name__ == "__main__":
    try:
        main()
    except CustomBaseException as known_error:
        known_error.report()
    except Exception as unknown_error:
        logging.error(f"Unhandled exception: {unknown_error}")
