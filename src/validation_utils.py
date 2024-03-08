import logging
from pathlib import Path

from validation_data import REQUIRED_GAME_FILES, POSSIBLE_EXE_PATHS, \
    VERSIONS_INFO, NO_EXE_ALLOWED
from config import Config
from errors import ManifestMissingError, RootNotFoundError, VersionError, \
    GameNotFoundError, GDPFoundError


logger = logging.getLogger("validation")
