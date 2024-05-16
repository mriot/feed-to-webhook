import traceback


class CustomBaseException(Exception):
    def __init__(self, title, message) -> None:
        self.title = title
        self.message = message

        # TODO - need traceback data

    def print(self):
        print(f"ERROR: {self.title}\n{self.message}")

    def log_to_file(self):
        print(f"ERROR: {self.title}\n{self.message}")

    def send_to_webhook(self):
        pass

    def all(self):
        self.print()
        self.log_to_file()
        self.send_to_webhook()


class TitleException(CustomBaseException):
    def __init__(self, title) -> None:
        self.title = f"{title} - blablabla"
        super().__init__(self.title, "")
