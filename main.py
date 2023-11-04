import requests
import json
from urllib.parse import urlparse, urlunparse
import xml.etree.ElementTree as ET


with open("config.json", "r") as f:
    config = json.load(f)


def fx_twitter_url(link):
    parsed_url = urlparse(link)
    modified_url = parsed_url._replace(netloc="fxtwitter.com")
    fixed_url = urlunparse(modified_url)
    return fixed_url


def main():
    for feed in config["feeds"]:
        response = requests.get(feed["url"], headers={"User-Agent": "Hi, I am a bot!"})

        if (response.status_code == 200):
            root = ET.fromstring(response.content.decode("utf-8"))
            items = root.findall("channel/item")

            last_item_date = feed.get("last_item_date")
            if last_item_date and last_item_date == items[0].find("pubDate").text:
                continue

            feed["last_item_date"] = items[0].find("pubDate").text

            with open("config.json", "w") as f:
                json.dump(config, f, indent=2)

            link = items[0].find("link").text

            if feed.get("is_twitter_feed"):
                link = fx_twitter_url(link)

            requests.post(feed["webhook"], {"content": link})
        else:
            requests.post(config["debug"]["webhook"], {
                "content": f"Error {str(response.status_code)} while fetching feed {feed['url']}"
            })

if __name__ == "__main__":
    main()