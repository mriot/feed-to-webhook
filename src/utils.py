import json
import logging
import re
import traceback
from os import path
from typing import Optional
from urllib.parse import urlparse

import requests

from file_handler import JsonFile


def setup_logging():
    logging.basicConfig(
        filename=path.join(path.dirname(path.realpath(__file__)), "../ftw.log"),
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )


def strip_protocol(string: str):
    """Removes all URL protocols from a string."""
    return re.sub(r"^[a-zA-Z]+://", "", string)


def get_favicon_url(url: str) -> str:
    """Returns the URL of the favicon for a given website."""
    # sadly, the duckduckgo API isn't as reliable as the google one
    return f"https://www.google.com/s2/favicons?domain={urlparse(url).hostname}&sz=128"


class WebhookAttachment:
    """
    Utility class to create a webhook attachment.

    Methods:
    - `to_dict()` returns the attachment in the format required by Discord.

    Format: `{"fileID": ("name.ext", content)}`
    """

    def __init__(self, file_name: str, content: str):
        self.file_id = file_name.split(".")[0]
        self.name = file_name
        self.content = content

    def to_dict(self):
        return {self.file_id: (self.name, self.content)}


class ErrorHandler:
    """
    Handles logging and reporting of errors.

    Methods:
    - `report()` prints to console, logs to file, and sends to error webhook.
    - `log()` prints to console and logs to file without sending to error webhook.

    Private Methods (you can use them tho)
    - `_get_traceback_string()` returns the traceback string of the error.
    - `_log_to_console()` logs the error to the console.
    - `_log_to_file()` logs the error to a file.
    - `_send_to_error_webhook()` sends the error to an error webhook.
    """

    @staticmethod
    def report(
        title: str,
        message: str,
        attachment: Optional[WebhookAttachment] = None,
        level: int = logging.ERROR,
    ) -> None:
        """
        Print to console, log to file, and send to error webhook.

        Args:
        - `title` (str): The title of the error.
        - `message` (str): The error message.
        - `attachment` (optional WebhookAttachment): The attachment to include in the error report.
        - `level` (int): The logging level for logging the error.
        """
        tb_info = ErrorHandler._get_traceback_string()
        ErrorHandler._log_to_console(title, message, tb_info)
        ErrorHandler._log_to_file(title, message, tb_info, level=level)
        ErrorHandler._send_to_error_webhook(title, message, tb_info, attachment)

    @staticmethod
    def log(
        title: str,
        message: str,
        level: int = logging.ERROR,
    ) -> None:
        """
        Print to console and log to file without sending to error webhook.

        Args:
        - `title` (str): The title of the error.
        - `message` (str): The error message.
        - `level` (int): The logging level for logging the error.
        """
        tb_info = ErrorHandler._get_traceback_string()
        ErrorHandler._log_to_console(title, message, tb_info)
        ErrorHandler._log_to_file(title, message, tb_info, level=level)

    @staticmethod
    def _get_traceback_string() -> str:
        tb = traceback.extract_stack()[:-2][-1]
        return f"Raised in '{tb.filename}' on line {tb.lineno} in '{tb.name}'"

    @staticmethod
    def _log_to_console(title: str, message: str, tb_info: Optional[str] = None) -> None:
        tb_info = tb_info or ErrorHandler._get_traceback_string()
        print("=" * 25, title, message, tb_info, "=" * 25, sep="\n")

    @staticmethod
    def _log_to_file(
        title: str,
        message: str,
        tb_info: Optional[str] = None,
        level: int = logging.ERROR,
    ) -> None:

        tb_info = tb_info or ErrorHandler._get_traceback_string()
        logging.log(level, f"{title} - {message}\n{tb_info}")

    @staticmethod
    def _send_to_error_webhook(
        title: str,
        message: str,
        tb_info: Optional[str] = None,
        attachment: Optional[WebhookAttachment] = None,
    ) -> None:

        tb_info = tb_info or ErrorHandler._get_traceback_string()

        if not (errhook := JsonFile("config.json", False).read().get("error_webhook")):
            logging.warning("Trying to send error to webhook, but no error webhook is configured.")
            return

        payload = {
            "embeds": [
                {
                    "title": f"ERROR: {title}",
                    "description": f"{message}\n\n{tb_info}",
                    "color": 16711680,
                }
            ]
        }

        res = requests.post(
            errhook,
            data={"payload_json": json.dumps(payload)},
            files=attachment.to_dict() if attachment else None,
            timeout=10,
        )

        if res.status_code >= 400:
            logging.error(f"Error webhook returned status code {res.status_code} ({res.reason})")
