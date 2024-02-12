import logging
import copy
from pathlib import Path

from errors import ManifestMissingError, ResourcesMissingError, \
    ModsFoundError, ModNotFoundError
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
        self.errors = 0
        self.logger = logging.getLogger("pavlik")
        if manifest.yaml:
            self.manifest = manifest.yaml
        else:
            self.logger.error(f"Unable to load {config.manifest}")
            raise ManifestMissingError(config.manifest)

        if "options" in dir(config):
            options = YamlConfig(config.options)
            if options.yaml:
                self.options = options.yaml
            else:
                self.logger.error(f"Unable to load {config.options}")
                raise ManifestMissingError(config.options)

        self.validate_manifest()

    def validate_manifest(self) -> bool | None:
        self.logger.info("Validating manifest.")

        validate_manifest_types(self.manifest)

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
        elif isinstance(game_validation, str):
            mod_manifest_path = self.game_path / "data" / game_validation
            if not mod_manifest_path.exists():
                raise ResourcesMissingError(mod_manifest_path)

            mod_manifest = YamlConfig(mod_manifest_path)

            match self.game_version:
                case "cp114" | "cr114":
                    if self.game_version == "cp114":
                        mods_amount = 1
                    elif self.game_version == "cr114":
                        mods_amount = 2

                    if len(mod_manifest.yaml) > mods_amount:
                        keys = list(mod_manifest.yaml.keys())
                        raise ModsFoundError(keys[:-mods_amount])

                    if self.game_version == "cp114":
                        return True

                case "isl12cp" | "isl12cr":
                    if "ImprovedStoryline" not in mod_manifest.yaml:
                        raise ModNotFoundError("Improved Storyline v1.2")

                    isl_ver = mod_manifest.yaml["ImprovedStoryline"]["version"]

                    if isl_ver not in ["1.2", "1.2 HD"]:
                        raise ModNotFoundError("Improved Storyline v1.2")

                    if self.game_version == "isl12cp":
                        mods_amount = 2
                    elif self.game_version == "isl12cr":
                        mods_amount = 3

                    if len(mod_manifest.yaml) > mods_amount:
                        keys = list(mod_manifest.yaml.keys())
                        raise ModsFoundError(keys[:-mods_amount])

                    if self.game_version == "isl12cp":
                        return True

            # update manifest based on installed options
            match self.game_version:
                case "cr114" | "isl12cr":
                    for mod, opt in mod_manifest.yaml.items():
                        if mod == "community_remaster":
                            if opt["hd_vehicle_models"] == "yes" \
                            and opt["ost_remaster"] == "yes":
                                installed = "ost_and_models"
                            elif not opt["hd_vehicle_models"] == "yes" \
                            and opt["ost_remaster"] == "yes":
                                installed = "only_ost"
                            elif opt["hd_vehicle_models"] == "yes" \
                            and not opt["ost_remaster"] == "yes":
                                installed = "only_models"

            self.manifest.update(
                self.options[installed]
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
        landscape = {}
        exe = {"content": []}
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
                    npc_look.extend(category["groups"])
                case "landscape":
                    landscape = copy.copy(category)
                case "exe":
                    exe["content"].append(category["content"])
                    exe["file"] = category["file"]
                case "lua":
                    lua.append(category)

        return {
            "logger": self.logger,
            "game_path": self.game_path,
            "game_version": self.game_version,
            "resources": self.manifest["resources_validation"],
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
