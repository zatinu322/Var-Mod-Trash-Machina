from pathlib import Path

from pydantic import BaseModel, Field, field_validator

from gui.constants import RESOURCES_PATH
from helpers.yaml_utils import serialize_yaml
from schemas.manifest import Manifest
from validators import validate_file_path

from ._shared import model_config


class AllowedExecutable(BaseModel):
    version: str
    offset: int
    length: int

    model_config = model_config


class RequiredMod(BaseModel):
    name: str
    version: str

    model_config = model_config


class Version(BaseModel):
    name: str
    title: str
    allowed_executables: list[AllowedExecutable]
    restricted_options: list[str] = Field(default_factory=list)
    manifest: Path
    options: str | None = None  # TODO: Add path validation
    required_mods: list[RequiredMod] = Field(default_factory=list)
    forbid_extra_mods: bool = True
    required_files: list[str] = Field(default_factory=list)

    model_config = model_config

    @field_validator("manifest", mode="after")
    def validate_manifest(cls, value: Path) -> Path:
        manifest_path = validate_file_path(RESOURCES_PATH / value)
        serialize_yaml(yaml_path=manifest_path, validation_model=Manifest)
        return manifest_path


class Versions(BaseModel):
    versions: list[Version]

    model_config = model_config

    @property
    def all(cls) -> dict[str, Version]:
        return {version.name: version for version in cls.versions}

    def get_by_name(self, name: str) -> Version:
        return self.all[name]
