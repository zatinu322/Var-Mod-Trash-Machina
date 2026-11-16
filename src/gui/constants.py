from pathlib import Path

NAME = "Ex Machina Randomizer"
VERSION = "v2.0.0"
BUILD = "build 261115a"
FULL_NAME = f"{NAME} {VERSION} {BUILD}"


MAIN_PATH = Path()
SRC_PATH = Path(__file__).parent.parent
ASSETS_PATH = SRC_PATH / "assets"
RESOURCES_PATH = MAIN_PATH / "resources"
LOCALIZATION_PATH = SRC_PATH / "localisation" / "localisation.yaml"
SETTINGS_PATH = RESOURCES_PATH / "settings.yaml"
PRESETS_PATH = RESOURCES_PATH / "presets.yaml"

SUPPORTED_VERSIONS = {
    "steam": "Steam v1.02",
    "cp114": "Community Patch v1.14.1",
    "cr114": "Community Remaster v1.14.1",
    "isl12cp": "Improved Storyline v1.2.1 (ComPatch)",
    "isl12cr": "Improved Storyline v1.2.1 (ComRemaster)",
    "isl1053": "Improved Storyline v1.0.5.3 (Пока не работает)",  # FIXME
}
