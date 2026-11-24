import logging
from pathlib import Path

import yaml
from pydantic import BaseModel

logger = logging.getLogger(__name__)


def serialize_yaml[DataModel: BaseModel](
    yaml_path: Path,
    validation_model: type[DataModel],
) -> DataModel:
    """Serialize provided yaml to pydantic model."""
    raw_yaml = yaml_path.read_text(encoding="utf-8")
    return validation_model.model_validate(yaml.safe_load(raw_yaml))


def save_yaml(yaml_path: Path, yaml_data: BaseModel) -> None:
    """Save provided data to yaml file."""
    yaml_path.write_text(yaml.safe_dump(yaml_data.model_dump()), encoding="utf-8")
