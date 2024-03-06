import yaml
import logging

logger = logging.getLogger("pavlik")


class YamlConfig(object):
    def __init__(self, yaml_path: str) -> None:
        self.path = yaml_path
        self.yaml = self.read_yaml()

    def read_yaml(self) -> dict | None:
        try:
            with open(self.path, "r", encoding="utf-8") as config:
                loaded_yaml = self.load_yaml(config)
                if loaded_yaml:
                    return loaded_yaml
                else:
                    return {}
        except FileNotFoundError:
            logger.warning(f"File not found: {self.path}")
            return {}

    def load_yaml(self, stream) -> dict:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            logger.error(exc)

    def dump_yaml(self, data: dict) -> None:
        with open(self.path, "w", encoding="utf-8") as stream:
            try:
                yaml.dump(data, stream)
            except yaml.YAMLError as exc:
                logger.error(exc)
