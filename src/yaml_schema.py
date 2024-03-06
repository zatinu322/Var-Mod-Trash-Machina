from pydantic import BaseModel


class SettingsTypes(BaseModel):
    cb_ai_vehs: bool
    cb_aim: bool
    cb_armor: bool
    cb_bkgd: bool
    cb_books_history: bool
    cb_cab_cargo: bool
    cb_clans: bool
    cb_controls: bool
    cb_crashes: bool
    cb_descriptions: bool
    cb_dialogues: bool
    cb_digits: bool
    cb_dwellers: bool
    cb_engines: bool
    cb_env_models: bool
    cb_env_textures: bool
    cb_explosions: bool
    cb_fadingmsgs: bool
    cb_fov: bool
    cb_goods_guns: bool
    cb_gravity: bool
    cb_gui_icons: bool
    cb_gui_text: bool
    cb_guns: bool
    cb_guns_lua: bool
    cb_hits: bool
    cb_horns: bool
    cb_humans: bool
    cb_landscape: bool
    cb_lightmaps: bool
    cb_maps: bool
    cb_masks: bool
    cb_music: bool
    cb_names: bool
    cb_npc_look: bool
    cb_other_sounds: bool
    cb_pl_veh: bool
    cb_quests: bool
    cb_radar: bool
    cb_radio: bool
    cb_render: bool
    cb_shooting: bool
    cb_skybox: bool
    cb_speech: bool
    cb_splashes: bool
    cb_tiles: bool
    cb_towns: bool
    cb_trees: bool
    cb_veh_skins: bool
    cb_weather: bool
    cb_wheels: bool
    game_path: str
    height: float
    is_maximized: bool
    language: str
    pos_x: float
    pos_y: float
    preset: str
    version: str
    width: float


class ManifestTypes(BaseModel):
    version_validation: bool | str | None
    resources_validation: list[str]
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
    type: str
    groups: list[list[dict[str, list[str]]]]


class TextTypes(BaseModel):
    type: str
    groups: list[list[dict[str, dict[str, str | list[str]]]]]


class TextInfoTypes(BaseModel):
    tag: str
    name: str
    text: str
    include: list[str] = None
    exclude: list[str] = None


class ModelsTypes(BaseModel):
    type: str
    tag: str
    name: str
    path: str
    groups: list[list[str]]


class BarNpcModelsTypes(BaseModel):
    type: str
    groups: list[dict[str, str | list[str]]]


class BarNpcModelsInfoTypes(BaseModel):
    file: str
    tag: str
    name: str
    prototype: str = None
    maps: list[str]
    config: list[str]


class LandscapeTypes(BaseModel):
    type: str
    file: str
    state: str
    maps: list[str]
    multiple: bool


class ExecutableTypes(BaseModel):
    type: str
    file: str
    content: str


class LuaTypes(BaseModel):
    type: str
    variable: str
    prototypes: list[list[str]] = None


def validate_types(validator: object, manifest: dict) -> None:
    validator.model_validate(validator(**manifest), strict=True)


def validate_settings_types(settings: dict) -> None:
    """
    Validates strict tags in settings.

    Raises ValidationError if validation fails.
    """
    validate_types(SettingsTypes, settings)


def validate_manifest_types(manifest: dict) -> None:
    """
    Validates strict tags in manifest.

    Raises ValidationError if validation fails.
    """
    validate_types(ManifestTypes, manifest)

    for _, trigger in manifest["triggers_to_change"].items():
        validate_types(
            TriggersToChangeTypes,
            trigger
        )

    for files_category in [
        "cb_maps", "cb_digits", "cb_splashes", "cb_bkgd",
        "cb_clans", "cb_gui_icons", "cb_radar", "cb_goods_guns",
        "cb_cab_cargo", "cb_aim", "cb_music", "cb_speech",
        "cb_radio", "cb_crashes", "cb_explosions", "cb_engines",
        "cb_horns", "cb_hits", "cb_shooting", "cb_other_sounds",
        "cb_env_textures", "cb_masks", "cb_veh_skins",
        "cb_lightmaps", "cb_skybox", "cb_tiles",
    ]:
        validate_types(FilesTypes, manifest[files_category])

    for text_category in [
        "cb_names", "cb_dialogues", "cb_quests", "cb_controls",
        "cb_fadingmsgs", "cb_gui_text", "cb_books_history",
        "cb_descriptions", "cb_weather"
    ]:
        validate_types(TextTypes, manifest[text_category])
        for groups in manifest[text_category]["groups"]:
            for group in groups:
                for _, xml in group.items():
                    validate_types(TextInfoTypes, xml)

    for models_category in [
        "cb_env_models", "cb_towns", "cb_guns", "cb_trees",
        "cb_wheels", "cb_humans"
    ]:
        validate_types(ModelsTypes, manifest[models_category])

    validate_types(BarNpcModelsTypes, manifest["cb_npc_look"])

    for look in manifest["cb_npc_look"]["groups"]:
        validate_types(BarNpcModelsInfoTypes, look)

    validate_types(LandscapeTypes, manifest["cb_landscape"])

    for exe_category in [
        "cb_render", "cb_gravity", "cb_fov", "cb_armor",
    ]:
        validate_types(ExecutableTypes, manifest[exe_category])

    for lua_category in [
        "cb_guns_lua", "cb_ai_vehs", "cb_dwellers", "cb_pl_veh",
    ]:
        validate_types(LuaTypes, manifest[lua_category])
