from pydantic import BaseModel, ValidationError
from icecream import ic


class ManifestTypes(BaseModel):
    version_validation: bool | str | None
    resources_validation: list[str]
    folder_to_copy: str
    lua_to_edit: str
    server_paths: list[str]
    server_items: list[str | dict[str, str]]
    triggers_to_change: dict[str, dict[str, str]]

    cb_maps: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_digits: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_splashes: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_bkgd: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_clans: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_gui_icons: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_radar: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_goods_guns: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_cab_cargo: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_aim: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_music: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_speech: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_radio: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_crashes: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_explosions: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_engines: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_horns: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_hits: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_shooting: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_other_sounds: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_env_textures: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_masks: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_veh_skins: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_lightmaps: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_skybox: dict[str, str | list[list[dict[str, list[str]]]]]
    cb_tiles: dict[str, str | list[list[dict[str, list[str]]]]]

    cb_names: dict[
        str, str | list[list[dict[str, dict[str, str | list[str]]]]]
    ]
    cb_dialogues: dict[
        str, str | list[list[dict[str, dict[str, str | list[str]]]]]
    ]
    cb_quests: dict[
        str, str | list[list[dict[str, dict[str, str | list[str]]]]]
    ]
    cb_controls: dict[
        str, str | list[list[dict[str, dict[str, str | list[str]]]]]
    ]
    cb_fadingmsgs: dict[
        str, str | list[list[dict[str, dict[str, str | list[str]]]]]
    ]
    cb_gui_text: dict[
        str, str | list[list[dict[str, dict[str, str | list[str]]]]]
    ]
    cb_books_history: dict[
        str, str | list[list[dict[str, dict[str, str | list[str]]]]]
    ]
    cb_descriptions: dict[
        str, str | list[list[dict[str, dict[str, str | list[str]]]]]
    ]
    cb_weather: dict[
        str, str | list[list[dict[str, dict[str, str | list[str]]]]]
    ]

    cb_env_models: dict[str, str | list[list[str]]]
    cb_towns: dict[str, str | list[list[str]]]
    cb_guns: dict[str, str | list[list[str]]]
    cb_trees: dict[str, str | list[list[str]]]
    cb_wheels: dict[str, str | list[list[str]]]
    cb_humans: dict[str, str | list[list[str]]]

    cb_npc_look: dict[str, str | list[dict[str, str | list[str]]]]

    cb_landscape: dict[str, str | list[str] | bool]

    cb_render: dict[str, str]
    cb_gravity: dict[str, str]
    cb_fov: dict[str, str]
    cb_armor: dict[str, str]

    cb_guns_lua: dict[str, str | list[list[str]]]
    cb_ai_vehs: dict[str, str | list[list[str]]]
    cb_dwellers: dict[str, str | list[list[str]]]
    cb_pl_veh: dict[str, str | list[list[str]]]


class TriggersToChangeTypes(BaseModel):
    name: str
    script: str


class FilesTypes(BaseModel):
    cb_maps: dict[str, list[dict[str, list[str]]]]
    cb_digits: dict[str, list[dict[str, list[str]]]]
    cb_splashes: dict[str, list[dict[str, list[str]]]]
    cb_bkgd: dict[str, list[dict[str, list[str]]]]
    cb_clans: dict[str, list[dict[str, list[str]]]]
    cb_gui_icons: dict[str, list[dict[str, list[str]]]]
    cb_radar: dict[str, list[dict[str, list[str]]]]
    cb_goods_guns: dict[str, list[dict[str, list[str]]]]
    cb_cab_cargo: dict[str, list[dict[str, list[str]]]]
    cb_aim: dict[str, list[dict[str, list[str]]]]
    cb_music: dict[str, list[dict[str, list[str]]]]
    cb_speech: dict[str, list[dict[str, list[str]]]]
    cb_radio: dict[str, list[dict[str, list[str]]]]
    cb_crashes: dict[str, list[dict[str, list[str]]]]
    cb_explosions: dict[str, list[dict[str, list[str]]]]
    cb_engines: dict[str, list[dict[str, list[str]]]]
    cb_horns: dict[str, list[dict[str, list[str]]]]
    cb_hits: dict[str, list[dict[str, list[str]]]]
    cb_shooting: dict[str, list[dict[str, list[str]]]]
    cb_other_sounds: dict[str, list[dict[str, list[str]]]]
    cb_env_textures: dict[str, list[dict[str, list[str]]]]
    cb_masks: dict[str, list[dict[str, list[str]]]]
    cb_veh_skins: dict[str, list[dict[str, list[str]]]]
    cb_lightmaps: dict[str, list[dict[str, list[str]]]]
    cb_skybox: dict[str, list[dict[str, list[str]]]]
    cb_tiles: dict[str, list[dict[str, list[str]]]]


class TextTypes(BaseModel):
    tag: str
    name: str
    text: str
    include: list[str] = None
    exclude: list[str] = None


class ModelsTypes(BaseModel):
    tag: str
    name: str
    models: list[str]


class BarNpcModelsTypes(BaseModel):
    file: str
    tag: str
    name: str
    prototype: str = None
    maps: list[str]
    config: list[str]


class LandscapeTypes(BaseModel):
    file: str
    state: str
    maps: list[str]
    multiple: bool


class ExecutableTypes(BaseModel):
    file: str
    cb_render: str
    cb_gravity: str
    cb_fov: str
    cb_armor: str


class LuaTypes(BaseModel):
    variable: str
    prototypes: dict[str, list[str]] = None


def validate_types(validator: object, manifest: dict) -> bool:
    validator.model_validate(validator(**manifest), strict=True)
    return True


def validate_manifest_types(manifest: dict) -> bool:
    try:
        validate_types(ManifestTypes, manifest)

    #     for _, file_info in data["triggers_to_change"].items():
    #         validate_types(TriggersToChangeTypes, file_info)

    #     validate_types(FilesTypes, data["files"])

    except ValidationError as e:
        ic(e)
        return False
    else:
        return True


if __name__ == "__main__":

    file = "resources\\manifests\\new_manifest_steam.yaml"

    validate_manifest_types(file)
# user = ManifestTypes(**data)

# try:
#     user.model_validate(ManifestTypes(**data), strict=True)
# except ValidationError as e:
#     ic(e.errors())

# for _, v in data["text"].items():
#     for _, v1 in v.items():
#         for _, v2 in v1.items():
#             a = TextTypes(**v2)
#             a.model_validate(a, strict=True)

# for _, v in data["models"].items():
#     for _, v1 in v.items():
#         for _, v2 in v1.items():
#             a = ModelsTypes(**v2)
#             a.model_validate(a, strict=True)

# for _, v in data["bar_npc_models"].items():
#     for _, v1 in v.items():
#         a = BarNpcModelsTypes(**v1)
#         a.model_validate(a, strict=True)

# for _, v in data["landscape"].items():
#     for _, v1 in v.items():
#         a = LandscapeTypes(**v1)
#         a.model_validate(a, strict=True)

# a = ExecutableTypes(**data["executable"])
# a.model_validate(a, strict=True)

# for _, v in data["lua"].items():
#     a = LuaTypes(**v)
#     a.model_validate(a, strict=True)

# triggers = Files(**data["files"])
# triggers.model_validate(triggers, strict=True)
