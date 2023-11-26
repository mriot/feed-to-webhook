import requests
from Sender import Sender
from twitter_feed import TwitterFeed
from rss_feed import RssFeed
from timestamps import Timestamps
from file_handler import YamlFile


def main():
    config = YamlFile("config.yaml", False).read()
    timestamps = Timestamps()

    # twitter
    for tfeed in config.get("twitter_feeds", []):
        try:
            url, webhooks, include_retweets = tfeed.get("url"), tfeed.get("webhooks"), tfeed.get("include_retweets")
            feed = TwitterFeed(url, webhooks, include_retweets)
            feed.load()
            timestamps.filter_out_old_posts(feed)
            Sender(feed).send()
            timestamps.update(feed)
        except Exception as e:
            print(e)
            requests.post(config["error_webhook"], {"content": f"Error {str(e)} while fetching twitter feed {tfeed['url']}"})

    # rss
    for rfeed in config.get("rss_feeds", []):
        try:
            url, webhooks, summarize = rfeed.get("url"), rfeed.get("webhooks"), rfeed.get("summarize")
            feed = RssFeed(url, webhooks, summarize)
            feed.load()
            timestamps.filter_out_old_posts(feed)
            Sender(feed).send_json()
            timestamps.update(feed)
        except Exception as e:
            print(e)
            requests.post(config["error_webhook"], {"content": f"Error {str(e)} while fetching RSS feed {rfeed['url']}"})

    timestamps.write()


if __name__ == "__main__":
    main()
