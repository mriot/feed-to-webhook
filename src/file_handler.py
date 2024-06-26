from os import path
import sys
import jsonc

from utils import ErrorHandler


class JsonFile:
    """Helper class for reading and writing JSON files in the project's root directory."""

    def __init__(self, file_name: str, create: bool = True):
        self.file_path: str = path.join(path.dirname(path.realpath(__file__)), "..", file_name)

        if create and not path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                jsonc.dump({}, file, ensure_ascii=False, indent=4)

    def read(self) -> dict:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return jsonc.load(file) or {}

        except jsonc.JSONDecodeError as e:
            ErrorHandler.log(
                "JSON Decode Error",
                f"Error parsing JSON file '{self.file_path}': {e}",
            )
            sys.exit(1)

        except FileNotFoundError as e:
            ErrorHandler.log("File Not Found", f"File {e} not found")
            sys.exit(1)

    def write(self, data: dict) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            jsonc.dump(data, file, ensure_ascii=False, indent=4)
