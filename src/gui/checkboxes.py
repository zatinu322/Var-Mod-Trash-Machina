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
            cls.ai_vehs.data: cls.ai_vehs,
            cls.aim.data: cls.aim,
            cls.armor.data: cls.armor,
            cls.bkgd.data: cls.bkgd,
            cls.books_history.data: cls.books_history,
            cls.cab_cargo.data: cls.cab_cargo,
            cls.clans.data: cls.clans,
            cls.controls.data: cls.controls,
            cls.crashes.data: cls.crashes,
            cls.descriptions.data: cls.descriptions,
            cls.dialogues.data: cls.dialogues,
            cls.digits.data: cls.digits,
            cls.dwellers.data: cls.dwellers,
            cls.engines.data: cls.engines,
            cls.env_models.data: cls.env_models,
            cls.env_textures.data: cls.env_textures,
            cls.explosions.data: cls.explosions,
            cls.fadingmsgs.data: cls.fadingmsgs,
            cls.fov.data: cls.fov,
            cls.goods_guns.data: cls.goods_guns,
            cls.gravity.data: cls.gravity,
            cls.gui_icons.data: cls.gui_icons,
            cls.gui_text.data: cls.gui_text,
            cls.guns.data: cls.guns,
            cls.guns_lua.data: cls.guns_lua,
            cls.hits.data: cls.hits,
            cls.horns.data: cls.horns,
            cls.humans.data: cls.humans,
            cls.landscape.data: cls.landscape,
            cls.lightmaps.data: cls.lightmaps,
            cls.maps.data: cls.maps,
            cls.masks.data: cls.masks,
            cls.music.data: cls.music,
            cls.names.data: cls.names,
            cls.npc_look.data: cls.npc_look,
            cls.other_sounds.data: cls.other_sounds,
            cls.pl_veh.data: cls.pl_veh,
            cls.quests.data: cls.quests,
            cls.radar.data: cls.radar,
            cls.radio.data: cls.radio,
            cls.render.data: cls.render,
            cls.shooting.data: cls.shooting,
            cls.skybox.data: cls.skybox,
            cls.speech.data: cls.speech,
            cls.splashes.data: cls.splashes,
            cls.tiles.data: cls.tiles,
            cls.towns.data: cls.towns,
            cls.trees.data: cls.trees,
            cls.veh_skins.data: cls.veh_skins,
            cls.weather.data: cls.weather,
            cls.wheels.data: cls.wheels,
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
