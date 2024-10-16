import yaml
import logging
from pathlib import Path

logger = logging.getLogger(Path(__file__).name)


def serialize_yaml(yaml_path: Path) -> dict:
    """
    Serializes provided yaml to dict.

    Returns serialized data or empty dict.
    """
    try:
        with open(yaml_path, "r", encoding="utf-8") as stream:
            serialized_yaml = yaml.safe_load(stream)
            return serialized_yaml
    except FileNotFoundError:
        logger.error(f"File not found: {yaml_path}")
    except yaml.YAMLError as err:
        logger.exception(err)

    return {}


def save_yaml(yaml_path: Path, yaml_data: dict) -> None:
    """
    Saves provided data to yaml file.
    """
    with open(yaml_path, "w", encoding='utf-8') as stream:
        try:
            yaml.dump(yaml_data, stream)
        except yaml.YAMLError as err:
            logger.error(err)
