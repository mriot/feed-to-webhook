from file_handler import YamlFile
from dateutil.parser import parse


class Timestamps:
    def __init__(self):
        self._timestamps_file = YamlFile("feed_timestamps.yaml")
        self._timestamps = self._timestamps_file.read() or {}

    def get(self, url):
        timestamp = self._timestamps.get(url)
        print(timestamp)
        if not timestamp:
            return None
        return parse(timestamp)

    def update(self, url, timestamp):
        self._timestamps[url] = timestamp

    def write(self):
        self._timestamps_file.write(self._timestamps)

    def check_for_new_posts(self, feed):
        # TODO: cant compare to none type
        new_posts = [post for post in feed.feed_items if post.get_pubdate() > self.get(feed.url)]
        print(feed.feed_items, new_posts)
        feed.feed_items = new_posts

    def is_newer(self, feed):
        url = feed.url
        timestamp = self.get(url)
        if not timestamp:
            return True
        return feed.latest_timestamp > timestamp  # a more recent date is considered greater
