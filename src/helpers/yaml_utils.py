import logging
from pathlib import Path
from typing import Any, cast

import yaml
from mergedeep import merge

logger = logging.getLogger(__name__)


def serialize_yaml(yaml_path: Path, *override_paths: Path) -> dict[str, Any]:
    """Serialize provided yaml to dict."""
    try:
        raw_yaml = yaml_path.read_text(encoding="utf-8")
        serialized_yaml = yaml.safe_load(raw_yaml)
        for path in override_paths:
            override_yaml = path.read_text(encoding="utf-8")
            serialized_yaml = merge(serialized_yaml, yaml.safe_load(override_yaml))
        return cast(dict[str, Any], serialized_yaml)
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
