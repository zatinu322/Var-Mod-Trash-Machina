import logging
from pathlib import Path

from flet import (
    ControlEvent,
    CrossAxisAlignment,
    DropdownOption,
    Event,
    FilePicker,
    MainAxisAlignment,
    Padding,
    Page,
    ScrollMode,
    ThemeMode,
)

from gui.constants import (
    FULL_NAME,
    LOCALISATION_PATH,
    MAIN_PATH,
    PRESETS_PATH,
    SETTINGS_PATH,
    SRC_PATH,
    VERSIONS_PATH,
)
from gui.layout import RandomizerGUI
from gui.translation import (
    retranslate_app_options,
    retranslate_checkboxes,
    retranslate_main_widgets,
    retranslate_path_browser,
)
from helpers.yaml_utils import serialize_yaml
from schemas.app_config import AppConfig
from schemas.localisation import AppLocalisation
from schemas.presets import Preset, Presets, PresetTitle
from schemas.versions import Versions

logger = logging.getLogger(__name__)


class RandomizerApp(RandomizerGUI):
    def init(self) -> None:
        super().init()

        self.app_config = AppConfig.model_validate(serialize_yaml(yaml_path=SETTINGS_PATH))
        self.presets = {
            preset.name: preset
            for preset in Presets.model_validate(
                serialize_yaml(yaml_path=PRESETS_PATH),
            ).presets
        }
        self.presets["custom"] = Preset(name="custom", title=PresetTitle(rus="Пользовательский", en="Custom"))
        self.versions = Versions.model_validate(serialize_yaml(yaml_path=VERSIONS_PATH))

        self.localisations = AppLocalisation.model_validate(serialize_yaml(LOCALISATION_PATH))
        # adjust localisation with existing presets
        self.localisations.rus.options.presets.names = {name: preset.title.rus for name, preset in self.presets.items()}
        self.localisations.en.options.presets.names = {name: preset.title.en for name, preset in self.presets.items()}

        self.locale = self.localisations.get_locale(self.app_config.language)

        self.rus_button.on_click = self.switch_locale
        self.eng_button.on_click = self.switch_locale

        self.options.select_all_button.on_click = self.set_checkboxes_status
        self.options.deselect_all_button.on_click = self.set_checkboxes_status

        self.path_browser.browse_button.on_click = self.browse_game_path

        self.options.preset.on_select = self.apply_preset
        for checkbox in self.options.checkboxes.all.values():
            checkbox.on_change = self.switch_preset_to_custom

        # TODO: base validation of manifests and options
        # TODO: apply_config
        # TODO: update path status on translation
        # TODO: update checkboxes on version pick
        # TODO: update checkboxes on config apply
        # TODO: update status on path change
        # TODO: update status on config apply
        # TODO: save config on app close
        # TODO: show/close randomization log

    def retranslate_ui(self) -> None:
        retranslate_main_widgets(self)
        retranslate_path_browser(self.path_browser, self.locale.game_path)
        retranslate_app_options(self.options, self.locale.options)
        retranslate_checkboxes(self.options.checkboxes, self.locale.options.checkboxes)

        self.update()

    def switch_locale(self, e: Event) -> None:
        self.locale = self.localisations.get_locale(e.control.data)
        self.retranslate_ui()

    def set_checkboxes_status(self, e: Event) -> None:
        """Select or deselect all checkboxes."""
        control_data: bool = e.control.data
        if control_data is None:
            raise ValueError("SelectionButton does not contain data.")

        for checkbox in [checkbox for checkbox in self.options.checkboxes.all.values() if not checkbox.disabled]:
            checkbox.value = control_data

        self.switch_preset_to_custom()

    async def browse_game_path(self, _: Event) -> None:
        game_path = await FilePicker().get_directory_path()
        if game_path:
            self.path_browser.path_field.value = game_path
            self.update()

    def update_presets(self) -> None:
        self.options.preset.options = [
            DropdownOption(key=preset.name, text=preset.name)
            for preset in self.presets.values()
        ]
        self.update()

    def update_versions(self) -> None:
        self.version.options = [
            DropdownOption(key=version.name, text=version.title)
            for version in self.versions.versions
        ]
        self.update()

    def switch_preset_to_custom(self) -> None:
        """Switch preset to custom when on checkbox value change."""
        self.options.preset.value = "custom"

    def apply_preset(self) -> None:
        preset_key = self.options.preset.value
        if preset_key is None:
            return
        preset = self.presets.get(preset_key, None)
        if not preset:
            logger.error("No preset found for key %s.", preset_key)
            return

        preset_checkboxes = preset.checkboxes.model_dump(exclude_unset=True)
        for checkbox in self.options.checkboxes.all.values():
            if checkbox.disabled:
                continue

            value = preset_checkboxes.get(checkbox.data, None)
            if value is None:
                continue

            checkbox.value = value

        self.update()


def start_app(page: Page) -> None:
    def window_resized(_: ControlEvent) -> None:
        # TODO: define whether I need this now or not
        ...

    def save_config():
        # TODO: save config on close
        ...

    def create_error_container():
        # TODO: create error container when problems occured
        ...

    page.title = FULL_NAME

    page.vertical_alignment = MainAxisAlignment.START
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    page.window.width = 880
    page.window.min_width = 832
    page.window.height = 706

    page.bgcolor = "#3d5a68"
    page.theme_mode = ThemeMode.DARK
    page.padding = Padding.all(0)

    page.scroll = ScrollMode.AUTO

    logo_path = Path(__file__).parent.parent / "assets" / "rpg_logo.ico"
    page.window.icon = str(logo_path.resolve())

    logger.info(
        "Running %s in %s.\nSource code at %s.",
        FULL_NAME,
        MAIN_PATH.resolve(),
        SRC_PATH.resolve(),
    )

    randomizer_app = RandomizerApp(
        width=800,
        expand=True,  # enable page scroll
    )
    page.add(randomizer_app)

    # we need to do this only after control is added on page
    randomizer_app.update_presets()
    randomizer_app.update_versions()
    randomizer_app.retranslate_ui()
    randomizer_app.apply_preset()
