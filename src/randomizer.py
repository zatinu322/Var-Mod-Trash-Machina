import logging
from pathlib import Path

from errors import ManifestMissingError, ResourcesMissingError
from config import Config
from yaml_operations import YamlConfig
from yaml_schema import validate_manifest_types
from data import RESOURCES_PATH


class Randomizer():
    def __init__(self, config: Config) -> None:
        self.game_path = Path(config.game_path)
        self.game_version = config.game_version
        self.params = config.chkbxs
        manifest = YamlConfig(config.manifest)
        self.options = {}
        self.errors = 0
        self.logger = logging.getLogger("pavlik")
        if manifest.yaml:
            self.manifest = manifest.yaml
        else:
            self.logger.error(f"Unable to load {config.manifest}")
            raise ManifestMissingError(config.manifest)

        self.validate_manifest()

    def validate_manifest(self) -> bool | None:
        self.logger.info("Validating manifest.")

        if not validate_manifest_types(self.manifest):
            raise TypeError("Manifest types are not validated.")

        res_validation = self.manifest["resources_validation"]
        for file_path in res_validation:
            full_path: Path = RESOURCES_PATH / file_path
            if not full_path.exists():
                self.logger.error(f"File is missing: {full_path.resolve()}")
                raise ResourcesMissingError(full_path)

        xml_validation = [path for path in self.manifest["server_paths"]]
        triggers_info = self.manifest["triggers_to_change"]
        for k in triggers_info:
            xml_validation.append(k)
        xml_validation.append(self.manifest["lua_to_edit"])

        for file_path in xml_validation:
            full_path = self.game_path / file_path
            if not full_path.exists():
                self.logger.error(f"File is missing: {full_path.resolve()}")
                raise ResourcesMissingError(full_path)

        game_validation = self.manifest["version_validation"]
        if not game_validation:
            self.logger.info(
                "Additional game validation is not specified. Skipping."
            )
            return True
        else:
            raise NotImplementedError()

        # TODO: Add validating to str and list

        # if isinstance(game_validation, list):
        #     for file_path in game_validation:
        #         full_path = self.game_path / file_path
        #         if not full_path.exists():
        #             self.logger.error(
        #                 f"File is missing: {full_path.resolve()}"
        #             )
        #             raise ResourcesMissingError(full_path)
        # elif isinstance(game_validation, str):
        #     mod_manifest = YamlConfig(game_validation)
        #     ic(mod_manifest.yaml)
        #     raise NotImplementedError(
        #         "Validation via mod_manifest is not yet implemented."
        #     )

    def generate_working_set(self) -> dict:
        files = []
        text = []
        models = []
        npc_look = []
        landscape = []
        exe = []
        lua = []

        for chkbx, state in self.params.items():
            if not state:
                continue

            category = self.manifest[chkbx]

            match category["type"]:
                case "files":
                    files.extend(category["groups"])
                case "text":
                    text.extend(category["groups"])
                case "models":
                    models.append(category)
                case "npc_look":
                    npc_look.append(category["groups"])
                case "landscape":
                    landscape.append(category)
                case "exe":
                    exe.append(category)
                case "lua":
                    lua.append(category)

        return {
            "logger": self.logger,
            "game_path": self.game_path,
            "folder_to_copy": self.manifest["folder_to_copy"],
            "lua_to_edit": self.manifest["lua_to_edit"],
            "server_paths": self.manifest["server_paths"],
            "server_items": self.manifest["server_items"],
            "triggers_to_change": self.manifest["triggers_to_change"],
            "files": files,
            "text": text,
            "models": models,
            "npc_look": npc_look,
            "landscape": landscape,
            "exe": exe,
            "lua": lua
        }

    def report_error(self, msg: str) -> None:
        self.logger.error(msg)
        self.errors += 1

    def configure_randomization(self) -> list:
        working_set = []
        for option, groups in self.options.items():
            if not self.params.get(option, False):
                continue
            for group in groups.values():
                working_set.append(group)

        return working_set
