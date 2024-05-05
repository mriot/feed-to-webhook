from feed import Feed
from html2text import html2text
from bs4 import BeautifulSoup
from bs4.element import Tag
import utils


class RssFeed(Feed):
    def __init__(self, url, webhooks, embed_color):
        super().__init__(url, webhooks, embed_color)

    def make_embeds(self):
        for post in reversed(self.posts[:5]):
            desc_html = BeautifulSoup(post.post_description, "html.parser")

            # strip protocol from link-texts in the description - the actual link is kept as-is
            # (discord seems to not support markdown links if their name contains http:// or https://)
            for link in desc_html.find_all("a"):
                # link.text concatenates text from all child tags whereas
                # link.string could return None if there are multiple child tags
                link.string = utils.strip_protocol(link.text)

            # TODO - try to handle more media types
            # for now we just append the url of other media types to the description
            for media in post.post_media:
                if "image" not in media.get("type", ""):
                    desc_html.append(media.get("url", ""))

            embed = [
                {
                    "type": "image",
                    "color": self.embed_color,
                    "author": {
                        "name": self.feed_title,
                        "url": self.feed_link,
                        "icon_url": self.feed_avatar_url,
                    },
                    "title": post.post_title,
                    "url": post.post_link,
                    "description": self._format_description(desc_html, post),
                    "image": {
                        "url": self._extract_teaser_image(
                            post.post_media, desc_html, post.post_content
                        )
                    },
                    "timestamp": str(post.post_pub_date),
                    "footer": {
                        "text": utils.strip_protocol(self.feed_link),
                    },
                }
            ]

            self.new_embedded_posts.append(embed)

    def _extract_teaser_image(self, media, desc_html, content):
        if img_tag := desc_html.find("img"):
            if isinstance(img_tag, Tag):
                return img_tag.get("src", "")

        for item in media:
            if "image" in item.get("type", ""):
                return item.get("url", "")

        for item in content:
            if item.get("type") == "text/html":
                html = BeautifulSoup(item.value, "html.parser")
                if img_tag := html.find("img"):
                    if isinstance(img_tag, Tag):
                        return img_tag.get("src", "")

        return ""

    def _format_description(self, post_desc, post):
        description = str(post_desc)

        if len(description) >= 750 and post.post_link:
            description = description[:750]
            description += f"... <a href='{post.post_link}'>Read more</a>"

        if not post.post_title and post.post_link:
            description += f"<p><a href='{post.post_link}'>Link to post</a></p>"

        return html2text(str(description), bodywidth=0)
