from flet import Checkbox

from gui.shared import FletControl


class Checkboxes:
    ai_vehs = Checkbox(label="ai_vehs")
    aim = Checkbox(label="aim")
    armor = Checkbox(label="armor")
    bkgd = Checkbox(label="bkgd")
    books_history = Checkbox(label="books_history")
    cab_cargo = Checkbox(label="cab_cargo")
    clans = Checkbox(label="clans")
    controls = Checkbox(label="controls")
    crashes = Checkbox(label="crashes")
    descriptions = Checkbox(label="descriptions")
    dialogues = Checkbox(label="dialogues")
    digits = Checkbox(label="digits")
    dwellers = Checkbox(label="dwellers")
    engines = Checkbox(label="engines")
    env_models = Checkbox(label="env_models")
    env_textures = Checkbox(label="env_textures")
    explosions = Checkbox(label="explosions")
    fadingmsgs = Checkbox(label="fadingmsgs")
    fov = Checkbox(label="fov")
    goods_guns = Checkbox(label="goods_guns")
    gravity = Checkbox(label="gravity")
    gui_icons = Checkbox(label="gui_icons")
    gui_text = Checkbox(label="gui_text")
    guns = Checkbox(label="guns")
    guns_lua = Checkbox(label="guns_lua")
    hits = Checkbox(label="hits")
    horns = Checkbox(label="horns")
    humans = Checkbox(label="humans")
    landscape = Checkbox(label="landscape")
    lightmaps = Checkbox(label="lightmaps")
    maps = Checkbox(label="maps")
    masks = Checkbox(label="masks")
    music = Checkbox(label="music")
    names = Checkbox(label="names")
    npc_look = Checkbox(label="npc_look")
    other_sounds = Checkbox(label="other_sounds")
    pl_veh = Checkbox(label="pl_veh")
    quests = Checkbox(label="quests")
    radar = Checkbox(label="radar")
    radio = Checkbox(label="radio")
    render = Checkbox(label="render")
    shooting = Checkbox(label="shooting")
    skybox = Checkbox(label="skybox")
    speech = Checkbox(label="speech")
    splashes = Checkbox(label="splashes")
    tiles = Checkbox(label="tiles")
    towns = Checkbox(label="towns")
    trees = Checkbox(label="trees")
    veh_skins = Checkbox(label="veh_skins")
    weather = Checkbox(label="weather")
    wheels = Checkbox(label="wheels")

    @property
    def all(cls) -> list[FletControl]:
        return [
            cls.ai_vehs,
            cls.aim,
            cls.armor,
            cls.bkgd,
            cls.books_history,
            cls.cab_cargo,
            cls.clans,
            cls.controls,
            cls.crashes,
            cls.descriptions,
            cls.dialogues,
            cls.digits,
            cls.dwellers,
            cls.engines,
            cls.env_models,
            cls.env_textures,
            cls.explosions,
            cls.fadingmsgs,
            cls.fov,
            cls.goods_guns,
            cls.gravity,
            cls.gui_icons,
            cls.gui_text,
            cls.guns,
            cls.guns_lua,
            cls.hits,
            cls.horns,
            cls.humans,
            cls.landscape,
            cls.lightmaps,
            cls.maps,
            cls.masks,
            cls.music,
            cls.names,
            cls.npc_look,
            cls.other_sounds,
            cls.pl_veh,
            cls.quests,
            cls.radar,
            cls.radio,
            cls.render,
            cls.shooting,
            cls.skybox,
            cls.speech,
            cls.splashes,
            cls.tiles,
            cls.towns,
            cls.trees,
            cls.veh_skins,
            cls.weather,
            cls.wheels,
        ]

    @property
    def icons_group(cls) -> list[FletControl]:
        return [
            cls.maps,
            cls.digits,
            cls.splashes,
            cls.bkgd,
            cls.clans,
            cls.gui_icons,
            cls.radar,
            cls.goods_guns,
            cls.cab_cargo,
            cls.aim,
        ]

    @property
    def text_group(cls) -> list[FletControl]:
        return [
            cls.names,
            cls.dialogues,
            cls.quests,
            cls.controls,
            cls.fadingmsgs,
            cls.gui_text,
            cls.books_history,
            cls.descriptions,
        ]

    @property
    def sound_group(cls) -> list[FletControl]:
        return [
            cls.music,
            cls.speech,
            cls.radio,
            cls.crashes,
            cls.explosions,
            cls.engines,
            cls.horns,
            cls.hits,
            cls.shooting,
            cls.other_sounds,
        ]

    @property
    def models_group(cls) -> list[FletControl]:
        return [
            cls.env_models,
            cls.towns,
            cls.guns,
            cls.trees,
            cls.npc_look,
            cls.wheels,
            cls.humans,
            cls.dwellers,
        ]

    @property
    def textures_group(cls) -> list[FletControl]:
        return [
            cls.env_textures,
            cls.masks,
            cls.veh_skins,
            cls.lightmaps,
            cls.skybox,
            cls.tiles,
        ]

    @property
    def other_group(cls) -> list[FletControl]:
        return [
            cls.weather,
            cls.landscape,
            cls.ai_vehs,
            cls.pl_veh,
            cls.guns_lua,
        ]

    @property
    def executable_group(cls) -> list[FletControl]:
        return [
            cls.render,
            cls.gravity,
            cls.fov,
            cls.armor,
        ]
