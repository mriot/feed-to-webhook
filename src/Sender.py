class Sender:
    def send(self, feed):
        for webhook in feed.webhooks:
            webhook.send(feed.load())
