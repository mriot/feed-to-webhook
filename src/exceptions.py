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
    def __init__(self, title: str, body: Optional[str] = None, attachment: Optional[str] = None):
        self.title = title
        self.body = body
        self.attachment = attachment

        # Exclude the calls to extract_stack and this class to get the actual error origin
        self.tb = traceback.extract_stack()[:-2][-1]
        self.tb_str = f"Raised in '{self.tb.filename}' on line {self.tb.lineno} in {self.tb.name}"

    def print_to_console(self):
        print(f"ERROR: {self.title}\n{self.body}\n{self.tb_str}")

    def log_to_file(self, level=logging.ERROR):
        logging.log(level, f"{self.title} - {self.tb_str}\nData: {self.body}")

    def send_to_webhook(self):
        if errhook := JsonFile("config.json", False).read().get("error_webhook"):
            headers = {
                "Content-Type": "application/json" if not self.attachment else "multipart/form-data"
            }
            content = {
                "embeds": [
                    {
                        "title": f"ERROR: {self.title}",
                        "description": f"{self.body}\n{self.tb_str}",
                        "color": 16711680,
                    }
                ]
            }

            res = requests.post(
                errhook,
                json=content,
                headers=headers,
                files=[("file", self.attachment)] if self.attachment else None,
                timeout=10,
            )

            if res.status_code >= 300:
                logging.error(
                    f"Error webhook returned status code {res.status_code} ({res.reason})"
                )
        else:
            logging.warning("Trying to send error to webhook, but no error webhook is configured.")

    def handle(self):
        self.print_to_console()
        self.log_to_file()
        self.send_to_webhook()


class FeedParseError(CustomBaseException):
    def __init__(self, title, feed_data):
        self.feed_data = feed_data
        super().__init__(title, attachment=feed_data)


class FeedConfigError(CustomBaseException):
    def __init__(self, title, feed_config):
        self.feed_config = feed_config
        super().__init__(title, f"```{json.dumps(feed_config, indent=2)}```")


class WebhookHTTPError(CustomBaseException):
    def __init__(self, title, body, response):
        self.body = body
        self.response = response
        super().__init__(title, f"{body}\n```{response}```")
