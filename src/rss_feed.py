from feed import Feed
from html2text import html2text as html2md
from bs4 import BeautifulSoup as HtmlParser
from bs4.element import Tag


class RssFeed(Feed):
    def __init__(self, url, webhooks, embed_color):
        super().__init__(url, webhooks)
        self.embed_color = int(embed_color if embed_color is not None else "738adb", 16)

    def make_embeds(self):
        for item in reversed(self.feed_items[:5]):  # max items posted at once
            html = HtmlParser(item.description, "html.parser")

            # extract first image src from description (if any) - we pass it later as part of embed
            img_tag = html.find("img")
            img_src = img_tag.get("src") if isinstance(img_tag, Tag) else ""

            if item.media:
                img_src = item.media[0].get("url", img_src)

            # remove "http://" and "https://" from the link text
            # (discord does not support markdown links if their name contains http:// or https://)
            for link in html.find_all("a"):
                if link.text.find("http://") or link.text.find("https://"):
                    link.string = link.text.replace("http://", "").replace(
                        "https://", ""
                    )

            # remove certain html tags from description before transforming to markdown
            tags_to_remove = ["img"]
            for tag_name in tags_to_remove:
                for tag in html.find_all(tag_name):
                    tag.decompose()

            embed = [
                {
                    "type": "image",
                    "color": self.embed_color,
                    # ----------------------------------
                    "thumbnail": {"url": self.avatar_url},
                    "author": {"name": self.title, "url": self.link},
                    # ----------------------------------
                    "title": item.title,
                    "url": item.link,
                    "description": html2md(str(html), bodywidth=0),
                    "image": {"url": img_src},
                    "timestamp": str(item.pub_date),
                }
            ]

            self.new_feed_items.append(embed)

        return self
