import logging
from pathlib import Path

from pydantic import ValidationError
from flet import Page, Row, FilePicker, dropdown, ContainerTapEvent, Text, \
    FilePickerResultEvent, ControlEvent, Container, alignment, \
    MainAxisAlignment, ThemeMode, padding, app

import main_randomizer as mr
from randomizer import Randomizer
from gui import MainGui
from config import Config
from localisation import Localisation
from validation import Validation
from errors import LocalisationMissingError, RootNotFoundError, \
    GameNotFoundError, VersionError, ManifestMissingError, \
    GDPFoundError, ResourcesMissingError, ManifestKeyError, \
    ModsFoundError, ModNotFoundError
from enviroment import MAIN_PATH, SETTINGS_PATH, LOCALIZATION_PATH
from gui_info import FULL_NAME, SUPPORTED_VERSIONS, PRESETS

# from icecream import ic

logging.basicConfig(
    filename="randomizer.log",
    level=logging.INFO,
    format="[%(levelname)s][%(asctime)s]: "
           "%(message)s [%(filename)s, %(funcName)s]",
    filemode="w",
    datefmt="%m/%d/%Y %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger("randomizer")


class RandomizerWindow(MainGui):
    def __init__(
        self,
        page: Page,
        config: Config,
        locale: Localisation,
        working_width: int
    ) -> None:
        super().__init__(page, working_width)

        self.config = config
        self.locale = locale

        # different column widths for different languages
        self.opt_column_widths = {
            (self.opt_icons, self.t_icons_row): {"rus": 160, "eng": 180},
            (self.opt_text, self.t_text_row): {"rus": 210, "eng": 160},
            (self.opt_sounds, self.t_sounds_row): {"rus": 135, "eng": 110},
            (self.opt_models, self.t_models_row): {"rus": 210, "eng": 190},
            (self.opt_textures, self.t_textures_row): {"rus": 135, "eng": 125},
            (self.opt_other, self.t_other_row): {"rus": 150, "eng": 135},
            (self.opt_exe, self.t_executable_row): {"rus": 185, "eng": 165}
        }

        # TODO: Remove
        self.validate = Validation()

        # Add FilePicker to page overlay
        self.get_dir_dialog = FilePicker(on_result=self.get_dir_result)
        page.overlay.extend([self.get_dir_dialog])

    def set_widget_connections(self) -> None:
        """
        Sets `on_click` and `on_change` connections
        between controls and it's functions.
        """
        self.btn_rus.on_click = self.switch_lang
        self.btn_eng.on_click = self.switch_lang
        self.browse_btn.on_click = (
            lambda _: self.get_dir_dialog.get_directory_path()
        )
        self.btn_select_all.on_click = self.change_chkbxs_status
        self.btn_deselect_all.on_click = self.change_chkbxs_status
        self.start_randomization_btn.on_click = self.start_randomization
        self.info_cont_btn.on_click = self.close_info_cont

        self.game_path_tf.on_change = self.game_path_changed
        self.dd_preset.on_change = self.update_checkboxes_from_preset
        self.game_version_dd.on_change = self.adjust_cb_state
        for chkbx in self.chkbxs_dict:
            chkbx.on_change = self.set_custom_preset

        self.update_app()

    def fill_versions_dd(self, versions: dict) -> None:
        """
        Fills Dropdown with avaliable game versions
        from given `dict`.
        """
        for key, text in versions.items():
            self.game_version_dd.options.append(
                dropdown.Option(text=text, key=key)
            )
        self.update_app()

    def fill_presets_dd(self, presets: dict) -> None:
        """
        Fills Dropdown with avaliable presets
        from given `dict`.
        """
        for preset in presets:
            self.dd_preset.options.append(
                dropdown.Option(text=preset, key=preset)
            )

    def switch_lang(self, e: ContainerTapEvent) -> None:
        """
        Switches GUI language to provided.
        """
        match e.control:
            case self.btn_rus:
                self.locale.update_lang("rus")
                self.config.lang = "rus"
            case self.btn_eng:
                self.locale.update_lang("eng")
                self.config.lang = "eng"
        self.retranslate_ui()

    def apply_config(self):
        """
        Applies data from `self.config` to GUI.
        """
        self.page.window_left = self.config.pos_x
        self.page.window_top = self.config.pos_y
        if self.config.is_maximized:
            self.page.window_maximized = True
        elif self.config.width and self.config.height:
            self.page.window_width = self.config.width
            self.page.window_height = self.config.height

        self.locale.update_lang(self.config.lang)
        self.retranslate_ui()

        self.dd_preset.value = self.config.preset
        for k, v in self.chkbxs_dict.items():
            if not k.disabled:
                k.value = self.config.chkbxs.get(v, False)

        self.game_path_tf.value = self.config.game_path
        self.update_path_status()

        self.game_version_dd.value = self.config.game_version
        self.adjust_cb_state()

        self.update_app()

    def adjust_width(self) -> None:
        """
        Adjusts widgets width when changing localisation.
        """

        for (k, k1), v in self.opt_column_widths.items():
            k.width = v.get(self.locale.lang)
            k1.width = v.get(self.locale.lang)

        self.update_app()

    def retranslate_ui(self) -> None:
        """
        Retranslates whole GUI according to language in `self.locale`
        """
        self.expandable_options.name.value = self.locale.tr("options_title")
        self.dd_preset.label = self.locale.tr("t_presets")
        self.btn_deselect_all.text = self.locale.tr("btn_deselect_all")
        self.btn_select_all.text = self.locale.tr("btn_select_all")
        self.t_icons.value = self.locale.tr("t_icons")
        self.t_text.value = self.locale.tr("t_text")
        self.t_sounds.value = self.locale.tr("t_sounds")
        self.t_models.value = self.locale.tr("t_models")
        self.t_textures.value = self.locale.tr("t_textures")
        self.t_other.value = self.locale.tr("t_other")
        self.t_executable.value = self.locale.tr("t_executable")
        self.game_path_tf.label = self.locale.tr("game_path_tf_l")
        self.game_path_tf.hint_text = self.locale.tr("game_path_tf_h")
        self.browse_btn.text = self.locale.tr("browse_btn")
        self.game_version_dd.label = self.locale.tr("game_version_l")
        self.game_version_dd.hint_text = self.locale.tr("game_version_h")
        self.start_randomization_btn.text = self.locale.tr("randomization_btn")
        self.info_cont_heading.value = self.locale.tr("rand_info")

        for k, v in self.chkbxs_dict.items():
            k.label = self.locale.tr(v)

        for option in self.dd_preset.options:
            option.text = self.locale.tr(option.key)

        self.update_path_status()
        self.adjust_width()
        self.update_app()

    def update_app(self) -> None:
        """
        Updates all controlls used in GUI.
        """
        self.update()
        self.page.update()
        self.expandable_options.update()

    def get_dir_result(self, e: FilePickerResultEvent) -> None:
        """
        Proceeds game path from FilePicker to GUI
        and updates it's status.
        """
        if e.path:
            self.game_path_tf.value = e.path
            self.update_path_status()
            self.update_app()

    def game_path_changed(self, e: ControlEvent) -> None:
        """
        Handles every change in game path field
        (except from FilePicker) and updates path status.
        """
        self.update_path_status(e.data)

    def update_path_status(self, cur_value: str = None) -> None:
        """Updates path validation status in GUI."""
        if cur_value is None:
            cur_value = self.game_path_tf.value
        if cur_value == "":
            self.game_path_status_t.value = ""
            self.game_path_status_t.opacity = 0
            return

        game_path = Path(self.game_path_tf.value)

        try:
            validation, exe = self.validate.game_dir(game_path)
        except (RootNotFoundError, GameNotFoundError, VersionError):
            validation, exe = False, None
        except GDPFoundError:
            validation, exe = False, None
            self.game_path_status_t.color = "red"
            self.game_path_status_t.opacity = 100
            self.game_path_status_t.value = self.locale.tr("gdp_found")

        if validation:
            if exe:
                self.game_path_status_t.value = self.locale.tr("valid_path")
                self.game_path_status_t.opacity = 100
                self.game_path_status_t.color = "green"

                self.adjust_cb_state()
            else:
                self.game_path_status_t.value = self.locale.tr(
                    "valid_path_no_exe"
                )
                self.game_path_status_t.opacity = 100
                self.game_path_status_t.color = "yellow"

                self.change_cb_state(
                    True,
                    self.cb_render,
                    self.cb_fov,
                    self.cb_gravity,
                    self.cb_armor
                )
        else:
            self.game_path_status_t.color = "red"
            self.game_path_status_t.opacity = 100
            self.game_path_status_t.value = self.locale.tr("invalid_path")
        self.update_app()

    def change_chkbxs_status(self, e: ControlEvent) -> None:
        """
        Checks or unchecks all checkboxes in settings category,
        based on what bool value is provided in ControlEvent.
        """
        match e.control:
            case self.btn_select_all:
                checked = True
            case self.btn_deselect_all:
                checked = False

        for chkbx in self.chkbxs_dict:
            if not chkbx.disabled:
                chkbx.value = checked

        self.set_custom_preset()

        self.update_app()

    def show_info_cont(self) -> None:
        """
        Disables main GUI and places Container
        with human-readable randomization log.
        """
        self.page.overlay.append(self.bg_cont)
        self.page.overlay.append(self.info_cont)

        # clear all previous content if any
        self.log_container.controls.clear()
        self.progress_bar.value = 0
        self.info_cont_btn.disabled = True

    def info_cont_write(
        self,
        message: str,
        color: str | int = "white"
    ) -> None:
        """
        Adds provided message to randomization log container.
        """
        self.log_container.controls.append(
            Text(
                value=message,
                color=color
            )
        )
        self.update_app()

    def info_cont_abort(self) -> None:
        """
        Reports about aborting randomization.

        Sets Container widgets to default.
        """
        self.info_cont_write(self.locale.tr("randomization_aborted"), "red")
        self.info_cont_write(self.locale.tr("rand_OK"))

        self.info_cont_btn.disabled = False
        self.progress_bar.value = 0

        self.update_app()

    def info_cont_success(self) -> None:
        """
        Reports about successful randomization.

        Sets Container widgets to success state.
        """
        self. info_cont_write(self.locale.tr("rand_done_full"), "green")
        self.info_cont_write(self.locale.tr("rand_OK"))

        self.info_cont_btn.disabled = False
        self.progress_bar.value = 1

        self.update_app()

    def close_info_cont(self, e: ControlEvent) -> None:
        """
        Closes randomization log Container
        when pressing OK button in it.
        """
        self.page.overlay.remove(self.info_cont)
        self.page.overlay.remove(self.bg_cont)

        self.update_app()

    def update_checkboxes_from_preset(self, e: ControlEvent) -> None:
        """
        Updates checkboxes according to chosen preset.
        """
        chkbxs_config = PRESETS.get(e.data, {})
        for k, v in self.chkbxs_dict.items():
            new_value = chkbxs_config.get(v)
            if new_value is None:
                continue
            if not k.disabled:
                k.value = new_value
            else:
                k.value = False

        self.update_app()

    def adjust_cb_state(self, e: ControlEvent = None) -> None:
        """
        Updates checkboxes state (not values) according
        to chosen game_version in versions Dropdown.
        """
        match self.game_version_dd.value:
            case "cp114" | "cr114" | "isl12cp" | "isl12cr":
                self.uncheck_chkbxs(self.cb_fov)
                self.change_cb_state(True, self.cb_fov)
            case "steam":
                self.change_cb_state(
                    False,
                    self.cb_render,
                    self.cb_gravity,
                    self.cb_fov,
                    self.cb_armor
                )

    def collect_chkbxs_values(self) -> dict:
        """
        Collects current checkboxes values to dictionary.
        """
        return {v: k.value for (k, v) in self.chkbxs_dict.items()}

    def update_config(self) -> None:
        self.config.pos_x = self.page.window_left
        self.config.pos_y = self.page.window_top
        if self.page.window_maximized:
            self.config.is_maximized = True
        else:
            self.config.is_maximized = False
        self.config.width = self.page.window_width
        self.config.height = self.page.window_height
        self.config.preset = self.dd_preset.value
        self.config.game_path = self.game_path_tf.value
        self.config.game_version = self.game_version_dd.value
        chkbxs = self.collect_chkbxs_values()
        self.config.chkbxs.update(chkbxs)
        self.config.update_config()

    def set_custom_preset(self, e: ControlEvent = None) -> None:
        """
        Sets custom preset if any chechbox's value was changed.
        """
        self.dd_preset.value = "p_custom"

        self.update_app()

    def uncheck_chkbxs(self, *chkbxs):
        """
        Unchecks provided checkboxes.
        """
        for chkbx in chkbxs:
            chkbx.value = False
        self.update_config()
        self.update_app()

    def change_chkbxs_state(self, is_disabled: bool, *chkbxs) -> None:
        """
        Enables or disables provided checkboxes.
        When disables it also sets checkbox value to False.
        """
        for chkbx in chkbxs:
            chkbx.disabled = is_disabled
        self.update_config()
        self.update_app()

    def start_randomization(self, e: ControlEvent = None) -> None:
        self.update_config()
        self.show_info_cont()
        self.info_cont_write(self.locale.tr("rand_start"))

        self.info_cont_write(self.locale.tr("rand_validation"))
        try:
            validation, exe_status = self.validate.settings(self.config)
        except RootNotFoundError as no_root:
            logger.error(
                f"Unable to validate game path. {no_root} does not exists.")
            self.info_cont_write(
                f"{self.locale.tr('game_path_missing')}\n{no_root}",
                color="red"
            )
            self.info_cont_abort()
            return
        except GameNotFoundError as no_game:
            logger.error(
                "Unable to validate game path."
                f"{no_game} is missing."
            )

            self.info_cont_write(
                f"{self.locale.tr('not_game_dir')}\n{no_game}",
                color="red"
            )
            self.info_cont_abort()
            return
        except GDPFoundError as gdp_found:
            logger.error(
                "Unable to validate game path."
                f"GDP archives found: {gdp_found}"
            )

            self.info_cont_write(
                f"{self.locale.tr('gdp_found')}\n{gdp_found}",
                color="red"
            )
            self.info_cont_abort()
            return
        except VersionError:
            self.info_cont_write(
                f"{self.locale.tr('incorrect_version')}",
                color="red"
            )
            self.info_cont_abort()
            return
        except ManifestMissingError as no_manifest:
            self.info_cont_write(
                f"{self.locale.tr('manifest_missing')}\n{no_manifest}",
                color="red"
            )
            self.info_cont_abort()
            return

        match exe_status:
            case "no_exe":
                logger.warning("Randomization options related to executable \
                               randomizing will be forcibly disabled.")
                self.info_cont_write(
                    f"{self.locale.tr('is_continued')}",
                    color="yellow"
                )
                self.uncheck_chkbxs(
                    self.cb_render,
                    self.cb_armor,
                    self.cb_fov,
                    self.cb_gravity
                )
            case "no_fov":
                self.info_cont_write(
                    f"{self.locale.tr('compatch_no_fov')}",
                    color="yellow"
                )

                self.uncheck_chkbxs(self.cb_fov)

        self.progress_bar.value += 0.10

        if validation:
            try:
                randomizer = Randomizer(self.config)
                working_set = randomizer.generate_working_set()

                self.info_cont_write(self.locale.tr("rand_copy"))
                mr.copy_files(working_set)
                self.progress_bar.value += 0.10

                self.info_cont_write(self.locale.tr("rand_prepare"))
                mr.edit_files(working_set)
                self.progress_bar.value += 0.10

                self.info_cont_write(self.locale.tr("rand_files"))
                mr.randomize_files(working_set)
                # if not status:
                #     self.info_cont_write(f"{self.locale.tr('rand_nothing')}")
                # else:
                #     self.info_cont_write(f"{self.locale.tr('rand_done')}")
                self.progress_bar.value += 0.10

                self.info_cont_write(self.locale.tr("rand_text"))
                mr.randomize_text(working_set)
                self.progress_bar.value += 0.10

                self.info_cont_write(self.locale.tr("rand_models"))
                mr.randomize_models(working_set)
                self.progress_bar.value += 0.10

                self.info_cont_write(self.locale.tr("rand_barnpcs"))
                mr.randomize_barnpcs(working_set)
                self.progress_bar.value += 0.10

                self.info_cont_write(self.locale.tr("rand_landscape"))
                mr.randomize_landscape(working_set)
                self.progress_bar.value += 0.10

                self.info_cont_write(self.locale.tr("rand_executable"))
                new_exe = mr.randomize_executable(working_set)
                self.progress_bar.value += 0.10
                if new_exe:
                    for option, value in new_exe.items():
                        self.info_cont_write(
                            f"{'\t'*10}{self.locale.tr(option)}: {value}",
                            "yellow"
                        )

                self.info_cont_write(self.locale.tr("rand_lua"))
                mr.randomize_lua(working_set)
                self.progress_bar.value += 0.10

                self.info_cont_success()
            except ValidationError as validation_error:
                self.info_cont_write(
                    self.locale.tr('incorrect_types'),
                    "red"
                )
                self.info_cont_abort()
                for error in validation_error.errors():
                    logger.error(error)
            except ManifestMissingError as bad_manifest:
                self.info_cont_write(
                    f"{self.locale.tr('bad_manifest')}\n{bad_manifest}",
                    "red"
                )
                self.info_cont_abort()
            except ModsFoundError as mods_found:
                self.info_cont_write(
                    f"{self.locale.tr('mods_found')}:\n{mods_found}",
                    "red"
                )
                self.info_cont_abort()
            except ModNotFoundError as mod_not_found:
                self.info_cont_write(
                    f"{self.locale.tr('mod_not_found')}:\n{mod_not_found}",
                    "red"
                )
                self.info_cont_abort()
            except ResourcesMissingError as res_missing:
                self.info_cont_write(
                    f"{self.locale.tr('file_missing')}\n{res_missing}",
                    "red"
                )
                self.info_cont_abort()
            except ManifestKeyError as wrong_key_type:
                self.info_cont_write(
                    f"{self.locale.tr('wrong_key_type')} {wrong_key_type}",
                    "red"
                )
                self.info_cont_abort()

            # except Exception as exc:
            #     self.info_cont_write(exc, "red")
            #     self.info_cont_abort()
            finally:
                self.info_cont_btn.disabled = False


def main(page: Page) -> None:
    def window_resized(e: ControlEvent) -> None:
        main_app.main_column.width = page.width
        main_app.main_column.height = page.height-3
        try:
            main_app.info_cont.width = page.width
            main_app.info_cont.height = page.height-3
            main_app.info_cont.update()
        # error occurs because this widget is not always on app main screen
        except AssertionError:
            pass

        main_app.update()

    def save_config(e: ControlEvent) -> None:
        """
        Saves config when exiting application.
        """
        if e.data == "close":
            try:
                main_app.update_config()
                main_app.config.save_config()
            except Exception as exc:
                logger.error(exc)

            page.window_destroy()

    def create_error_container(message: str) -> None:
        """
        Creates error container instead of main GUI
        if semothing went wrong on startup.
        """
        page.window_maximizable = False

        return Row(
            controls=[
                Container(
                    Text(
                        value=message,
                        size=18,
                        text_align="center"
                    ),
                    bgcolor="#610606",
                    width=850,
                    height=50,
                    alignment=alignment.center,
                    border_radius=20
                )
            ],
            width=page.width,
            height=page.height,
            alignment=MainAxisAlignment.CENTER
        )

    page.title = FULL_NAME
    page.vertical_alignment = MainAxisAlignment.START
    page.horizontal_alignment = MainAxisAlignment.CENTER
    page.window_width = 880
    page.window_min_width = 832
    page.window_height = 706
    page.bgcolor = "#3d5a68"

    # page.window_resizable = False
    # page.window_maximizable = False

    page.theme_mode = ThemeMode.DARK
    page.padding = padding.all(0)

    page.window_prevent_close = True

    page.on_window_event = save_config
    page.on_resize = window_resized

    logger.info(f"Running {FULL_NAME} in {MAIN_PATH}")

    try:
        main_app = RandomizerWindow(
            page=page,
            config=Config(SETTINGS_PATH),
            locale=Localisation(LOCALIZATION_PATH),
            working_width=800
        )
    except LocalisationMissingError as loc_missing:
        logger.critical(loc_missing)
        page.add(create_error_container(loc_missing))
        page.update()
        return
    except ValidationError as invalid_settings:
        logger.critical(invalid_settings)
        page.add(create_error_container(invalid_settings))
        page.update()
        return
    except Exception as exc:
        page.add(exc)
        return

    page.add(main_app)
    page.update()

    main_app.set_widget_connections()
    main_app.fill_versions_dd(SUPPORTED_VERSIONS)
    main_app.fill_presets_dd(PRESETS)
    main_app.apply_config()

    logger.debug(f"Config applied: {main_app.config.yaml}")


def start():
    app(target=main)
