import yaml
import logging

logger = logging.getLogger("yaml_parser")


class YamlConfig(object):
    def __init__(self, yaml_path: str) -> None:
        logger.debug(f"Processing {yaml_path}...")

        self.path = yaml_path
        self.yaml = self.read_yaml()

    def read_yaml(self) -> dict:
        """
        Reads provided yaml document.

        Returns loaded yaml or empty dict
        if content is missing.
        """
        try:
            with open(self.path, "r", encoding="utf-8") as config:
                loaded_yaml = self.load_yaml(config)
                if loaded_yaml:
                    return loaded_yaml
                return {}
        except FileNotFoundError:
            logger.error(f"File not found: {self.path}")
            return {}

    def load_yaml(self, stream) -> dict | None:
        """
        Loads yaml-file content and returns it in dict form.

        Returnes `None` if `YamlError` occured.
        """
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            logger.error(exc)

    def save_yaml(self, data: dict) -> None:
        """
        Saves provided data to yaml-file.
        """
        with open(self.path, "w", encoding="utf-8") as stream:
            try:
                yaml.dump(data, stream)
            except yaml.YAMLError as exc:
                logger.error(exc)
