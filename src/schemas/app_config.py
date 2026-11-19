from pydantic import BaseModel


class AppWindow(BaseModel):
    pos_x: int = 0
    pox_y: int = 0

    width: float | None = None
    height: float | None = None

    is_maximized: bool = False


class AppCheckboxes(BaseModel):
    ai_vehs: bool = False
    aim: bool = False
    armor: bool = False
    bkgd: bool = False
    books_history: bool = False
    cab_cargo: bool = False
    clans: bool = False
    controls: bool = False
    crashes: bool = False
    descriptions: bool = False
    dialogues: bool = False
    digits: bool = False
    dwellers: bool = False
    engines: bool = False
    env_models: bool = False
    env_textures: bool = False
    explosions: bool = False
    fadingmsgs: bool = False
    fov: bool = False
    goods_guns: bool = False
    gravity: bool = False
    gui_icons: bool = False
    gui_text: bool = False
    guns: bool = False
    guns_lua: bool = False
    hits: bool = False
    horns: bool = False
    humans: bool = False
    landscape: bool = False
    lightmaps: bool = False
    maps: bool = False
    masks: bool = False
    music: bool = False
    names: bool = False
    npc_look: bool = False
    other_sounds: bool = False
    pl_veh: bool = False
    quests: bool = False
    radar: bool = False
    radio: bool = False
    render: bool = False
    shooting: bool = False
    skybox: bool = False
    speech: bool = False
    splashes: bool = False
    tiles: bool = False
    towns: bool = False
    trees: bool = False
    veh_skins: bool = False
    weather: bool = False
    wheels: bool = False


class AppConfig(BaseModel):
    window: AppWindow = AppWindow()
    language: str = "en"
    preset: str = "p_custom"
    checkboxes: AppCheckboxes = AppCheckboxes()
    game_path: str = ""
    game_version: str = ""
