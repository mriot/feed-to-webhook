from file_handler import YamlFile


class Timestamps:
    def __init__(self):
        self._timestamps_file = YamlFile("feed_timestamps.yaml")
        self._timestamps = self._timestamps_file.read() or {}
        # self._new_timestamps = {}

    def get(self, url):
        return self._timestamps.get(url)

    def update(self, url, timestamp):
        self._timestamps[url] = timestamp

    def write(self):
        self._timestamps_file.write(self._timestamps)

    def is_newer(self, feed):
        url = feed.url
        timestamp = self.get(url)
        if not timestamp:
            return True
        return feed.latest_timestamp > timestamp  # a more recent date is considered greater
