import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


def serialize_yaml(yaml_path: Path) -> dict[str, Any]:
    """Serialize provided yaml to dict."""
    try:
        raw_yaml = yaml_path.read_text(encoding="utf-8")
        return yaml.safe_load(raw_yaml)
    except Exception as err:
        logger.exception(err)

    return {}


def save_yaml(yaml_path: Path, yaml_data: dict) -> None:
    """Save provided data to yaml file."""
    with open(yaml_path, "w", encoding='utf-8') as stream:
        try:
            yaml.dump(yaml_data, stream)
        except Exception as err:
            logger.exception(err)
