import requests
from Sender import Sender
from feed import TwitterFeed
from timestamps import Timestamps
from twitter_feed import twitter_feed
from rss_feed import rss_feed
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
            if not timestamps.is_newer(feed):
                continue
            Sender(feed).send()
            print(feed.latest_timestamp)
            timestamps.update(url, feed.latest_timestamp)
        except Exception as e:
            requests.post(config["error_webhook"], {"content": f"Error {str(e)} while fetching twitter feed {tfeed['url']}"})

    # rss
    # for rfeed in config.get("rss_feeds", []):
    #     result = rss_feed(rfeed, prev_feed_timestamps.get(rfeed["url"], None))
    #     new_feed_timestamps[rfeed["url"]] = result.get("last_timestamp")
    #     if (result.get("error")):
    #         requests.post(config["error_webhook"], {"content": f"Error {str(result['error'])} while fetching rss feed {rfeed['url']}"})

    timestamps.write()


if __name__ == "__main__":
    main()
