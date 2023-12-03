from urllib.parse import urlparse, urlunparse
from feed import Feed
from html2text import html2text
from bs4 import BeautifulSoup


class TwitterFeed(Feed):
    def __init__(self, url, webhooks, include_retweets=True):
        super().__init__(url, webhooks)
        self.include_retweets = include_retweets

    def prepare_content(self):
        feed_owner = self.feed_data_dict.feed.get("title", "[unknown]")  # -> username / @username
        feed_owner_accountname = feed_owner.split(" / ")[-1]  # -> @username
        feed_owner_link = f"https://twitter.com/{feed_owner_accountname.replace('@', '')}"
        feed_owner_avatar = self.feed_data_dict.feed.get("image", {}).get("url")
        feed_color = int(str(self.feed_data_dict.feed.get("embed_color") or "1DA1F2"), 16)

        for item in self.feed_items[:5]:
            post_author = item.item_root.get("author")  # @username
            # post_author_url = f"https://twitter.com/{post_author.replace('@', '')}" if post_author else ""
            post_url = item.item_root.get("link", "")
            post_url = urlunparse(urlparse(post_url)._replace(netloc="twitter.com"))
            post_description = item.item_root.get("description")
            is_retweet = feed_owner.find(post_author) == -1 if feed_owner and post_author else False

            if is_retweet and not self.include_retweets:
                continue

            # extract image(s) from description - we pass them as part of embed
            soup = BeautifulSoup(post_description, "html.parser")
            img_tags = soup.find_all("img")
            img_src = img_tags[0]["src"] if img_tags else ""

            # remove all images from text
            for img in img_tags:
                img.decompose()

            embed = [
                {
                    "type": "article",
                    "color": feed_color,
                    "author": {
                        "name": feed_owner_accountname,
                        "url": feed_owner_link
                    },
                    "thumbnail": {
                        "url": feed_owner_avatar
                    },
                    "title": f"Tweet by {post_author}",
                    "url": post_url,
                    "description": html2text(str(soup)),
                    "fields": [
                        {
                            "name": "",
                            "value": f"———\nretweeted by {feed_owner_accountname}" if is_retweet else "",
                        }
                    ],
                    "image": {
                        "url": img_src
                    },
                    "timestamp": str(item.get_pubdate()),
                }
            ]

            self.final_items_to_be_posted.append(embed)

        return self
