from pydantic import BaseModel


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


class RandomizationLog(BaseModel):
    heading: str
    progress: RandomizationProgress
    models_render: str
    gravity: str
    fov: str


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


class RandomizationPresets(BaseModel):
    label: str
    recommended: str
    custom: str

    def get_preset(self, preset: str | None) -> str:
        if preset is None:
            raise ValueError("No key preset provided.")

        preset_text: str | None = getattr(self, preset, None)
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


class GamePathStatus(BaseModel):
    not_found: str
    valid: str
    gdp_found: str
    exe_not_found: str


class GamePathLocale(BaseModel):
    label: str
    hint: str
    browse_button: str
    status: GamePathStatus


class GameVersionLocale(BaseModel):
    label: str
    hint: str


class AppLocale(BaseModel):
    """Single language locale."""
    randomization_button: str
    powered_by: str  # TODO: Add to GUI
    rights_reserved: str  # TODO: Add to GUI
    game_path: GamePathLocale
    game_version: GameVersionLocale
    options: OptionsLocale
    log: RandomizationLog
    errors: AppErrors


class AppLocalisation(BaseModel):
    rus: AppLocale
    en: AppLocale

    def get_locale(self, language: str) -> AppLocale:
        if language == "rus":
            return self.rus
        if language == "en":
            return self.en
        raise ValueError(f"{language} language is not supported.")
