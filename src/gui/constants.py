from pathlib import Path

NAME = "Ex Machina Randomizer"
VERSION = "v2.0.0"
BUILD = "build 261115a"
FULL_NAME = f"{NAME} {VERSION} {BUILD}"


MAIN_PATH = Path()
SRC_PATH = Path(__file__).parent.parent
ASSETS_PATH = SRC_PATH / "assets"
RESOURCES_PATH = MAIN_PATH / "resources"
LOCALISATION_PATH = SRC_PATH / "localisation.yaml"
SETTINGS_PATH = RESOURCES_PATH / "settings.yaml"
PRESETS_PATH = RESOURCES_PATH / "presets.yaml"
VERSIONS_PATH = RESOURCES_PATH / "versions.yaml"
MANIFESTS_PATH = RESOURCES_PATH / "manifests"
OPTIONS_PATH = RESOURCES_PATH / "options"
