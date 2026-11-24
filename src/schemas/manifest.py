from enum import StrEnum

from pydantic import BaseModel, Field

from ._shared import model_config


class OptionType(StrEnum):
    FILES = "files"
    XML_TEXT = "xml-text"
    XML_ATTRIBUTES = "xml-attributes"


class BaseOption(BaseModel):
    type: OptionType

    model_config = model_config


class GroupFiles(BaseModel):
    path: str
    items: list[str]

    model_config = model_config


class FilesOption(BaseOption):
    groups: list[list[GroupFiles]]

    model_config = model_config


class XMLText(BaseModel):
    tag: str
    id: str
    value: str
    exclude_suffixes: list[str] = Field(default_factory=list)
    include_suffixes: list[str] = Field(default_factory=list)

    model_config = model_config


class GroupText(BaseModel):
    path: str
    items: list[XMLText]

    model_config = model_config


class XMLTextOption(BaseOption):
    groups: list[list[GroupText]]

    model_config = model_config


class XMLAttributesOption(BaseOption):
    path: str
    tag: str
    id: str
    groups: list[list[str]]

    model_config = model_config


class Options(BaseModel):
    maps: FilesOption
    digits: FilesOption
    splashes: FilesOption
    bkgd: FilesOption
    clans: FilesOption
    gui_icons: FilesOption
    radar: FilesOption
    goods_guns: FilesOption
    cab_cargo: FilesOption
    aim: FilesOption
    music: FilesOption
    speech: FilesOption
    radio: FilesOption
    crashes: FilesOption
    explosions: FilesOption
    engines: FilesOption
    horns: FilesOption
    hits: FilesOption
    shooting: FilesOption
    other_sounds: FilesOption
    env_textures: FilesOption
    masks: FilesOption
    veh_skins: FilesOption
    lightmaps: FilesOption
    skybox: FilesOption
    tiles: FilesOption
    names: XMLTextOption
    dialogues: XMLTextOption
    quests: XMLTextOption
    controls: XMLTextOption
    fadingmsgs: XMLTextOption
    gui_text: XMLTextOption
    books_history: XMLTextOption
    descriptions: XMLTextOption
    weather: XMLTextOption
    env_models: XMLAttributesOption
    towns: XMLAttributesOption
    guns: XMLAttributesOption
    trees: XMLAttributesOption
    wheels: XMLAttributesOption
    humans: XMLAttributesOption
    # TODO: add types
    ai_vehs: None = None
    armor: None = None
    dwellers: None = None
    fov: None = None
    gravity: None = None
    guns_lua: None = None
    landscape: None = None
    npc_look: None = None
    pl_veh: None = None
    render: None = None

    model_config = model_config


class Servers(BaseModel):
    paths: list[str]
    items: list[str]

    model_config = model_config


class TriggerScript(BaseModel):
    name: str
    script: str

    model_config = model_config


class Trigger(BaseModel):
    path: str
    scripts: list[TriggerScript]

    model_config = model_config


class Prerequisites(BaseModel):
    servers: Servers
    triggers: list[Trigger]

    model_config = model_config


class Manifest(BaseModel):
    prerequisites: Prerequisites
    options: Options

    model_config = model_config
