import os
import yaml
import requests
from twitter_feed import twitter_feed
from rss_feed import rss_feed


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_dir, "config.yaml")

    config_file = open(config_path, "r+")
    config = yaml.safe_load(config_file)

    # twitter
    for i, tfeed in enumerate(config["twitter_feeds"]):
        result = twitter_feed(tfeed)  # return error or last item date
        if (result.get("error")):
            requests.post(config["error_webhook"], {"content": f"Error {str(result['error'])} while fetching twitter feed {tfeed['url']}"})
        else:
            config["twitter_feeds"][i]["last_item_date"] = result["last_item_date"]

    # rss
    for i, rfeed in enumerate(config["rss_feeds"]):
        result = rss_feed(rfeed)  # return error or last item date
        if (result.get("error")):
            requests.post(config["error_webhook"], {"content": f"Error {str(result['error'])} while fetching rss feed {rfeed['url']}"})
        else:
            config["rss_feeds"][i]["last_item_date"] = result["last_item_date"]

    # override config file
    config_file.seek(0)
    config_file.truncate()
    yaml.safe_dump(config, config_file, sort_keys=False)

    config_file.close()


if __name__ == "__main__":
    main()
