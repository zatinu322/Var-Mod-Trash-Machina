import logging
from errors import ManifestMissingError, ResourcesMissingError, ManifestKeyError
from config import Config
from yaml_operations import YamlConfig
from data import RESOURCES_PATH
from icecream import ic

from pathlib import Path

logger = logging.getLogger("pavlik")

class Randomizer():
    def __init__(self, config: Config, need_validation: bool = False) -> None:
        self.game_path = Path(config.game_path)
        self.game_version = config.game_version
        self.params = config.chkbxs
        manifest = YamlConfig(config.manifest)
        self.options = {}
        self.errors = 0
        self.logger = logger
        if manifest.yaml:
            self.manifest = manifest.yaml
        else:
            self.logger.error(f"Unable to load {config.manifest}")
            raise ManifestMissingError(config.manifest)
        
        if need_validation: self.validate_manifest()
        
    def validate_manifest(self) -> bool | None:
        """Validates files and key types from resources_validation,
        version_validation and LuaToEdit keys from manifest. 
        Returns True if all is valid, else None."""
        self.logger.info("Validating manifest.")

        res_validation = self.manifest.get("resources_validation", False)
        if not(isinstance(res_validation, list)):
            self.logger.error(f"Incorrect data type for \"resources_validation\" key: list expected, got {type(res_validation)}")
            raise ManifestKeyError("resources_validation", type(res_validation))

        for file_path in res_validation:
            full_path: Path = RESOURCES_PATH / file_path
            if not(full_path.exists()):
                self.logger.error(f"File is missing: {full_path.resolve()}")
                raise ResourcesMissingError(full_path)
        
        lua_validation = self.manifest.get("LuaToEdit", None)
        if not lua_validation or not(isinstance(lua_validation, str)):
            self.logger.error(f"Incorrect data type for \"LuaToEdit\" key: str expected, got {type(res_validation)}")
            raise ManifestKeyError("LuaToEdit", type(lua_validation))
        
        full_path = RESOURCES_PATH / lua_validation
        if not full_path.exists():
            self.logger.error(f"File is missing: {full_path.resolve()}")
            raise ResourcesMissingError(full_path)

        game_validation = self.manifest.get("version_validation", False)
        if not game_validation:
            self.logger.info("Additional game validation is not specified. Skipping.")
            return True

        if isinstance(game_validation, list):
            for file_path in game_validation:
                full_path = self.game_path / file_path
                if not full_path.exists():
                    self.logger.error(f"File is missing: {full_path.resolve()}")
                    raise ResourcesMissingError(full_path)
        elif isinstance(game_validation, str):
            mod_manifest = YamlConfig(game_validation)
            ic(mod_manifest.yaml)
            raise NotImplementedError("Validation via mod_manifest is not yet implemented.")
        
        return True
    
    def report_error(self, msg: str) -> None:
        logger.error(msg)
        self.errors += 1
    
    def configure_randomization(self) -> list:
        working_set = []
        for option, groups in self.options.items():
            if not self.params.get(option, False):
                continue
            for group in groups.values():
                working_set.append(group)
        
        return working_set