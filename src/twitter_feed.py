from urllib.parse import urlparse, urlunparse
import xml.etree.ElementTree as ET
from feed import Feed, FeedItem


class TwitterFeed(Feed):
    def __init__(self, url, webhooks, include_retweets=True):
        super().__init__(url, webhooks)
        self.include_retweets = include_retweets

    def prepare_content(self):
        feed_owner = self.feed_root.get("author", "`[not found]`")  # -> username / @username
        # feed_owner_accountname = feed_owner.split(" / ")[-1] if feed_owner else ""  # -> @username
        feed_owner_link = f"https://twitter.com/{feed_owner.replace('@', '')}" if feed_owner else ""

        for item in self.feed_items[:5]:
            # post_author = item.root.findtext("dc:creator", default="", namespaces={"dc": "http://purl.org/dc/elements/1.1/"})  # @username
            post_author = item.item_root.get("author")  # @username
            post_author_url = f"https://twitter.com/{post_author.replace('@', '')}" if post_author else ""
            post_url = item.item_root.get("link", "")
            post_date = item.get_pubdate().strftime("%b %d, %Y %H:%M:%S")
            is_retweet = feed_owner.find(post_author) == -1 if feed_owner and post_author else False

            if is_retweet and not self.include_retweets:
                continue

            # enables an embed view for twitter posts (which is disabled for some reason)
            post_url = urlunparse(urlparse(post_url)._replace(netloc="fxtwitter.com"))

            if is_retweet:
                output = f"♻️ [{feed_owner}](<{feed_owner_link}>) retweeted [{post_author}](<{post_author_url}>)\n{post_url}"
            else:
                output = f"📢 [{feed_owner}](<{feed_owner_link}>) tweeted at {post_date} \n{post_url}"

            self.final_items_to_be_posted.append(output)

        return self
