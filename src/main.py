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
    except Exception as e:
        tb = traceback.TracebackException.from_exception(e).stack[-1]
        err = f"❌ {e}\n-> Error occurred in file '{tb.filename}' at line {tb.lineno} in function '{tb.name}'"
        print(err)

        if errhook := JsonFile("config.json", False).read().get("error_webhook"):
            requests.post(errhook, {"content": f"❌ {e}"})
