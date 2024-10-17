from pathlib import Path
import logging

logger = logging.getLogger(Path(__file__).name)

MAIN_PATH = Path()
SRC_PATH = Path(__file__).parent.parent
ASSETS_PATH = SRC_PATH / "assets"
RESOURCES_PATH = MAIN_PATH / "resources"
LOCALIZATION_PATH = SRC_PATH / "localisation" / "localisation.yaml"
SETTINGS_PATH = RESOURCES_PATH / "settings.yaml"
