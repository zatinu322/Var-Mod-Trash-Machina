from pydantic import BaseModel, Field


class AllowedExecutable(BaseModel):
    version: str
    offset: int
    length: int


class RequiredMod(BaseModel):
    name: str
    version: str


class Version(BaseModel):
    name: str
    title: str
    allowed_executables: list[AllowedExecutable]
    restricted_options: list[str] = Field(default_factory=list)
    manifest: str
    options: str | None = None
    required_mods: list[RequiredMod] = Field(default_factory=list)
    forbid_extra_mods: bool = True


class Versions(BaseModel):
    versions: list[Version]
