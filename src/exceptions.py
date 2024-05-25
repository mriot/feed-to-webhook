import json
import logging
import traceback
from os import path
from typing import Optional

import requests

from file_handler import JsonFile


logging.basicConfig(
    filename=path.join(path.dirname(path.realpath(__file__)), "../ftw.log"),
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)


class CustomBaseException(Exception):
    def __init__(self, title: str, message: str, attachment: Optional[dict] = None):
        self.title = title
        self.message = message
        self.attachment = attachment  # format: {"fileID": ("name.ext", str)}

        # Exclude the calls to extract_stack and this class to get the actual error origin
        self.tb = traceback.extract_stack()[:-2][-1]
        self.tb_str = f"Raised in '{self.tb.filename}' on line {self.tb.lineno} in '{self.tb.name}'"

    def log(self, level=logging.ERROR):
        """Log the error to the console and log file."""
        self.print_to_console()
        self.log_to_file(level=level)

    def report(self):
        """Report the error to the console, log file, and webhook."""
        self.print_to_console()
        self.log_to_file()
        self.send_to_webhook()

    def print_to_console(self):
        print("=" * 25, self.title, self.message, self.tb_str, "=" * 25, sep="\n")

    def log_to_file(self, level=logging.ERROR):
        logging.log(level, f"{self.title} - {self.message}\n{self.tb_str}")

    def send_to_webhook(self):
        if not (errhook := JsonFile("config.json", False).read().get("error_webhook")):
            logging.warning("Trying to send error to webhook, but no error webhook is configured.")
        else:
            payload = {
                "embeds": [
                    {
                        "title": f"ERROR: {self.title}",
                        "description": f"{self.message}\n{self.tb_str}",
                        "color": 16711680,
                    }
                ]
            }

            res = requests.post(
                errhook,
                data={"payload_json": json.dumps(payload)},
                files=self.attachment if self.attachment else None,
                timeout=10,
            )

            if res.status_code >= 400:
                logging.error(
                    f"Error webhook returned status code {res.status_code} ({res.reason})"
                )


class FeedParseError(CustomBaseException):
    def __init__(self, title: str, message: str, feed_data_attachment: str):
        self.title = title
        self.message = message
        self.feed_data = {"file": ("feed_data.xml", feed_data_attachment)}
        super().__init__(self.title, self.message, attachment=self.feed_data)


class FeedConfigError(CustomBaseException):
    def __init__(self, title: str, feed_config: str):
        self.title = title
        self.feed_config = f"```{json.dumps(feed_config, indent=2)}```"
        super().__init__(self.title, self.feed_config)


class WebhookHTTPError(CustomBaseException):
    def __init__(self, title: str, message: str, response: str):
        self.title = title
        self.message = message
        self.response = f"```{response}```"
        super().__init__(self.title, f"{self.message}\n{self.response}")


class ConfigError(CustomBaseException):
    def __init__(self, title: str, message: str):
        self.title = title
        self.message = message
        super().__init__(self.title, self.message)


class NoItemsInFeedError(CustomBaseException):
    def __init__(self, title: str, message: str):
        self.title = title
        self.message = message
        super().__init__(self.title, self.message)
