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

    # new_items = []

    # TODO sender function
    # - gets list of feed objects (embeds are already prepared and stored in feed object)
    # - extract embeds from all feeds and sort them by timestamp (store them in a list)
    # - update timestamps (or do it in main() ?)
    # - send embeds to webhooks (add rate limit handling)

    # twitter
    for tfeed in CONFIG.get("twitter_feeds", []):
        try:
            feed = TwitterFeed(
                tfeed.get("url"),
                tfeed.get("webhooks"),
                tfeed.get("embed_color"),
                tfeed.get("exclude_retweets"),
                tfeed.get("override_domain"),
            )
            feed.load()  # TODO automatically load feed upon creation
            feed.remove_old_posts(timestamps)  # REPLACED: timestamps.filter_out_old_posts(feed)
            # TODO we dont need to continue if there are no new posts
            feed.prepare_content()  # TODO rename to make_embeds()
            # TODO store feed object in a list
            # new_items.extend(feed.final_items_to_be_posted) # we should not need this anymore
            # Sender(feed).send_json() # TODO make function, drop class
            # timestamps.update(feed) # will be handled by sender function
        except Exception as e:
            tb = traceback.TracebackException.from_exception(e).stack[-1]
            err = f"❌ {e}\n-> Error occurred in file '{tb.filename}' at line {tb.lineno} in function '{tb.name}'"
            print(err)
            requests.post(CONFIG.get("error_webhook"), {"content": err})

    # rss
    for rfeed in CONFIG.get("rss_feeds", []):
        try:
            feed = RssFeed(
                rfeed.get("url"),
                rfeed.get("webhooks"),
                rfeed.get("embed_color"),
                rfeed.get("summarize")  # TODO: implement
            )
            feed.load()
            timestamps.filter_out_old_posts(feed)
            Sender(feed).send_json()
            timestamps.update(feed)
        except Exception as e:
            tb = traceback.TracebackException.from_exception(e).stack[-1]
            err = f"❌ {e}\n-> Error occurred in file '{tb.filename}' at line {tb.lineno} in function '{tb.name}'"
            print(err)
            requests.post(CONFIG.get("error_webhook"), {"content": err})

    # timestamps.write()

    # print(new_items)
    # print(new_items[0][0].get("title"))
    # new_items.sort(key=lambda x: x[0]["timestamp"])
    # print(new_items)

    END_TIME = time.time()
    print(f"Execution time: {round(END_TIME - START_TIME, 1)} seconds")


if __name__ == "__main__":
    main()
