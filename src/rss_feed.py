from bs4 import BeautifulSoup
from bs4.element import Tag

from embed import Embed
from utils import strip_protocol
from feed import Feed


class RssFeed(Feed):
    def __init__(self, url, webhooks, embed_color):
        super().__init__(url, webhooks, embed_color)
        self.new_embedded_posts: list[Embed] = []

    def generate_embeds(self):
        for post in reversed(self.posts[:5]):
            desc_html = BeautifulSoup(post.post_description, "html.parser")

            # strip protocol from link-texts in the description - the actual link is kept as-is
            # (discord seems to not support markdown links if their name contains http or https)
            for link in desc_html.find_all("a"):
                # link.text concatenates the text from all child tags
                # link.string replaces the inner text of the a-tag (which clears all child tags)
                link.string = strip_protocol(link.text)

            # TODO - try to handle more media types
            # for now we just append the url of other media types to the description
            for media in post.post_media:
                if "image" not in media.get("type", ""):
                    desc_html.append(media.get("url", ""))

            self.new_embedded_posts.append(
                Embed()
                .add_title(post.post_title, post.post_link)
                .add_description(str(desc_html))
                .add_color(self.embed_color)
                .add_author(self.feed_title, self.feed_link, self.feed_avatar_url)
                .add_image(self._find_image(desc_html, post.post_media, post.post_content))
                .add_timestamp(post.post_pub_date)
                .add_footer(strip_protocol(self.feed_link))
            )

        return self.new_embedded_posts

    def _find_image(self, desc_html: BeautifulSoup, media: list, content: list) -> str:
        """Returns URL of the first image found in the post description, media or content tags"""
        if img_tag := desc_html.find("img"):
            if isinstance(img_tag, Tag):
                src = img_tag.get("src", "")
                if isinstance(src, str):
                    return src

        for item in media:
            if "image" in item.get("type", ""):
                return item.get("url", "")

        for item in content:
            if item.get("type") == "text/html":
                html = BeautifulSoup(item.value, "html.parser")
                if img_tag := html.find("img"):
                    if isinstance(img_tag, Tag):
                        src = img_tag.get("src", "")
                        if isinstance(src, str):
                            return src

        return ""
