from flet import Checkbox

from gui.shared import FletControl


class Checkboxes:
    ai_vehs = Checkbox(label="ai_vehs", data="ai_vehs")
    aim = Checkbox(label="aim", data="aim")
    armor = Checkbox(label="armor", data="armor")
    bkgd = Checkbox(label="bkgd", data="bkgd")
    books_history = Checkbox(label="books_history", data="books_history")
    cab_cargo = Checkbox(label="cab_cargo", data="cab_cargo")
    clans = Checkbox(label="clans", data="clans")
    controls = Checkbox(label="controls", data="controls")
    crashes = Checkbox(label="crashes", data="crashes")
    descriptions = Checkbox(label="descriptions", data="descriptions")
    dialogues = Checkbox(label="dialogues", data="dialogues")
    digits = Checkbox(label="digits", data="digits")
    dwellers = Checkbox(label="dwellers", data="dwellers")
    engines = Checkbox(label="engines", data="engines")
    env_models = Checkbox(label="env_models", data="env_models")
    env_textures = Checkbox(label="env_textures", data="env_textures")
    explosions = Checkbox(label="explosions", data="explosions")
    fadingmsgs = Checkbox(label="fadingmsgs", data="fadingmsgs")
    fov = Checkbox(label="fov", data="fov")
    goods_guns = Checkbox(label="goods_guns", data="goods_guns")
    gravity = Checkbox(label="gravity", data="gravity")
    gui_icons = Checkbox(label="gui_icons", data="gui_icons")
    gui_text = Checkbox(label="gui_text", data="gui_text")
    guns = Checkbox(label="guns", data="guns")
    guns_lua = Checkbox(label="guns_lua", data="guns_lua")
    hits = Checkbox(label="hits", data="hits")
    horns = Checkbox(label="horns", data="horns")
    humans = Checkbox(label="humans", data="humans")
    landscape = Checkbox(label="landscape", data="landscape")
    lightmaps = Checkbox(label="lightmaps", data="lightmaps")
    maps = Checkbox(label="maps", data="maps")
    masks = Checkbox(label="masks", data="masks")
    music = Checkbox(label="music", data="music")
    names = Checkbox(label="names", data="names")
    npc_look = Checkbox(label="npc_look", data="npc_look")
    other_sounds = Checkbox(label="other_sounds", data="other_sounds")
    pl_veh = Checkbox(label="pl_veh", data="pl_veh")
    quests = Checkbox(label="quests", data="quests")
    radar = Checkbox(label="radar", data="radar")
    radio = Checkbox(label="radio", data="radio")
    render = Checkbox(label="render", data="render")
    shooting = Checkbox(label="shooting", data="shooting")
    skybox = Checkbox(label="skybox", data="skybox")
    speech = Checkbox(label="speech", data="speech")
    splashes = Checkbox(label="splashes", data="splashes")
    tiles = Checkbox(label="tiles", data="tiles")
    towns = Checkbox(label="towns", data="towns")
    trees = Checkbox(label="trees", data="trees")
    veh_skins = Checkbox(label="veh_skins", data="veh_skins")
    weather = Checkbox(label="weather", data="weather")
    wheels = Checkbox(label="wheels", data="wheels")

    @property
    def all(cls) -> dict[str, Checkbox]:
        return {
            "ai_vehs": cls.ai_vehs,
            "aim": cls.aim,
            "armor": cls.armor,
            "bkgd": cls.bkgd,
            "books_history": cls.books_history,
            "cab_cargo": cls.cab_cargo,
            "clans": cls.clans,
            "controls": cls.controls,
            "crashes": cls.crashes,
            "descriptions": cls.descriptions,
            "dialogues": cls.dialogues,
            "digits": cls.digits,
            "dwellers": cls.dwellers,
            "engines": cls.engines,
            "env_models": cls.env_models,
            "env_textures": cls.env_textures,
            "explosions": cls.explosions,
            "fadingmsgs": cls.fadingmsgs,
            "fov": cls.fov,
            "goods_guns": cls.goods_guns,
            "gravity": cls.gravity,
            "gui_icons": cls.gui_icons,
            "gui_text": cls.gui_text,
            "guns": cls.guns,
            "guns_lua": cls.guns_lua,
            "hits": cls.hits,
            "horns": cls.horns,
            "humans": cls.humans,
            "landscape": cls.landscape,
            "lightmaps": cls.lightmaps,
            "maps": cls.maps,
            "masks": cls.masks,
            "music": cls.music,
            "names": cls.names,
            "npc_look": cls.npc_look,
            "other_sounds": cls.other_sounds,
            "pl_veh": cls.pl_veh,
            "quests": cls.quests,
            "radar": cls.radar,
            "radio": cls.radio,
            "render": cls.render,
            "shooting": cls.shooting,
            "skybox": cls.skybox,
            "speech": cls.speech,
            "splashes": cls.splashes,
            "tiles": cls.tiles,
            "towns": cls.towns,
            "trees": cls.trees,
            "veh_skins": cls.veh_skins,
            "weather": cls.weather,
            "wheels": cls.wheels,
        }

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
