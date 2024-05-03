from feed import Feed
from html2text import html2text as html2md
from bs4 import BeautifulSoup as HtmlParser
from bs4.element import Tag


class RssFeed(Feed):
    def __init__(self, url, webhooks, embed_color):
        super().__init__(url, webhooks)
        self.embed_color = int(embed_color if embed_color is not None else "738adb", 16)

    def make_embeds(self):
        for item in reversed(self.feed_items[:5]):  # max items posted at once per feed
            desc_html = HtmlParser(item.description, "html.parser")
            desc_html = self._sanitize_links(desc_html)

            # TODO - this needs some work
            for media in item.media:
                if "image" not in media.get("type", ""):
                    desc_html.append(media.get("url", ""))

            embed = [
                {
                    "type": "image",
                    "color": self.embed_color,
                    "author": {
                        "name": self.title,
                        "url": self.link,
                        "icon_url": self.avatar_url,
                    },
                    "title": item.title or "Link to post",
                    "url": item.link,
                    "description": self._get_description(desc_html),
                    "image": {"url": self._get_teaser_image(item.media, desc_html, item.content)},
                    "timestamp": str(item.pub_date),
                }
            ]

            self.new_feed_items.append(embed)

        return self

    def _get_teaser_image(self, media, desc_html, content):
        try:
            if img_tag := desc_html.find("img"):
                if isinstance(img_tag, Tag):
                    return img_tag.get("src", "")

            for item in media:
                if "image" in item.get("type", ""):
                    return item.get("url", "")

            for item in content:
                if item.get("type") == "text/html":
                    html = HtmlParser(item.value, "html.parser")
                    if img_tag := html.find("img"):
                        if isinstance(img_tag, Tag):
                            return img_tag.get("src", "")
        except Exception as e:
            print("Failed to get teaser image:", e)
            return ""

    def _get_description(self, desc):
        description = str(desc)

        if len(description) >= 750:
            description = description[:750]
            description += "..."
            description += f"\n[Read more]({self.link})"

        return html2md(str(description), bodywidth=0)

    def _sanitize_links(self, html):
        # remove "http://" and "https://" from the link text
        # (discord does not support markdown links if their name contains http:// or https://)
        for link in html.find_all("a"):
            if link.text.find("http://") or link.text.find("https://"):
                link.string = link.text.replace("http://", "").replace("https://", "")
        return html

    def _sanitize_html(self, html):
        # remove certain html tags from description before transforming to markdown
        tags_to_remove = ["img"]
        for tag_name in tags_to_remove:
            for tag in html.find_all(tag_name):
                tag.decompose()
        return html
