import dateutil.parser
import feedparser


class Feed:
    def __init__(self, url, webhooks, embed_color=None):
        self.url = url
        self.webhooks = webhooks
        self.embed_color = int(embed_color if embed_color is not None else "738adb", 16)

        # download and parse feed
        feed_data = feedparser.parse(self.url)

        if feed_data.get("bozo_exception"):
            raise Exception(
                f"Failed to parse feed from URL {self.url}\n{feed_data.get('bozo_exception')}"
            )

        channel = feed_data.get("feed")  # information about the feed itself
        entries = feed_data.get("entries")  # data about the actual posts

        if not entries:
            raise Exception(f"Failed to extract feed items from {self.url}")

        self.feed_title = channel.get("title", "Untitled")
        self.feed_description = channel.get("description", "")
        self.feed_link = channel.get("link", "")
        self.feed_avatar_url = channel.get("image", {}).get("url", "")
        self.feed_gernerator = channel.get("generator", "")

        self.posts = [Post(item) for item in entries[:25]]  # upper limit just in case
        self.latest_timestamp = max((item.post_pub_date) for item in self.posts)

        self.new_embedded_posts = []  # populated by make_embeds()

    def remove_old_posts(self, timestamp):
        self.posts = [post for post in self.posts if post.post_pub_date > timestamp]


class Post:
    def __init__(self, item):
        self.post_link = item.get("link", "")
        self.post_title = item.get("title", "")
        self.post_pub_date = dateutil.parser.parse(item.get("published"))
        self.post_author = item.get("author", "")
        self.post_description = item.get("description", "")
        self.post_media = item.get("media_content", [])
        self.post_content = item.get("content", [])
