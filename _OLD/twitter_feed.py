from urllib.parse import urlparse, urlunparse
from feed import Feed
from html2text import html2text
from bs4 import BeautifulSoup


class TwitterFeed(Feed):
    def __init__(self, url, webhooks, embed_color, exclude_retweets, override_domain):
        super().__init__(url, webhooks)
        self.embed_color = int(embed_color if embed_color is not None else "1DA1F2", 16)
        self.exclude_retweets = exclude_retweets
        self.override_domain = "twitter.com" if override_domain is None else override_domain

    def make_embeds(self):
        feed_owner = self.feed_data_dict.feed.get("title", "[unknown]")  # -> username / @username
        feed_owner_accountname = feed_owner.split(" / ")[-1]  # -> @username
        feed_owner_avatar = self.feed_data_dict.feed.get("image", {}).get("url")
        feed_owner_link = self.feed_data_dict.feed.get("link")
        if self.override_domain:
            feed_owner_link = urlunparse(urlparse(feed_owner_link)._replace(netloc=self.override_domain))

        for item in self.feed_items[:5]:
            post_author = item.item_root.get("author")  # @username
            post_description = item.item_root.get("description")
            is_retweet = feed_owner.find(post_author) == -1
            post_url = item.item_root.get("link", "")
            if self.override_domain:
                post_url = urlunparse(urlparse(post_url)._replace(netloc=self.override_domain))

            if is_retweet and self.exclude_retweets:
                continue

            soup = BeautifulSoup(post_description, "html.parser")

            # extract first image src from description - we pass it later as part of embed
            img_tag = soup.find("img")
            img_src = img_tag["src"] if img_tag else ""

            # replace links from the current nitter instance in description
            if self.override_domain:
                feed_domain = urlparse(self.feed_data_dict.feed.get("link")).netloc
                for a_tag in soup.find_all("a"):
                    url = urlparse(a_tag["href"])
                    text = a_tag.text
                    if url.netloc == feed_domain:
                        a_tag["href"] = urlunparse(url._replace(netloc=self.override_domain))
                        a_tag.string = text.replace(url.netloc, self.override_domain)

            # remove certain tags from description before transforming to markdown
            # <hr> seems to be used in a 'quoting tweet'
            tags_to_remove = ["img", "hr"]
            for tag_name in tags_to_remove:
                for tag in soup.find_all(tag_name):
                    tag.decompose()

            embed = [
                {
                    "type": "image",  # required for images without extension ¯\_(ツ)_/¯
                    "color": self.embed_color,
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
