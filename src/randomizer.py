import os
import logging
from errors import ManifestMissingError

logger = logging.getLogger("pavlik")

class Randomizer():
    def __init__(self, main_app) -> None:
        self.main_app = main_app
        self.config = main_app.config
        print(main_app.config.__dict__)
        if main_app.manifest:
            self.manifest = main_app.manifest.config
        else:
            raise ManifestMissingError()