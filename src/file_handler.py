from os import path
import sys
import json


class JsonFile:
    """Helper class for reading and writing JSON files in the project's root directory."""

    def __init__(self, file_name, create=True):
        self.file_path = path.join(path.dirname(path.realpath(__file__)), "..", file_name)

        if create and not path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump({}, file, ensure_ascii=False, indent=4)

    def read(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file) or {}
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file '{self.file_path}': {e}")
            sys.exit(1)
        except FileNotFoundError as e:
            print(f"File {e} not found")
            sys.exit(1)

    def write(self, data):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
