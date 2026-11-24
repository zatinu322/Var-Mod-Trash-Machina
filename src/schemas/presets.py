from pydantic import BaseModel

from ._shared import model_config


class PresetCheckboxes(BaseModel):
    maps: bool = False
    digits: bool = False
    splashes: bool = False
    bkgd: bool = False
    clans: bool = False
    gui_icons: bool = False
    radar: bool = False
    goods_guns: bool = False
    cab_cargo: bool = False
    aim: bool = False
    names: bool = False
    dialogues: bool = False
    quests: bool = False
    controls: bool = False
    fadingmsgs: bool = False
    gui_text: bool = False
    books_history: bool = False
    descriptions: bool = False
    music: bool = False
    speech: bool = False
    radio: bool = False
    crashes: bool = False
    explosions: bool = False
    engines: bool = False
    horns: bool = False
    hits: bool = False
    shooting: bool = False
    other_sounds: bool = False
    env_models: bool = False
    towns: bool = False
    guns: bool = False
    trees: bool = False
    npc_look: bool = False
    wheels: bool = False
    humans: bool = False
    dwellers: bool = False
    env_textures: bool = False
    masks: bool = False
    veh_skins: bool = False
    lightmaps: bool = False
    skybox: bool = False
    tiles: bool = False
    weather: bool = False
    landscape: bool = False
    ai_vehs: bool = False
    pl_veh: bool = False
    guns_lua: bool = False
    render: bool = False
    gravity: bool = False
    fov: bool = False
    armor: bool = False

    model_config = model_config


class PresetTitle(BaseModel):
    rus: str
    en: str

    model_config = model_config


class Preset(BaseModel):
    name: str
    title: PresetTitle
    checkboxes: PresetCheckboxes = PresetCheckboxes()

    model_config = model_config


class Presets(BaseModel):
    presets: list[Preset]

    model_config = model_config
