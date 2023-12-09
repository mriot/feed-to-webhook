import requests
from sender import Sender
from twitter_feed import TwitterFeed
from rss_feed import RssFeed
from timestamps import Timestamps
from file_handler import YamlFile
import traceback
import time


def main():
    START_TIME = time.time()

    CONFIG = YamlFile("config.yaml", False).read()
    timestamps = Timestamps()
    sender = Sender()

    def process_feed(feed):
        try:
            feed.load()
            feed.remove_old_posts(timestamps)
            timestamps.update(feed)

            if not feed.feed_items:
                return

            feed.make_embeds()
            sender.add(feed)
        except Exception as e:
            tb = traceback.TracebackException.from_exception(e).stack[-1]
            err = f"❌ {e}\n-> Error occurred in file '{tb.filename}' at line {tb.lineno} in function '{tb.name}'"
            print(err)
            requests.post(CONFIG.get("error_webhook"), {"content": err})

    # twitter
    for tfeed in CONFIG.get("twitter_feeds", []):
        process_feed(TwitterFeed(
            tfeed.get("url"),
            tfeed.get("webhooks"),
            tfeed.get("embed_color"),
            tfeed.get("exclude_retweets"),
            tfeed.get("override_domain"),
        ))

    # rss
    for rfeed in CONFIG.get("rss_feeds", []):
        process_feed(RssFeed(
            rfeed.get("url"),
            rfeed.get("webhooks"),
            rfeed.get("embed_color"),
            rfeed.get("summarize")  # TODO: implement
        ))

    sender.send_embeds()

    timestamps.write()

    END_TIME = time.time()
    print(f"Execution time: {round(END_TIME - START_TIME, 1)} seconds")


if __name__ == "__main__":
    main()
