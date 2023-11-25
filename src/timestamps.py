from file_handler import YamlFile
from dateutil.parser import parse
from datetime import datetime


class Timestamps:
    def __init__(self):
        self._timestamps_file = YamlFile("feed_timestamps.yaml")
        self._timestamps = self._timestamps_file.read() or {}

    def get(self, url):
        timestamp = self._timestamps.get(url)
        if not timestamp:
            # only save latest feed timestamp on first run; don't post anything
            return datetime.now()
        return parse(timestamp)

    def update(self, feed):
        self._timestamps[feed.url] = feed.latest_timestamp

    def write(self):
        self._timestamps_file.write(self._timestamps)

    def filter_out_old_posts(self, feed):
        feed.feed_items = [post for post in feed.feed_items if post.get_pubdate() > self.get(feed.url)]
