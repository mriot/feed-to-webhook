import re


class FeedConfigError(Exception):
    """Exception raised for errors in the feed configuration."""

    def __init__(self, message, feed_config):
        super().__init__(message)
        self.feed_config = feed_config


def strip_protocol(string: str) -> str:
    """Removes all URL protocols from a string."""
    return re.sub(r"^[a-zA-Z]+://", "", string)
