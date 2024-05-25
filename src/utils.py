import re
from urllib.parse import urlparse


def strip_protocol(string: str) -> str:
    """Removes all URL protocols from a string."""
    return re.sub(r"^[a-zA-Z]+://", "", string)


def get_favicon_url(url: str) -> str:
    """Returns the URL of the favicon for a given website."""
    # sadly, the duckduckgo API isn't as reliable as the google one
    return f"https://www.google.com/s2/favicons?domain={urlparse(url).hostname}&sz=128"
