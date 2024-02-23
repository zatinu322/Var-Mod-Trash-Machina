from pathlib import Path


REQUIRED_GAME_FILES = [
    Path("data"),
    Path("data/gamedata"),
    Path("data/if"),
    Path("data/maps"),
    Path("data/models"),
    Path("data/music"),
    Path("data/scripts"),
    Path("data/sounds"),
    Path("data/textures"),
    Path("data/tiles"),
    Path("data/weathertexs"),
    Path("data/weather.xml")
]

POSSIBLE_EXE_PATHS = [
    Path("hta.exe"),
    Path("game.exe"),
    Path("start.exe"),
    Path("ExMachina.exe")
]

NO_EXE_ALLOWED = ["steam", "isl1053"]
FOV_ALLOWED = ["steam", "isl1053"]

VERSIONS_INFO = {
    "steam": {
        "exe": [
            {
                "version": "release build v1.02",
                "offset": 0x0059069C,
                "length": 19
            }
        ],
        "manifest": "resources/manifests/manifest_steam.yaml"
    },
    "cp114": {
        "exe": [
            {
                "version": "Patch build v1.14",
                "offset": 0x00590696,
                "length": 17
            }
        ],
        "manifest": "resources/manifests/manifest_cp114.yaml"
    },
    "cr114": {
        "exe": [
            {
                "version": "Remaster build v1.14",
                "offset": 0x00590696,
                "length": 20
            }
        ],
        "manifest": "resources/manifests/manifest_cr114.yaml",
        "options": "resources/options/options_cr114.yaml"
    },
    "isl12cp": {
        "exe": [
            {
                "version": "Patch build v1.14",
                "offset": 0x00590696,
                "length": 17
            }
        ],
        "manifest": "resources/manifests/manifest_isl12cp.yaml"
    },
    "isl12cr": {
        "exe": [
            {
                "version": "Remaster build v1.14",
                "offset": 0x00590696,
                "length": 20
            }
        ],
        "manifest": "resources/manifests/manifest_isl12cr.yaml",
        "options": "resources/options/options_isl12cr.yaml"
    },
    "isl1053": {
        "exe": [
            {
                "version": "release build v1.02",
                "offset": 0x0059069C,
                "length": 19
            }
        ],
        "manifest": "resources/manifests/manifest_isl1053.yaml"
    }
}
