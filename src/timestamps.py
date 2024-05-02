from file_handler import JsonFile
from dateutil.parser import parse
from dateutil import tz
from datetime import datetime


class Timestamps:
    def __init__(self):
        self._timestamps_file = JsonFile("feed_timestamps.json")
        self._timestamps = self._timestamps_file.read() or {}

    def get(self, url):
        timestamp = self._timestamps.get(url)

        if not timestamp:
            # if there is no timestamp, we likely haven't fetched this feed before
            # so we return the current time to simulate that we're up to date
            return datetime.now(tz=tz.UTC)

        return parse(timestamp)

    def update(self, feed):
        self._timestamps[feed.url] = feed.latest_timestamp.isoformat()

    def write(self):
        self._timestamps_file.write(self._timestamps)
