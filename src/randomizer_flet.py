import flet as ft
from flet import *
import logging

import main_randomizer as mr

from icecream import ic
from pathlib import Path

from gui import MainGui
from config import Config
from localisation import Localisation
from validation import Validation
from errors import LocalisationMissingError, RootNotFoundError, ExeMissingError, GameNotFoundError, VersionError, ManifestMissingError, GDPFoundError
from data import FULL_NAME, MAIN_PATH, SETTINGS_PATH, LOCALIZATION_PATH, SUPPORTED_VERSIONS, PRESETS

logging.basicConfig(filename = "randomizer.log",
                    level = logging.INFO,
                    format = "[%(levelname)s][%(asctime)s]: %(message)s [%(filename)s, %(funcName)s]", 
                    filemode= "w", 
                    datefmt="%m/%d/%Y %H:%M:%S",
                    encoding="utf-8")

logger = logging.getLogger("pavlik")

class RandomizerWindow(MainGui):
    def __init__(
        self,
        page: Page, 
        config: Config, 
        locale: Localisation,
        main_width: int, 
        working_width: int
    ) -> None:
        super().__init__(main_width, working_width)

        self.page = page
        self.config = config
        self.locale = locale

        self.bg_cont = ft.Container(
            Row(
                controls=[
                    Column(
                        controls=[], alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ]
            ),
                bgcolor=ft.colors.BLACK87
        )

        self.opt_column_widths = {
            (self.opt_icons, self.t_icons_row): {"rus": 160, "eng": 180},
            (self.opt_text, self.t_text_row): {"rus": 210, "eng": 160},
            (self.opt_sounds, self.t_sounds_row): {"rus": 135, "eng": 110},
            (self.opt_models, self.t_models_row): {"rus": 210, "eng": 190},
            (self.opt_textures, self.t_textures_row): {"rus": 135, "eng": 125},
            (self.opt_other, self.t_other_row): {"rus": 150, "eng": 135},
            (self.opt_exe, self.t_executable_row): {"rus": 185, "eng": 165}
        }

        self.validate = Validation()

        # Add FilePicker to page overlay
        self.get_dir_dialog = FilePicker(on_result=self.get_dir_result)
        page.overlay.extend([self.get_dir_dialog])
    
    def fill_versions_dd(self, versions: dict) -> None:
        for key,text in versions.items():
            self.game_version_dd.options.append(dropdown.Option(text=text, key=key))
        self.update_app()
    
    def fill_presets_dd(self, presets: dict) -> None:
        for preset in presets:
            self.dd_preset.options.append(dropdown.Option(text=preset, key=preset))

    def set_widget_connections(self) -> None:
        self.btn_rus.on_click = self.switch_lang
        self.btn_eng.on_click = self.switch_lang
        self.browse_btn.on_click = lambda _: self.get_dir_dialog.get_directory_path()
        self.game_path_tf.on_change = self.game_path_changed
        self.btn_select_all.on_click = self.select_or_deselect
        self.btn_deselect_all.on_click = self.select_or_deselect
        self.dd_preset.on_change = self.update_checkboxes
        self.start_randomization_btn.on_click = self.start_randomization
        self.info_cont_btn.on_click = self.close_info_cont

        for chkbx in self.chkbxs_dict:
            chkbx.on_change = self.set_custom_preset
        self.update_app()
    
    def switch_lang(self, e: ContainerTapEvent):
        match e.control:
            case self.btn_rus:
                self.locale.update_lang("rus")
                self.config.lang = "rus"
            case self.btn_eng:
                self.locale.update_lang("eng")
                self.config.lang = "eng"
        self.retranslate_ui()
    
    def adjust_width(self) -> None:
        """Adjusts widgets width when changing localisation."""

        for (k,k1), v in self.opt_column_widths.items():
            k.width = v.get(self.locale.lang)
            k1.width = v.get(self.locale.lang)
        
        self.update_app()
    
    def apply_config(self):
        self.page.window_left = self.config.pos_x
        self.page.window_top = self.config.pos_y

        self.locale.update_lang(self.config.lang)
        self.retranslate_ui()

        self.game_path_tf.value = self.config.game_path
        self.update_path_status()

        self.dd_preset.value = self.config.preset
        for k,v in self.chkbxs_dict.items():
            k.value = self.config.chkbxs.get(v, False)
        
        self.game_version_dd.value = self.config.game_version
        
        self.update_app()

    def retranslate_ui(self) -> None:
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

        for k,v in self.chkbxs_dict.items():
            k.label = self.locale.tr(v)
        
        for option in self.dd_preset.options:
            option.text = self.locale.tr(option.key)

        
        self.update_path_status()
        
        self.adjust_width()

        self.update_app()

    def update_app(self):
        self.update()
        self.page.update()
        self.expandable_options.update()
    
    def create_dialog(
        self,
        modal: bool = False,
        title: str = "",
        content: str = "",
        actions: list[TextButton, None] = []
    ) -> AlertDialog:
        return AlertDialog(
            modal = modal,
            title = Text(title),
            content = Text(content),
            actions = actions,
        )
    
    def get_dir_result(self, e: FilePickerResultEvent) -> None:
        if e.path:
            self.game_path_tf.value = e.path
            self.update_path_status()
            self.update_app()
    
    def game_path_changed(self, e: ControlEvent) -> None:
        self.update_path_status(e.data)

    def update_path_status(self, cur_value: str = None) -> None:
        if cur_value is None: cur_value = self.game_path_tf.value
        if cur_value == "":
            self.game_path_status_t.value=""
            self.game_path_status_t.opacity = 0
            return

        game_path = Path(self.game_path_tf.value)

        try:
            validation = self.validate.game_dir(game_path)
        except (RootNotFoundError, ExeMissingError, GameNotFoundError, VersionError):
            validation = False
        except GDPFoundError:
            validation = False
            self.game_path_status_t.color="red"
            self.game_path_status_t.opacity = 100
            self.game_path_status_t.value = self.locale.tr("gdp_found")

        if validation:
            self.game_path_status_t.value = self.locale.tr("valid_path")
            self.game_path_status_t.opacity = 100
            self.game_path_status_t.color="green"
        else:
            self.game_path_status_t.color="red"
            self.game_path_status_t.opacity = 100
            self.game_path_status_t.value = self.locale.tr("invalid_path")
        self.update_app()
    
    def select_or_deselect(self, e: ControlEvent):
        match e.control:
            case self.btn_select_all:
                checked = True
            case self.btn_deselect_all:
                checked = False
        
        for chkbx in self.chkbxs_dict:
            chkbx.value = checked
        self.set_custom_preset()
        
        self.update_app()
    
    def show_info_cont(self) -> None:
        self.page.overlay.append(self.bg_cont)
        self.page.overlay.append(self.info_cont)
        self.log_container.controls.clear()
        self.progress_bar.value = 0
        self.info_cont_btn.disabled = True
        self.retranslate_ui()
    
    def info_cont_write(self, message: str, color: str | int = "white") -> None:
        self.log_container.controls.append(
            Text(
                value=message,
                color=color
            )
        )
        self.update_app()
    
    def info_cont_abort(self):
        self.info_cont_write(self.locale.tr("randomization_aborted"), "red")
        self.info_cont_write(self.locale.tr("rand_OK"))
        self.info_cont_btn.disabled = False
        self.progress_bar.value = 0
        self.update_app()
    
    def info_cont_success(self):
        self. info_cont_write(self.locale.tr("rand_done_full"), "green")
        self.info_cont_write(self.locale.tr("rand_OK"))
        self.info_cont_btn.disabled = False
        self.progress_bar.value = 1
        self.update_app()

    def close_info_cont(self, e: ControlEvent) -> None:
        self.page.overlay.remove(self.info_cont)
        self.page.overlay.remove(self.bg_cont)
        self.update_app()
    
    def update_checkboxes(self, e: ControlEvent) -> None:
        chkbxs_config = PRESETS.get(e.data, {})
        for k,v in self.chkbxs_dict.items():
            new_value = chkbxs_config.get(v, None)
            if new_value == None: continue
            else: k.value = new_value

        self.update_app()
    
    def collect_chkbxs_values(self) -> dict:
        return {v:k.value for (k,v) in self.chkbxs_dict.items()}
    
    def update_config(self) -> None:
        self.config.pos_x = self.page.window_left
        self.config.pos_y = self.page.window_top
        self.config.preset = self.dd_preset.value
        self.config.game_path = self.game_path_tf.value
        self.config.game_version = self.game_version_dd.value
        chkbxs = self.collect_chkbxs_values()
        self.config.chkbxs.update(chkbxs)
        self.config.update_config()
        
    def set_custom_preset(self, e: ControlEvent = None) -> None:
        self.dd_preset.value = "p_custom"
        self.update_app()

    def disable_chkbxs(self, *chkbxs):
        for chkbx in chkbxs:
            chkbx.value = False
        self.update_config()
    
    def start_randomization(self, e: ControlEvent = None) -> None:
        self.update_config()
        self.show_info_cont()
        self.info_cont_write(self.locale.tr("rand_start"))

        self.info_cont_write(self.locale.tr("rand_validation"))
        try:
            validation, exe_status = self.validate.settings(self.config)
        except RootNotFoundError as no_root:
            self.info_cont_write(f"{self.locale.tr('game_path_missing')}\n{no_root}", color="red")
            self.info_cont_abort()
            return
        except ExeMissingError as no_exe:
            self.info_cont_write(f"{self.locale.tr('exe_not found')}\n{no_exe}", color="red")
            self.info_cont_abort()
            return
        except GameNotFoundError as no_game:
            self.info_cont_write(f"{self.locale.tr('not_game_dir')}\n{no_game}", color="red")
            self.info_cont_abort()
            return
        except GDPFoundError as gdp_found:
            self.info_cont_write(f"{self.locale.tr('gdp_found')}\n{gdp_found}", color="red")
            self.info_cont_abort()
            return
        except VersionError as bad_version:
            self.info_cont_write(f"{self.locale.tr('incorrect_version')}", color="red")
            self.info_cont_abort()
            return
        except ManifestMissingError as no_manifest:
            self.info_cont_write(f"{self.locale.tr('manifest_missing')}\n{no_manifest}", color="red")
            self.info_cont_abort()
            return
        
        match exe_status:
            case "no_exe":
                ic('no exe')
                logger.warning("Randomization options related to executable randomizer will be forcibly disabled.")
                self.info_cont_write(f"{self.locale.tr("is_continued")}", color="yellow")
                self.disable_chkbxs(
                    self.cb_render, 
                    self.cb_armor, 
                    self.cb_fov, 
                    self.cb_gravity
                )
            case "no_fov":
                ic('no_fov')
                self.info_cont_write(f"{self.locale.tr("is_continued")}", color="yellow")

                self.disable_chkbxs(self.cb_fov)
        
        self.progress_bar.value += 0.11

        if validation:
            try:
                
                self.info_cont_write(self.locale.tr("rand_copy"))
                mr.copy_files(self.config)
                self.progress_bar.value += 0.11

                self.info_cont_write(self.locale.tr("rand_files"))
                errors, status = mr.randomize_files(self.config)
                if not status:
                    self.info_cont_write(f"{self.locale.tr("rand_nothing")}")
                else:
                    self.info_cont_write(f"{self.locale.tr("rand_done")}")
                self.progress_bar.value += 0.11

                self.info_cont_write(self.locale.tr("rand_text"))
                mr.randomize_text(self.config)
                self.progress_bar.value += 0.11

                self.info_cont_write(self.locale.tr("rand_models"))
                mr.randomize_models(self.config)
                self.progress_bar.value += 0.11

                self.info_cont_write(self.locale.tr("rand_barnpcs"))
                mr.randomize_barnpcs(self.config)
                self.progress_bar.value += 0.11

                self.info_cont_write(self.locale.tr("rand_landscape"))
                mr.randomize_landscape(self.config)
                self.progress_bar.value += 0.11

                self.info_cont_write(self.locale.tr("rand_executable"))
                mr.randomize_executable(self.config)
                self.progress_bar.value += 0.11

                self.info_cont_write(self.locale.tr("rand_lua"))
                mr.randomize_lua(self.config)
                self.progress_bar.value += 0.11

                self.info_cont_success()

            except ManifestMissingError as bad_manifest:
                self.info_cont_write(f"{self.locale.tr('bad_manifest')}\n{bad_manifest}", "red")
                self.info_cont_abort()
                return
            except Exception as exc:
                self.info_cont_write(exc)
                self.info_cont_abort()
            finally:
                self.info_cont_btn.disabled = False


def main(page: Page) -> None:
    def save_config(e: ControlEvent) -> None:
        if e.data == "close":
            try:
                app.update_config()
                app.config.save_config()
            except Exception as exc:
                logger.error(exc)
            
            page.window_destroy()
    
    def create_error_container(message: str) -> None:
        return Container(
            Row(
                controls=[
                    Text(
                    value=message,
                    size=18
                    )
                ],
                alignment=MainAxisAlignment.CENTER
            ),
            width=1320,
            height=100,
            bgcolor="#610606",
            border_radius=20
        )
    
    logger.info(f"Running {FULL_NAME} in {MAIN_PATH}")

    page.title = FULL_NAME
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = MainAxisAlignment.CENTER
    page.window_width = 880
    page.window_height = 700

    page.window_resizable = False
    page.window_max_width = 880
    page.window_min_width = 880
    page.window_max_height = 870
    page.window_min_height = 800
    page.window_maximizable = False

    page.theme_mode = ThemeMode.DARK

    try:
        app = RandomizerWindow(
        page = page,
        config = Config(SETTINGS_PATH),
        locale = Localisation(LOCALIZATION_PATH),
        main_width = 850,
        working_width = 800
        )
    except LocalisationMissingError as loc_missing:
        logger.critical(loc_missing)
        page.add(create_error_container(loc_missing))
        page.update()
        return
    except Exception as exc:
        page.add(exc)
        return
    
    page.window_prevent_close = True

    page.on_window_event = save_config

    page.add(app)
    page.update()

    app.set_widget_connections()
    app.fill_versions_dd(SUPPORTED_VERSIONS)
    app.fill_presets_dd(PRESETS)
    app.apply_config()

def start():
    ft.app(target=main)