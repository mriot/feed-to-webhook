from file_handler import YamlFile
from dateutil.parser import parse
from dateutil import tz
from datetime import datetime


class Timestamps:
    def __init__(self):
        self._timestamps_file = YamlFile("feed_timestamps.yaml")
        self._timestamps = self._timestamps_file.read() or {}

    def get(self, url):
        timestamp = self._timestamps.get(url)
        if not timestamp:
            # only save latest feed timestamp on first run; don't post anything
            return datetime.now(tz=tz.UTC)
        return parse(timestamp)

    def update(self, feed):
        self._timestamps[feed.url] = feed.latest_timestamp

    def write(self):
        self._timestamps_file.write(self._timestamps)
