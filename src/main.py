import requests
from Sender import Sender
from feed import TwitterFeed
from twitter_feed import twitter_feed
from rss_feed import rss_feed
from file_handler import YamlFile


def main():
    config = YamlFile("config.yaml", False).read()

    timestamps_file = YamlFile("feed_timestamps.yaml")
    prev_feed_timestamps = timestamps_file.read() or {}
    new_feed_timestamps = {}

    # twitter
    for tfeed in config.get("twitter_feeds", []):
        try:
            url, webhooks, include_retweets = tfeed.get("url"), tfeed.get("webhooks"), tfeed.get("include_retweets")
            feed = TwitterFeed(url, webhooks, include_retweets)
            Sender(feed).send()
            # result = twitter_feed(tfeed, prev_feed_timestamps.get(tfeed["url"], None))
            # new_feed_timestamps[tfeed["url"]] = result.get("last_timestamp")
        except Exception as e:
            requests.post(config["error_webhook"], {"content": f"Error {str(e)} while fetching twitter feed {tfeed['url']}"})

    # rss
    for rfeed in config.get("rss_feeds", []):
        result = rss_feed(rfeed, prev_feed_timestamps.get(rfeed["url"], None))
        new_feed_timestamps[rfeed["url"]] = result.get("last_timestamp")
        if (result.get("error")):
            requests.post(config["error_webhook"], {"content": f"Error {str(result['error'])} while fetching rss feed {rfeed['url']}"})

    # update timestamps
    timestamps_file.write(new_feed_timestamps)


if __name__ == "__main__":
    main()
