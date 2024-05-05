from datetime import datetime
from html2text import html2text


class Embed:
    def __init__(self):
        self.embed_config: dict = {"type": "image"}

        self.post_title: str = ""
        self.post_url: str = ""
        self.description: str = ""

        self.author_name: str = ""
        self.author_url: str = ""
        self.author_icon_url: str = ""

        self.image_url: str = ""
        self.timestamp: str = ""
        self.footer: str = ""
        self.embed_color: str = ""

    def add_title(self, title: str, url: str = ""):
        self.post_title = title
        self.post_url = url
        return self

    def add_description(self, description: str):
        desc = description

        # truncate description if it exceeds 750 characters
        if len(desc) >= 750 and self.post_url:
            desc = desc[:750]
            desc += f"... <a href='{self.post_url}'>Read more</a>"

        # add 'link to post' if no title is set
        if not self.post_title and self.post_url:
            desc += f"<p><a href='{self.post_url}'>Link to post</a></p>"

        self.description = html2text(str(desc), bodywidth=0)
        return self

    def add_color(self, color: int | str):
        self.embed_color = str(color)
        return self

    def add_author(self, name: str, url: str = "", icon_url: str = ""):
        self.author_name = name
        self.author_url = url
        self.author_icon_url = icon_url
        return self

    def add_image(self, url: str):
        self.image_url = url
        return self

    def add_timestamp(self, timestamp: str | datetime):
        self.timestamp = str(timestamp)
        return self

    def add_footer(self, text: str):
        self.footer = text
        return self

    def build(self) -> list[dict]:
        self.embed_config["author"] = {
            "name": self.author_name,
            "url": self.author_url,
            "icon_url": self.author_icon_url,
        }
        self.embed_config["title"] = self.post_title
        self.embed_config["url"] = self.post_url
        self.embed_config["description"] = self.description
        self.embed_config["image"] = {"url": self.image_url}
        self.embed_config["timestamp"] = self.timestamp
        self.embed_config["footer"] = {"text": self.footer}
        self.embed_config["color"] = self.embed_color

        return [self.embed_config]
