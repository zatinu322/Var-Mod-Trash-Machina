import asyncio
import logging
from pathlib import Path

from flet import (
    Colors,
    CrossAxisAlignment,
    DropdownOption,
    Event,
    FilePicker,
    MainAxisAlignment,
    Padding,
    Page,
    ScrollMode,
    ThemeMode,
    WindowEvent,
    WindowEventType,
)

from exceptions import ExecutableNotFoundError, GameNotFoundError, GDPFoundError, RootNotFoundError
from gui.constants import (
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_POS_X,
    DEFAULT_WINDOW_POS_Y,
    DEFAULT_WINDOW_WIDTH,
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
from helpers.yaml_utils import save_yaml, serialize_yaml
from schemas.app_config import AppConfig
from schemas.localisation import AppLocalisation
from schemas.presets import Preset, Presets, PresetTitle
from schemas.versions import Versions
from validators import validate_game_directory

logger = logging.getLogger(__name__)


class RandomizerApp(RandomizerGUI):
    def __init__(self, app_config: AppConfig, *args, **kwargs) -> None:
        self.app_config = app_config

        super().__init__(*args, **kwargs)

    def init(self) -> None:
        super().init()

        # store path validation task to prevent excessive disc load
        self._path_validation_task = None

        self.presets = {
            preset.name: preset
            for preset in serialize_yaml(yaml_path=PRESETS_PATH, validation_model=Presets).presets
        }
        self.presets["custom"] = Preset(name="custom", title=PresetTitle(rus="Пользовательский", en="Custom"))
        self.versions = serialize_yaml(yaml_path=VERSIONS_PATH, validation_model=Versions)

        self.localisations = serialize_yaml(LOCALISATION_PATH, validation_model=AppLocalisation)
        # add presets locale
        self.localisations.rus.options.presets.names = {name: preset.title.rus for name, preset in self.presets.items()}
        self.localisations.en.options.presets.names = {name: preset.title.en for name, preset in self.presets.items()}

        self.locale = self.localisations.all[self.app_config.language]

        self.rus_button.on_click = self.switch_locale
        self.eng_button.on_click = self.switch_locale

        self.options.select_all_button.on_click = self.set_checkboxes_status
        self.options.deselect_all_button.on_click = self.set_checkboxes_status

        self.path_browser.path_field.on_change = self.update_path_status
        self.path_browser.browse_button.on_click = self.browse_game_path

        self.version.on_select = self.switch_version

        self.options.preset.on_select = self.apply_preset
        for checkbox in self.options.checkboxes.all.values():
            checkbox.on_change = self.switch_preset_to_custom

        self.randomization_button.on_click = self.start_randomization
        self.randomization_overlay.ok_button.on_click = self.close_randomization_overlay

        # TODO: add justfile for linting and tests
        # TODO: info container logging
        # TODO: base validation of manifests and options

    async def retranslate_ui(self) -> None:
        retranslate_main_widgets(self)
        retranslate_path_browser(self.path_browser, self.locale.game_path)
        retranslate_app_options(self.options, self.locale.options)
        retranslate_checkboxes(self.options.checkboxes, self.locale.options.checkboxes)

        self.update()

        await self._update_path_status(self.path_browser.path_field.value)

    async def switch_locale(self, e: Event) -> None:
        self.locale = self.localisations.all[e.control.data]
        await self.retranslate_ui()

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
        await self._update_path_status(path=game_path)
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

    def switch_version(self, e: Event) -> None:
        version = self.versions.get_by_name(str(e.data))
        app_checkboxes = self.options.checkboxes.all
        if restricted_options := version.restricted_options:
            self.switch_preset_to_custom()
            for option in restricted_options:
                checkbox = app_checkboxes[option]
                checkbox.disabled = True
                checkbox.value = False

        self.update()

    def switch_preset_to_custom(self) -> None:
        """Switch preset to custom when checkbox value change."""
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

    async def apply_config(self) -> None:
        self.options.preset.value = self.app_config.preset
        self.path_browser.path_field.value = self.app_config.game_path
        self.version.value = self.app_config.game_version
        version = self.versions.get_by_name(self.version.value)

        app_checkboxes = self.options.checkboxes.all
        for data, checkbox in app_checkboxes.items():
            checkbox.value = getattr(self.app_config.checkboxes, data)
            checkbox.disabled = data in version.restricted_options

        await self._update_path_status(self.path_browser.path_field.value)

        self.update()
        self.page.update()

    def update_app_config(self) -> None:
        self.app_config.window.pos_x = self.page.window.left or DEFAULT_WINDOW_POS_X
        self.app_config.window.pos_y = self.page.window.top or DEFAULT_WINDOW_POS_Y
        self.app_config.window.is_maximized = self.page.window.maximized
        self.app_config.window.width = self.page.window.width or DEFAULT_WINDOW_WIDTH
        self.app_config.window.height = self.page.window.height or DEFAULT_WINDOW_HEIGHT

        self.app_config.language = self.locale.name

        self.app_config.preset = self.options.preset.value or ""
        app_checkboxes = self.app_config.checkboxes
        for data, checkbox in self.options.checkboxes.all.items():
            setattr(app_checkboxes, data, checkbox.value)

        self.app_config.game_path = self.path_browser.path_field.value
        self.app_config.game_version = self.version.value or ""

    def update_path_status(self, e: Event) -> None:
        if task := self._path_validation_task:
            task.cancel()
        self._path_validation_task = asyncio.ensure_future(self._update_path_status(e.data))

    async def _update_path_status(self, path: str | None) -> None:
        if not path:
            self.path_browser.status.value = ""
            self.update()
            return

        self.path_browser.progress_ring.visible = True
        self.path_browser.status.value = self.locale.game_path.status.in_progress
        self.path_browser.status.color = Colors.WHITE
        self.path_browser.update()

        try:
            await asyncio.sleep(2)

            validate_game_directory(Path(path.strip()))
            self.path_browser.status.value = self.locale.game_path.status.valid
            self.path_browser.status.color = Colors.GREEN
        except ExecutableNotFoundError:
            self.path_browser.status.value = self.locale.game_path.status.exe_not_found
            self.path_browser.status.color = Colors.RED
        except (RootNotFoundError, GameNotFoundError):
            self.path_browser.status.value = self.locale.game_path.status.not_found
            self.path_browser.status.color = Colors.RED
        except GDPFoundError:
            self.path_browser.status.value = self.locale.game_path.status.gdp_found
            self.path_browser.status.color = Colors.RED
        except asyncio.CancelledError:
            pass

        self.path_browser.progress_ring.visible = False
        self.update()

    def show_randomization_overlay(self) -> None:
        self.page.overlay.append(self.randomization_overlay)

        # reset previous content if any
        self.randomization_overlay.log.controls.clear()
        self.randomization_overlay.progress_bar.value = 0
        self.randomization_overlay.ok_button.disabled = True

        self.page.update()

    def close_randomization_overlay(self, _: Event) -> None:
        self.page.overlay.remove(self.randomization_overlay)
        self.page.update()

    def start_randomization(self, _: Event) -> None:
        self.update_app_config()
        self.show_randomization_overlay()
        self.randomization_overlay.ok_button.disabled = False  # FIXME
        self.randomization_overlay.update()


async def start_app(page: Page) -> None:
    async def save_config(e: WindowEvent) -> None:
        if e.type == WindowEventType.CLOSE:
            randomizer_app.update_app_config()
            save_yaml(SETTINGS_PATH, randomizer_app.app_config)
            await page.window.destroy()

    app_config = serialize_yaml(yaml_path=SETTINGS_PATH, validation_model=AppConfig)

    page.title = FULL_NAME

    page.vertical_alignment = MainAxisAlignment.START
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    page.window.prevent_close = True
    page.window.on_event = save_config

    page.window.min_width = 832
    if app_config.window.is_maximized:
        page.window.maximized = True
    else:
        page.window.width = app_config.window.width
        page.window.height = app_config.window.height
        page.window.left = app_config.window.pos_x
        page.window.top = app_config.window.pos_y

    page.bgcolor = "#3d5a68"
    page.theme_mode = ThemeMode.DARK
    page.padding = Padding.all(0)

    page.scroll = ScrollMode.AUTO

    logo_path = Path(__file__).parent.parent / "assets" / "rpg_logo.ico"
    page.window.icon = str(logo_path.resolve())

    logger.info("Running %s in %s.", FULL_NAME, MAIN_PATH.resolve())
    logger.info("Source code at %s.", SRC_PATH.resolve())

    randomizer_app = RandomizerApp(
        app_config=app_config,
        width=800,
        expand=True,  # enable page scroll
    )
    page.add(randomizer_app)

    # we need to do this only after control is added on page
    randomizer_app.update_presets()
    randomizer_app.update_versions()
    await randomizer_app.retranslate_ui()
    randomizer_app.apply_preset()
    await randomizer_app.apply_config()
