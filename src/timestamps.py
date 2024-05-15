from datetime import datetime

from dateutil import tz
from dateutil.parser import parse

from file_handler import JsonFile


class Timestamps:
    def __init__(self):
        self._timestamps_file = JsonFile("feed_timestamps.json")
        self._timestamps = self._timestamps_file.read() or {}

    def get(self, url):
        timestamp = self._timestamps.get(url)

        if not timestamp:
            # if there is no timestamp, we likely haven't fetched this feed before.
            # nothing will be posted rn but an entry will be added to the timestamps file.
            # return current time to ensure that all posts are filtered out.
            return datetime.now(tz=tz.UTC)

        return parse(timestamp)

    def remove_unconfigured_entries(self, feed_urls):
        for url in list(self._timestamps.keys()):
            if url not in feed_urls:
                del self._timestamps[url]

    def update(self, url, timestamp):
        self._timestamps[url] = timestamp.isoformat()

    def write(self):
        self._timestamps_file.write(self._timestamps)
