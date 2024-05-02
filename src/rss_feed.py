from feed import Feed
from html2text import html2text
from bs4 import BeautifulSoup


class RssFeed(Feed):
    def __init__(self, url, webhooks, embed_color):
        super().__init__(url, webhooks)
        self.embed_color = int(embed_color if embed_color is not None else "738adb", 16)

    def make_embeds(self):
        d = self.feed_data_dict
        avatar = self.feed_data_dict.feed.get("image", {}).get("url")

        for item in self.feed_items[:5]:
            soup = BeautifulSoup(item.item_root.get("description"), "html.parser")

            # extract first image src from description - we pass it later as part of embed
            img_tag = soup.find("img")
            img_src = img_tag["src"] if img_tag else ""

            # remove certain html tags from description before transforming to markdown
            tags_to_remove = ["img"]
            for tag_name in tags_to_remove:
                for tag in soup.find_all(tag_name):
                    tag.decompose()

            embed = [
                {
                    "type": "image",  # required for images without extension ¯\_(ツ)_/¯
                    "color": self.embed_color,
                    "author": {"name": d.feed.get("title"), "url": d.feed.get("link")},
                    "thumbnail": {"url": avatar},
                    "title": item.item_root.get("title"),
                    "url": item.item_root.get("link"),
                    "description": html2text(str(soup)),
                    "image": {"url": img_src or item.item_root.get("enclosure")},
                    "timestamp": str(item.get_pubdate()),
                }
            ]

            self.new_feed_items.append(embed)

        return self
