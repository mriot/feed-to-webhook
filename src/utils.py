import json
import re
import traceback

import requests

from file_handler import JsonFile


def strip_protocol(string: str) -> str:
    """Removes all URL protocols from a string."""
    return re.sub(r"^[a-zA-Z]+://", "", string)


class FeedConfigError(Exception):
    """Exception raised for errors in the feed configuration."""

    def __init__(self, title, feed_config=None):
        super().__init__(title)
        self.feed_config = feed_config


class WebhookHTTPError(requests.HTTPError):
    """Exception raised for errors in the webhook HTTP response."""

    def __init__(self, title, body, response=None):
        super().__init__(title)
        self.body = body
        self.response = response


def handle_error_reporting(err: Exception) -> None:
    """Handles error reporting and formatting."""
    tb = traceback.TracebackException.from_exception(err).stack[-1]
    err_msg = f"Error raised in '{tb.filename}' at line {tb.lineno} in function '{tb.name}'"

    if isinstance(err, FeedConfigError):
        err_msg = f"```{json.dumps(err.feed_config, indent=2)}``` \n {err_msg}"

    if isinstance(err, WebhookHTTPError):
        err_msg = f"{err.body} \n ```{err.response}``` \n {err_msg}"

    print(f"ERROR: {err}\n{err_msg}")

    # also send the error to the error webhook if it is configured
    if errhook := JsonFile("config.json", False).read().get("error_webhook"):
        res = requests.post(
            errhook,
            json={
                "embeds": [
                    {
                        "title": f"ERROR:  {err}",
                        "description": err_msg,
                        "color": 16711680,
                    }
                ]
            },
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        if res.status_code >= 300:
            print(f"Error webhook returned status code {res.status_code} ({res.reason})\n")
    else:
        print("Warning: No error webhook configured")
