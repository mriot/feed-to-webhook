import os
import yaml
import requests
from twitter_feed import twitter_feed
from rss_feed import rss_feed


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_dir, "config.yaml")
    feed_ts_path = os.path.join(script_dir, "feed_timestamps.yaml")
    new_feed_timestamps = {}

    # load config
    try:
        with open(config_path, "r") as config_file:
            config = yaml.safe_load(config_file)
    except FileNotFoundError:
        print("ERROR: config.yaml not found. Program will exit.")
        return 1

    # load timestamps
    with open(feed_ts_path, "a+") as timestamp_file:
        timestamp_file.seek(0)
        prev_feed_timestamps = yaml.safe_load(timestamp_file) or {}

    # twitter
    for tfeed in config["twitter_feeds"]:
        result = twitter_feed(tfeed, prev_feed_timestamps.get(tfeed["url"], None))
        new_feed_timestamps[tfeed["url"]] = result.get("last_timestamp")
        if (result.get("error")):
            requests.post(config["error_webhook"], {"content": f"Error {str(result['error'])} while fetching twitter feed {tfeed['url']}"})

    # rss
    for rfeed in config["rss_feeds"]:
        result = rss_feed(rfeed, prev_feed_timestamps.get(rfeed["url"], None))
        new_feed_timestamps[rfeed["url"]] = result.get("last_timestamp")
        if (result.get("error")):
            requests.post(config["error_webhook"], {"content": f"Error {str(result['error'])} while fetching rss feed {rfeed['url']}"})

    # update timestamps
    with open(feed_ts_path, "w") as timestamp_file:
        yaml.safe_dump(new_feed_timestamps, timestamp_file, sort_keys=False)


if __name__ == "__main__":
    main()
