import copy
from dataclasses import dataclass
import logging
from pathlib import Path

logger = logging.getLogger(Path(__file__).name)


@dataclass
class RandomizationParams:
    game_path: Path
    game_version: str
    resources_path: Path
    resources: list[str]
    lua_to_edit: Path
    server_paths: list[str]
    server_items: list[str]
    triggers_to_change: dict
    files: list
    text: list
    models: list
    npc_look: list
    landscape: list
    exe: list
    lua: list


def serialize_manifest(manifest: dict,
                       checkboxes: dict,
                       game_path: str,
                       game_version: str,
                       resources_path: Path) -> RandomizationParams:
    files = []
    text = []
    models = []
    npc_look = []
    landscape = {}
    exe = {"content": []}
    lua = []

    for chkbx, state in checkboxes.items():
        if not state:
            continue

        category = manifest[chkbx]

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

    return RandomizationParams(
        game_path=Path(game_path),
        game_version=game_version,
        resources_path=resources_path,
        resources=manifest["resources_validation"],
        lua_to_edit=manifest["lua_to_edit"],
        server_paths=manifest["server_paths"],
        server_items=manifest["server_items"],
        triggers_to_change=manifest["triggers_to_change"],
        files=files,
        text=text,
        models=models,
        npc_look=npc_look,
        landscape=landscape,
        exe=exe,
        lua=lua
    )
