import requests
from sender import Sender
from twitter_feed import TwitterFeed
from rss_feed import RssFeed
from timestamps import Timestamps
from file_handler import YamlFile


def main():
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
            print(e)
            requests.post(CONFIG.get("error_webhook"), {"content": f"Error {str(e)} while fetching twitter feed {tfeed['url']}"})

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
            print(e)
            requests.post(CONFIG.get("error_webhook"), {"content": f"Error {str(e)} while fetching RSS feed {rfeed['url']}"})

    timestamps.write()


if __name__ == "__main__":
    main()
