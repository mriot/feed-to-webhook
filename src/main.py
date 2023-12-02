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

    # twitter
    for tfeed in CONFIG.get("twitter_feeds", []):
        try:
            feed = TwitterFeed(
                tfeed.get("url"),
                tfeed.get("webhooks"),
                tfeed.get("include_retweets")
            )
            feed.load()
            timestamps.filter_out_old_posts(feed)
            Sender(feed).send()
            timestamps.update(feed)
        except Exception as e:
            tb = traceback.TracebackException.from_exception(e).stack[-1]
            err = f"❌ {e}\n-> Error occurred in file '{tb.filename}' at line {tb.lineno} in function '{tb.name}'\n-> While processing feed {tfeed['url']}"
            print(err)
            requests.post(CONFIG.get("error_webhook"), {"content": err})

    # rss
    for rfeed in CONFIG.get("rss_feeds", []):
        try:
            feed = RssFeed(
                rfeed.get("url"),
                rfeed.get("webhooks"),
                embed_color=rfeed.get("embed_color"),
                summarize=rfeed.get("summarize")
            )
            feed.load()
            timestamps.filter_out_old_posts(feed)
            Sender(feed).send_json()
            timestamps.update(feed)
        except Exception as e:
            tb = traceback.TracebackException.from_exception(e).stack[-1]
            err = f"❌ {e}\n-> Error occurred in file '{tb.filename}' at line {tb.lineno} in function '{tb.name}'\n-> While processing feed {tfeed['url']}"
            print(err)
            requests.post(CONFIG.get("error_webhook"), {"content": err})

    timestamps.write()

    END_TIME = time.time()
    print(f"Execution time: {round(END_TIME - START_TIME, 1)} seconds")


if __name__ == "__main__":
    main()
