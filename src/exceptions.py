import json
from typing import Optional

from utils import WebhookAttachment


class CustomBaseException(Exception):
    def __init__(self, title: str, message: str, attachment: Optional[WebhookAttachment] = None):
        self.title = title
        self.message = message
        self.attachment = attachment


class FeedParseError(CustomBaseException):
    def __init__(self, title: str, message: str, feed_data: str):
        self.title = title
        self.message = message
        # TODO - handle different file types (json, xml)
        self.feed_data = WebhookAttachment("feed_data.xml", feed_data)
        super().__init__(self.title, self.message, attachment=self.feed_data)


class FeedConfigError(CustomBaseException):
    def __init__(self, title: str, feed_config: str):
        self.title = title
        self.feed_config = f"```{json.dumps(feed_config, indent=2)}```"
        super().__init__(self.title, self.feed_config)


class WebhookHTTPError(CustomBaseException):
    def __init__(
        self,
        title: str,
        feed_url: str,
        webhook_url: str,
        response: str,
        payload: Optional[str] = None,
    ):
        self.title = title
        self.feed_url = feed_url
        self.webhook_url = webhook_url
        self.response = response
        self.attachment = WebhookAttachment("payload.json", payload) if payload else None

        message = (
            f"Feed: {self.feed_url}\n"
            f"Webhook: {self.webhook_url}\n\n"
            f"Response: ```{self.response}```"
        )

        super().__init__(self.title, message, attachment=self.attachment)


class WebhookRateLimitError(CustomBaseException):
    def __init__(self, feed_url: str, webhook_url: str):
        self.feed_url = feed_url
        self.webhook_url = webhook_url

        message = (
            "Could not deliver the message even after multiple retries.\n\n"
            f"Feed: {self.feed_url}\n"
            f"Webhook: {self.webhook_url}"
        )

        super().__init__("Rate limit exceeded", message)


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
