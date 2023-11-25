from urllib.parse import urlparse, urlunparse
import xml.etree.ElementTree as ET
from feed import Feed, FeedItem


class TwitterFeed(Feed):
    def __init__(self, url, webhooks, include_retweets=True):
        super().__init__(url, webhooks)
        self.include_retweets = include_retweets

    def sanitize(self):
        if not self._feed_root or not isinstance(self._feed_root, ET.Element):
            raise Exception("Root element not found")

        items = self.feed_items

        # TODO: error handling if name not found
        feed_owner = self._feed_root.findtext("channel/title") or "Unknown"  # username / @username
        feed_owner_accountname = feed_owner.split(" / ")[-1]  # @username
        feed_owner_link = "https://twitter.com/" + feed_owner_accountname.replace("@", "")

        for item in reversed(items[:5]):
            post_author = item.root.findtext("dc:creator", default="", namespaces={"dc": "http://purl.org/dc/elements/1.1/"})  # @username
            post_author_link = "https://twitter.com/" + post_author.replace("@", "")
            post_url = item.root.findtext("link")
            is_retweet = feed_owner.find(post_author) == -1

            if is_retweet and not self.include_retweets:
                continue

            post_url = urlunparse(urlparse(post_url)._replace(netloc="fxtwitter.com"))

            if is_retweet:
                output = f"♻️ [{feed_owner_accountname}](<{feed_owner_link}>) retweeted [{post_author}](<{post_author_link}>)\n{post_url}"
            else:
                output = f"📢 [{feed_owner_accountname}](<{feed_owner_link}>) tweeted \n{post_url}"

            self.content.append(output)

        return self
