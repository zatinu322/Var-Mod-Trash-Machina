from pydantic import BaseModel, Field

from ._shared import model_config


class AppErrors(BaseModel):
    no_game_path: str
    not_absolute_path: str
    game_path_missing: str
    not_game_dir: str
    exe_not_found: str
    incorrect_version_exe: str
    incorrect_version_mod: str
    compatch_no_fov: str
    manifest_missing: str
    file_missing: str
    incorrect_types: str
    mods_found: str
    mod_not_found: str
    randomization_aborted: str

    model_config = model_config


class RandomizationProgress(BaseModel):
    start: str
    validation: str
    copying: str
    prepare: str
    files: str
    text: str
    models: str
    barnpcs: str
    landscape: str
    no_landscape: str
    executable: str
    lua: str
    done_full: str
    ok: str
    done: str
    nothing: str

    model_config = model_config


class RandomizationLog(BaseModel):
    heading: str
    progress: RandomizationProgress
    models_render: str
    gravity: str
    fov: str

    model_config = model_config


class OptionCheckboxes(BaseModel):
    maps: str
    digits: str
    splashes: str
    bkgd: str
    clans: str
    gui_icons: str
    radar: str
    goods_guns: str
    cab_cargo: str
    aim: str
    names: str
    dialogues: str
    quests: str
    controls: str
    fadingmsgs: str
    gui_text: str
    books_history: str
    descriptions: str
    music: str
    speech: str
    radio: str
    crashes: str
    explosions: str
    engines: str
    horns: str
    hits: str
    shooting: str
    other_sounds: str
    env_models: str
    towns: str
    guns: str
    trees: str
    npc_look: str
    wheels: str
    humans: str
    dwellers: str
    env_textures: str
    masks: str
    veh_skins: str
    lightmaps: str
    skybox: str
    tiles: str
    weather: str
    landscape: str
    ai_vehs: str
    pl_veh: str
    guns_lua: str
    render: str
    gravity: str
    fov: str
    armor: str

    model_config = model_config


class RandomizationPresets(BaseModel):
    label: str
    names: dict[str, str] = Field(default_factory=dict)

    model_config = model_config

    def get_preset(self, preset: str | None) -> str:
        if preset is None:
            raise ValueError("No key preset provided.")

        preset_text = self.names.get(preset, None)
        if preset_text is not None:
            return preset_text

        raise ValueError(f"No translation found for {preset} preset.")


class OptionsLocale(BaseModel):
    heading: str
    presets: RandomizationPresets
    select_all_button: str
    deselect_all_button: str

    icons: str
    text: str
    sounds: str
    models: str
    textures: str
    other: str
    executable: str

    checkboxes: OptionCheckboxes

    model_config = model_config


class GamePathStatus(BaseModel):
    in_progress: str
    not_found: str
    valid: str
    gdp_found: str
    exe_not_found: str

    model_config = model_config


class GamePathLocale(BaseModel):
    label: str
    hint: str
    browse_button: str
    status: GamePathStatus

    model_config = model_config


class GameVersionLocale(BaseModel):
    label: str
    hint: str

    model_config = model_config


class AppLocale(BaseModel):
    """Single language locale."""
    name: str
    randomization_button: str
    powered_by: str  # TODO: Add to GUI
    rights_reserved: str  # TODO: Add to GUI
    game_path: GamePathLocale
    game_version: GameVersionLocale
    options: OptionsLocale
    log: RandomizationLog
    errors: AppErrors

    model_config = model_config


class AppLocalisation(BaseModel):
    rus: AppLocale
    en: AppLocale

    model_config = model_config

    @property
    def all(cls) -> dict[str, AppLocale]:
        return {
            cls.rus.name: cls.rus,
            cls.en.name: cls.en,
        }
