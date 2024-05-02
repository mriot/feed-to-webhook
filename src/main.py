import requests
from sender import Sender
from rss_feed import RssFeed
from timestamps import Timestamps
from file_handler import JsonFile
import traceback
import time


def main():
    START_TIME = time.time()

    config = JsonFile("config.json", False).read()
    timestamps = Timestamps()
    sender = Sender()

    for feed_config in config.get("feeds", []):
        feed = RssFeed(
            feed_config.get("url"),
            feed_config.get("webhooks"),
            feed_config.get("embed_color"),
        )

        try:
            feed.load()
            feed.remove_old_posts(timestamps)
            timestamps.update(feed)

            if not feed.feed_items:
                continue

            feed.make_embeds()
            sender.add(feed)
        except Exception as e:
            tb = traceback.TracebackException.from_exception(e).stack[-1]
            err = f"❌ {e}\n-> Error occurred in file '{tb.filename}' at line {tb.lineno} in function '{tb.name}'"
            print(err)
            if errhook := config.get("error_webhook"):
                requests.post(errhook, {"content": err})

    sender.send_embeds()

    timestamps.write()

    END_TIME = time.time()
    print(f"Execution time: {round(END_TIME - START_TIME, 1)} seconds")


if __name__ == "__main__":
    main()
