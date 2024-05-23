import json
import logging
import traceback
from os import path
from typing import Optional


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

        self.traceback_info = traceback.extract_stack()[:-2]  # Exclude this + call to extract_stack
        last_frame = self.traceback_info[-1]

        self.file_name = last_frame.filename
        self.line_number = last_frame.lineno
        self.function_name = last_frame.name
        self.code_line = last_frame.line

    def print(self):
        pass

    def log(self, level=logging.ERROR):
        logging.log(
            level,
            f"{self.title} : {self.body}  -  {self.file_name} - {self.line_number} - {self.function_name} - {self.code_line}",
        )

    def send_to_webhook(self):
        pass

    def handle(self):
        self.print()
        self.log()
        self.send_to_webhook()


class FeedConfigError(CustomBaseException):
    def __init__(self, title, feed_config):
        self.feed_config = feed_config
        super().__init__(title, f"```{json.dumps(feed_config, indent=2)}```")


class WebhookHTTPError(CustomBaseException):
    def __init__(self, title, body, response):
        self.body = body
        self.response = response
        super().__init__(title, f"{body}\n```{response}```")
