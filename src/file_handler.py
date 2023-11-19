import os
import sys
import yaml


class YamlFile:
    def __init__(self, file_name, create=True):
        self.file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)

        if create and not os.path.exists(self.file_path):
            open(self.file_path, "a").close()

    def read(self):
        try:
            with open(self.file_path, "r") as config_file:
                return yaml.safe_load(config_file)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            sys.exit(1)
        except FileNotFoundError as e:
            print(f"File {e} not found")
            sys.exit(1)

    def write(self, data):
        with open(self.file_path, "w") as config_file:
            yaml.safe_dump(data, config_file, sort_keys=False)
