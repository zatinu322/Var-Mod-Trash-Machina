import os

from pathlib import Path

VERSION = "0.9 beta"
NAME = f"Ex Machina Randomizer v{VERSION}"

MAIN_PATH = Path(os.getcwd())
RESOURCES_PATH = Path(os.path.join(MAIN_PATH, "resources"))
LOCALIZATION_PATH = Path(os.path.join(RESOURCES_PATH, "localisation.yaml"))
SETTINGS_PATH = Path(os.path.join(RESOURCES_PATH, "settings.yaml"))

REQUIRED_FILES = [
    RESOURCES_PATH,
    LOCALIZATION_PATH
]

REQUIRED_GAME_FILES = [
    "data",
    "dbghelp.dll",
    "fmod.dll"
]

SUPPORTED_VERSIONS = {
    "steam": "Steam v1.02",
    "cp114": "Community Patch v1.14",
    "cr114": "Community Remaster v1.14",
    "isl12cp": "Improved Storyline v1.2 (ComPatch)",
    "isl12cr": "Improved Storyline v1.2 (ComRemaster)",
    "isl1053": "Improved Storyline v1.0.5.3"
}

VERSIONS_INFO = {
    "steam": {
        "exe": [b"release build v1.02"],
        "manifest": "resources/manifests/manifest_steam.yaml"
    },
    "cp114": {
        "exe": [b"Patch build v1.14"],
        "manifest": ""
    },
    "cr114": {
        "exe": [b"Remaster build v1.14"],
        "manifest": ""
    },
    "isl12cp": {
        "exe": [b"Patch build v1.14"],
        "manifest": ""
    },
    "isl12cr": {
        "exe": [b"Remaster build v1.14"],
        "manifest": ""
    },
    "isl1053": {
        "exe": [b"release build v1.02"],
        "manifest": "resources/manifests/manifest_isl1053.yaml"
    }
}


PRESETS = {
    "p_recommended": {
        "cb_ai_vehs": True,
        "cb_aim": True,
        "cb_armor": True,
        "cb_bkgd": True,
        "cb_books_history": True,
        "cb_cab_cargo": True,
        "cb_clans": True,
        "cb_controls": False,
        "cb_crashes": True,
        "cb_descriptions": True,
        "cb_dialogues": True,
        "cb_digits": True,
        "cb_dwellers": True,
        "cb_engines": True,
        "cb_env_models": True,
        "cb_env_textures": False,
        "cb_explosions": True,
        "cb_fadingmsgs": True,
        "cb_fov": False,
        "cb_goods_guns": True,
        "cb_gravity": False,
        "cb_gui_icons": True,
        "cb_gui_text": True,
        "cb_guns": False,
        "cb_guns_lua": True,
        "cb_hits": True,
        "cb_horns": True,
        "cb_humans": True,
        "cb_landscape": False,
        "cb_lightmaps": True,
        "cb_maps": True,
        "cb_masks": True,
        "cb_music": True,
        "cb_names": True,
        "cb_npc_look": True,
        "cb_other_sounds": True,
        "cb_pl_veh": True,
        "cb_quests": True,
        "cb_radar": True,
        "cb_radio": True,
        "cb_render": False,
        "cb_shooting": True,
        "cb_skybox": True,
        "cb_speech": True,
        "cb_splashes": True,
        "cb_tiles": True,
        "cb_towns": False,
        "cb_trees": True,
        "cb_veh_skins": True,
        "cb_weather": True,
        "cb_wheels": True
    },
    "p_custom": {}
}