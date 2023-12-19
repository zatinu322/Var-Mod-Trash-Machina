import logging
from errors import ManifestMissingError
from config import Config
from yaml_operations import YamlConfig

from pathlib import Path

logger = logging.getLogger("pavlik")

class Randomizer():
    def __init__(self, config: Config) -> None:
        self.game_path = Path(config.game_path)
        self.game_version = config.game_version
        self.params = config.chkbxs
        manifest = YamlConfig(config.manifest)
        self.options = {}
        self.errors = 0
        if manifest.yaml:
            self.manifest = manifest.yaml
        else:
            raise ManifestMissingError(config.manifest)
    
    def report_error(self, msg: str) -> None:
        logger.error(msg)
        self.errors += 1
    
    def configure_randomization(self):
        working_set = []
        for option, groups in self.options.items():
            if not self.params.get(option, False):
                continue
            for group in groups.values():
                working_set.append(group)
        
        return working_set