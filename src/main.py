import os
import yaml
import requests
from twitter_feed import twitter_feed
from rss_feed import rss_feed


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_dir, "config.yaml")
    feed_ts_path = os.path.join(script_dir, "feed_timestamps.yaml")

    config_file = open(config_path, "r")
    config = yaml.safe_load(config_file)

    with open(feed_ts_path, "r") as f:
        prev_feed_timestamps = yaml.safe_load(f)
        if not prev_feed_timestamps:
            prev_feed_timestamps = {}

    new_feed_timestamps = {}

    # twitter
    for i, tfeed in enumerate(config["twitter_feeds"]):
        result = twitter_feed(tfeed, prev_feed_timestamps.get(tfeed["url"], None))
        if (result.get("error")):
            requests.post(config["error_webhook"], {"content": f"Error {str(result['error'])} while fetching twitter feed {tfeed['url']}"})
        # else:
        #     config["twitter_feeds"][i]["last_item_date"] = result["last_item_date"]
        new_feed_timestamps[tfeed["url"]] = result.get("last_timestamp")

    # rss
    for i, rfeed in enumerate(config["rss_feeds"]):
        result = rss_feed(rfeed, prev_feed_timestamps.get(rfeed["url"], None))
        if (result.get("error")):
            requests.post(config["error_webhook"], {"content": f"Error {str(result['error'])} while fetching rss feed {rfeed['url']}"})
        # else:
        #     config["rss_feeds"][i]["last_item_date"] = result["last_item_date"]
        new_feed_timestamps[rfeed["url"]] = result.get("last_timestamp")

    # override config file
    # config_file.seek(0)
    # config_file.truncate()
    # yaml.safe_dump(config, config_file, sort_keys=False)

    config_file.close()

    with open(feed_ts_path, "w") as f:
        yaml.safe_dump(new_feed_timestamps, f, sort_keys=False)


if __name__ == "__main__":
    main()
