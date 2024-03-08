from pathlib import Path


MAIN_PATH = Path().absolute().resolve()
RESOURCES_PATH = MAIN_PATH / "resources"
LOCALIZATION_PATH = Path(
    "src/localisation/localisation.yaml"
).resolve().absolute()
SETTINGS_PATH = RESOURCES_PATH / "settings.yaml"
