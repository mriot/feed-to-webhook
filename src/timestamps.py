from datetime import datetime

from dateutil import tz
from dateutil.parser import parse

from file_handler import JsonFile


class Timestamps:
    def __init__(self):
        self._timestamps_file = JsonFile("timestamps.json")
        self._timestamps = self._timestamps_file.read() or {}

    def get_last_post_date(self, url) -> datetime:
        timestamp = self._timestamps.get(url, {}).get("last_post")

        if not timestamp:
            # if there is no timestamp, we likely haven't fetched this feed before.
            # nothing will be posted rn but an entry will be added to the timestamps file.
            # return current time to ensure that all posts are filtered out.
            return datetime.now(tz=tz.UTC)

        return parse(timestamp)

    def get_etag(self, url) -> str:
        return self._timestamps.get(url, {}).get("etag")

    def get_last_modified(self, url) -> str:
        return self._timestamps.get(url, {}).get("last_modified")

    def remove_unconfigured_entries(self, feed_urls):
        for url in list(self._timestamps.keys()):
            if url not in feed_urls:
                del self._timestamps[url]

    def update(self, url, timestamp, etag=None, last_modified=None):
        self._timestamps[url] = {"last_post": timestamp.isoformat()}

        if etag:
            self._timestamps[url]["etag"] = etag
        if last_modified:
            self._timestamps[url]["last_modified"] = last_modified

    def write(self):
        self._timestamps_file.write(self._timestamps)
