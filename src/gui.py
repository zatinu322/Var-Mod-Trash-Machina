from pathlib import Path

from flet import UserControl, Page, ButtonStyle, RoundedRectangleBorder, \
    Container, Dropdown, ElevatedButton, FontWeight, Text, Row, \
    Column, MainAxisAlignment, border, Checkbox, TextField, \
    padding, alignment, ProgressBar, Image, CrossAxisAlignment, \
    ControlEvent, Icon, icons, animation, IconButton


class MainGui(UserControl):
    def __init__(self, page: Page, width: int) -> None:
        super().__init__()

        self.page = page
        self.main_width = width
        self.button_style = ButtonStyle(
            shape=RoundedRectangleBorder(radius=10)
        )
        self.btn_rus, self.btn_eng = self.create_lang_buttons()
        self.options_gui = self.create_options()
        self.expandable_options = ExpandableContainer(
            self.main_width, 760, 64, content=self.options_gui
        )
        self.game_path_setting_gui = self.create_game_path_setting()
        self.start_randomization_btn = self.create_randomization_btn()
        self.game_version_dd = self.create_game_version_setting()
        self.info_cont = self.create_info_container()

    # lang buttons
    def create_lang_buttons(self) -> None:
        """
        Creates buttons with flag icons for changing language.
        """
        return (
            Container(
                width=80,
                height=40,
                ink=True,
                image_src=Path("src\\assets\\rus.png").resolve(),
                image_fit="fill"
            ),
            Container(
                width=80,
                height=40,
                ink=True,
                image_src=Path("src\\assets\\eng.png").resolve(),
                image_fit="fill"
            )
        )

    # options
    def create_options(self) -> list:
        self.create_opt_chkbxs()

        self.dd_preset = Dropdown()
        self.btn_select_all = ElevatedButton(
            style=self.button_style, width=150, height=58
        )
        self.btn_deselect_all = ElevatedButton(
            style=self.button_style, width=150, height=58
        )

        self.t_icons = Text(value="t_icons", size=20, weight=FontWeight.BOLD)
        self.t_icons_row = Row(
            controls=[
                self.t_icons
            ],
            width=160,
            alignment="center"
        )

        self.t_text = Text(value="t_text", size=20, weight=FontWeight.BOLD)
        self.t_text_row = Row(
            controls=[
                self.t_text
            ],
            width=210,
            alignment="center"
        )

        self.t_sounds = Text(value="t_sounds", size=20, weight=FontWeight.BOLD)
        self.t_sounds_row = Row(
            controls=[
                self.t_sounds
            ],
            width=135,
            alignment="center"
        )

        self.t_models = Text(value="t_models", size=20, weight=FontWeight.BOLD)
        self.t_models_row = Row(
            controls=[
                self.t_models
            ],
            width=210,
            alignment="center"
        )

        self.t_textures = Text(
            value="t_textures", size=20, weight=FontWeight.BOLD
        )
        self.t_textures_row = Row(
            controls=[
                self.t_textures
            ],
            width=135,
            alignment="center"
        )

        self.t_other = Text(value="t_other", size=20, weight=FontWeight.BOLD)
        self.t_other_row = Row(
            controls=[
                self.t_other
            ],
            width=150,
            alignment="center"
        )

        self.t_executable = Text(
            value="t_exe", size=20, weight=FontWeight.BOLD
        )
        self.t_executable_row = Row(
            controls=[
                self.t_executable
            ],
            width=185,
            alignment="center"
        )

        self.opt_icons = Column(
            controls=[
                self.t_icons_row,
                Column(
                    controls=[
                        self.cb_maps,
                        self.cb_digits,
                        self.cb_splashes,
                        self.cb_bkgd,
                        self.cb_clans,
                        self.cb_gui_icons,
                        self.cb_radar,
                        self.cb_goods_guns,
                        self.cb_cab_cargo,
                        self.cb_aim
                    ],
                    spacing=0
                )
            ],
            width=160
        )

        self.opt_text = Column(
            controls=[
                self.t_text_row,
                Column(
                    controls=[
                        self.cb_names,
                        self.cb_dialogues,
                        self.cb_quests,
                        self.cb_controls,
                        self.cb_fadingmsgs,
                        self.cb_gui_text,
                        self.cb_books_history,
                        self.cb_descriptions
                    ],
                    spacing=0
                )
            ],
            width=160
        )

        self.opt_sounds = Column(
            controls=[
                self.t_sounds_row,
                Column(
                    controls=[
                        self.cb_music,
                        self.cb_speech,
                        self.cb_radio,
                        self.cb_crashes,
                        self.cb_explosions,
                        self.cb_engines,
                        self.cb_horns,
                        self.cb_hits,
                        self.cb_shooting,
                        self.cb_other_sounds
                    ],
                    spacing=0
                )
            ],
            width=110
        )

        self.opt_models = Column(
            controls=[
                self.t_models_row,
                Column(
                    controls=[
                        self.cb_env_models,
                        self.cb_towns,
                        self.cb_guns,
                        self.cb_trees,
                        self.cb_npc_look,
                        self.cb_wheels,
                        self.cb_humans,
                        self.cb_dwellers
                    ],
                    spacing=0
                )
            ],
            width=190
        )

        self.opt_textures = Column(
            controls=[
                self.t_textures_row,
                Column(
                    controls=[
                        self.cb_env_textures,
                        self.cb_masks,
                        self.cb_veh_skins,
                        self.cb_lightmaps,
                        self.cb_skybox,
                        self.cb_tiles
                    ],
                    spacing=0
                )
            ],
            width=125
        )

        self.opt_other = Column(
            controls=[
                self.t_other_row,
                Column(
                    controls=[
                        self.cb_weather,
                        self.cb_landscape,
                        self.cb_ai_vehs,
                        self.cb_pl_veh,
                        self.cb_guns_lua
                    ],
                    spacing=0
                )
            ],
            width=135
        )

        self.opt_exe = Column(
            controls=[
                self.t_executable_row,
                Column(
                    controls=[
                        self.cb_render,
                        self.cb_gravity,
                        self.cb_fov,
                        self.cb_armor
                    ],
                    spacing=0
                )
            ],
            width=185
        )

        return [
            Column(
                controls=[
                    Row(
                        controls=[
                            self.dd_preset,
                            self.btn_select_all,
                            self.btn_deselect_all
                        ],
                        alignment=MainAxisAlignment.CENTER
                    ),
                    Row(
                        width=self.main_width,
                        height=365,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Container(
                                content=self.opt_icons,
                                border=border.all(1, "black"),
                                border_radius=10,
                                bgcolor="white10"
                            ),
                            Container(
                                content=self.opt_text,
                                border=border.all(1, "black"),
                                border_radius=10,
                                bgcolor="white10"
                            ),
                            Container(
                                content=self.opt_sounds,
                                border=border.all(1, "black"),
                                border_radius=10,
                                bgcolor="white10"
                            ),
                            Container(
                                content=self.opt_models,
                                border=border.all(1, "black"),
                                border_radius=10,
                                bgcolor="white10"
                            )
                        ]
                    ),
                    Row(
                        width=self.main_width,
                        height=235,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Container(
                                content=self.opt_textures,
                                border=border.all(1, "black"),
                                border_radius=10,
                                bgcolor="white10"
                            ),
                            Container(
                                content=self.opt_other,
                                border=border.all(1, "black"),
                                border_radius=10,
                                bgcolor="white10"
                            ),
                            Container(
                                content=self.opt_exe,
                                border=border.all(1, "black"),
                                border_radius=10,
                                bgcolor="white10"
                            )
                        ]
                    )
                ]
            )
        ]

    def create_opt_chkbxs(self) -> None:
        """
        Creates checkboxes for options container
        and instance variable with dict[Checkbox, str].
        """
        self.cb_ai_vehs = Checkbox(label="cb_ai_vehs")
        self.cb_aim = Checkbox(label="cb_aim")
        self.cb_armor = Checkbox(label="cb_armor")
        self.cb_bkgd = Checkbox(label="cb_bkgd")
        self.cb_books_history = Checkbox(label="cb_books_history")
        self.cb_cab_cargo = Checkbox(label="cb_cab_cargo")
        self.cb_clans = Checkbox(label="cb_clans")
        self.cb_controls = Checkbox(label="cb_controls")
        self.cb_crashes = Checkbox(label="cb_crashes")
        self.cb_descriptions = Checkbox(label="cb_descriptions")
        self.cb_dialogues = Checkbox(label="cb_dialogues")
        self.cb_digits = Checkbox(label="cb_digits")
        self.cb_dwellers = Checkbox(label="cb_dwellers")
        self.cb_engines = Checkbox(label="cb_engines")
        self.cb_env_models = Checkbox(label="cb_env_models")
        self.cb_env_textures = Checkbox(label="cb_env_textures")
        self.cb_explosions = Checkbox(label="cb_explosions")
        self.cb_fadingmsgs = Checkbox(label="cb_fadingmsgs")
        self.cb_fov = Checkbox(label="cb_fov")
        self.cb_goods_guns = Checkbox(label="cb_goods_guns")
        self.cb_gravity = Checkbox(label="cb_gravity")
        self.cb_gui_icons = Checkbox(label="cb_gui_icons")
        self.cb_gui_text = Checkbox(label="cb_gui_text")
        self.cb_guns = Checkbox(label="cb_guns")
        self.cb_guns_lua = Checkbox(label="cb_guns_lua")
        self.cb_hits = Checkbox(label="cb_hits")
        self.cb_horns = Checkbox(label="cb_horns")
        self.cb_humans = Checkbox(label="cb_humans")
        self.cb_landscape = Checkbox(label="cb_landscape")
        self.cb_lightmaps = Checkbox(label="cb_lightmaps")
        self.cb_maps = Checkbox(label="cb_maps")
        self.cb_masks = Checkbox(label="cb_masks")
        self.cb_music = Checkbox(label="cb_music")
        self.cb_names = Checkbox(label="cb_names")
        self.cb_npc_look = Checkbox(label="cb_npc_look")
        self.cb_other_sounds = Checkbox(label="cb_other_sounds")
        self.cb_pl_veh = Checkbox(label="cb_pl_veh")
        self.cb_quests = Checkbox(label="cb_quests")
        self.cb_radar = Checkbox(label="cb_radar")
        self.cb_radio = Checkbox(label="cb_radio")
        self.cb_render = Checkbox(label="cb_render")
        self.cb_shooting = Checkbox(label="cb_shooting")
        self.cb_skybox = Checkbox(label="cb_skybox")
        self.cb_speech = Checkbox(label="cb_speech")
        self.cb_splashes = Checkbox(label="cb_splashes")
        self.cb_tiles = Checkbox(label="cb_tiles")
        self.cb_towns = Checkbox(label="cb_towns")
        self.cb_trees = Checkbox(label="cb_trees")
        self.cb_veh_skins = Checkbox(label="cb_veh_skins")
        self.cb_weather = Checkbox(label="cb_weather")
        self.cb_wheels = Checkbox(label="cb_wheels")

        self.chkbxs_dict = {
            self.cb_ai_vehs: "cb_ai_vehs",
            self.cb_aim: "cb_aim",
            self.cb_armor: "cb_armor",
            self.cb_bkgd: "cb_bkgd",
            self.cb_books_history: "cb_books_history",
            self.cb_cab_cargo: "cb_cab_cargo",
            self.cb_clans: "cb_clans",
            self.cb_controls: "cb_controls",
            self.cb_crashes: "cb_crashes",
            self.cb_descriptions: "cb_descriptions",
            self.cb_dialogues: "cb_dialogues",
            self.cb_digits: "cb_digits",
            self.cb_dwellers: "cb_dwellers",
            self.cb_engines: "cb_engines",
            self.cb_env_models: "cb_env_models",
            self.cb_env_textures: "cb_env_textures",
            self.cb_explosions: "cb_explosions",
            self.cb_fadingmsgs: "cb_fadingmsgs",
            self.cb_fov: "cb_fov",
            self.cb_goods_guns: "cb_goods_guns",
            self.cb_gravity: "cb_gravity",
            self.cb_gui_icons: "cb_gui_icons",
            self.cb_gui_text: "cb_gui_text",
            self.cb_guns: "cb_guns",
            self.cb_guns_lua: "cb_guns_lua",
            self.cb_hits: "cb_hits",
            self.cb_horns: "cb_horns",
            self.cb_humans: "cb_humans",
            self.cb_landscape: "cb_landscape",
            self.cb_lightmaps: "cb_lightmaps",
            self.cb_maps: "cb_maps",
            self.cb_masks: "cb_masks",
            self.cb_music: "cb_music",
            self.cb_names: "cb_names",
            self.cb_npc_look: "cb_npc_look",
            self.cb_other_sounds: "cb_other_sounds",
            self.cb_pl_veh: "cb_pl_veh",
            self.cb_quests: "cb_quests",
            self.cb_radar: "cb_radar",
            self.cb_radio: "cb_radio",
            self.cb_render: "cb_render",
            self.cb_shooting: "cb_shooting",
            self.cb_skybox: "cb_skybox",
            self.cb_speech: "cb_speech",
            self.cb_splashes: "cb_splashes",
            self.cb_tiles: "cb_tiles",
            self.cb_towns: "cb_towns",
            self.cb_trees: "cb_trees",
            self.cb_veh_skins: "cb_veh_skins",
            self.cb_weather: "cb_weather",
            self.cb_wheels: "cb_wheels",
        }

    # game path
    def create_game_path_setting(self):
        self.game_path_tf = TextField(width=600)
        self.browse_btn = ElevatedButton(
            bgcolor="white10",
            style=self.button_style)
        self.game_path_status_t = Text()

        return Column(
            controls=[
                Row(
                    controls=[
                        self.game_path_tf
                    ]
                ),
                Row(
                    controls=[
                        self.browse_btn,
                        self.game_path_status_t
                    ]
                )
            ]
        )

    # game version
    def create_game_version_setting(self):
        return Dropdown(width=600)

    # randomization button
    def create_randomization_btn(self):
        return ElevatedButton(
            width=300,
            height=70,
            style=self.button_style
        )

    # info container
    def create_info_container(self) -> Row:
        self.create_info_container_widgets()
        self.log_container.controls.clear()  # clear previous log
        return Row(
            [
                Container(
                    Column(
                        [
                            Row(
                                [
                                    Container(
                                        self.info_cont_heading,
                                        padding=padding.only(top=5)
                                    )
                                ],
                                alignment=MainAxisAlignment.CENTER
                            ),
                            Row(
                                [
                                    Container(
                                        width=600,
                                        opacity=0.7,
                                        height=330,
                                        alignment=alignment.top_left,
                                        padding=10,
                                        bgcolor="black",
                                        border_radius=10,
                                        content=self.log_container
                                    )
                                ],
                                alignment=MainAxisAlignment.CENTER
                            ),
                            Row(
                                [
                                    self.progress_bar
                                ],
                                alignment=MainAxisAlignment.CENTER
                            ),
                            Row(
                                [
                                    self.info_cont_btn
                                ],
                                alignment=MainAxisAlignment.CENTER
                            )
                        ]
                    ),
                    alignment=alignment.top_center,
                    bgcolor="#3d5a68",
                    opacity=80,
                    border_radius=20,
                    width=700,
                    height=470
                )
            ],
            width=800,
            alignment=MainAxisAlignment.CENTER
        )

    def create_info_container_widgets(self):
        self.progress_bar = ProgressBar(width=590, height=20, value=0)
        self.status_text = Text()
        self.info_cont_heading = Text(size=16, weight=FontWeight.BOLD)
        self.info_cont_btn = ElevatedButton(text="OK", width=150, height=50)
        self.log_container = Column(
            controls=[],
            spacing=1,
            width=600,
            scroll=True
        )

    def build(self) -> Container:
        self.main_column = Column(
            [
                # extra row, because padding and margin breaks scrolling
                Row(
                    height=1
                ),
                # language buttons
                Row(
                    [
                        self.btn_rus,
                        self.btn_eng
                    ],
                    width=200,
                    alignment=MainAxisAlignment.CENTER,
                    spacing=30
                ),
                # logo
                Row(
                    [
                        Container(
                            Image(src=Path("src\\assets\\logo.png").resolve()),
                            width=self.main_width
                        ),
                    ],
                    alignment=MainAxisAlignment.CENTER
                ),
                # settings
                Row(
                    [
                        self.expandable_options
                    ],
                    alignment=MainAxisAlignment.CENTER
                ),
                # game path selection
                Row(
                    [
                        self.game_path_setting_gui
                    ],
                    width=self.main_width,
                    height=100,
                    alignment=MainAxisAlignment.SPACE_AROUND
                ),
                # game version selection
                Row(
                    [
                        self.game_version_dd
                    ],
                    width=self.main_width,
                    alignment=MainAxisAlignment.SPACE_AROUND
                ),
                Row(
                    [
                        self.start_randomization_btn
                    ],
                    width=self.main_width,
                    alignment=MainAxisAlignment.CENTER
                ),
                # extra row, because padding and margin breaks scrolling
                Row(
                    height=1
                ),
            ],
            width=self.page.width-(self.page.padding.left*2),
            horizontal_alignment=CrossAxisAlignment.CENTER,
            alignment=MainAxisAlignment.START,
            scroll="hidden",
            spacing=30
        )
        self.main_cont = Container(
            self.main_column,
            # border=border.all("1", "red")
        )
        return self.main_cont


class ExpandableContainer(UserControl):
    def __init__(self,
                 width: int,
                 full_height: int,
                 hidden_height: int,
                 name: Text = Text(),
                 content: list = []) -> None:

        super().__init__()

        self.width = width
        self.full_height = full_height
        self.hidden_height = hidden_height
        self.name = name
        self.content = content

        self.format_name()

        self.expand_icon = IconButton(
            icon=icons.KEYBOARD_ARROW_DOWN,
            icon_size=30,
            on_click=lambda e: self.expand_container(e)
        )

    def format_name(self) -> None:
        self.name.size = 16
        self.name.weight = FontWeight.BOLD

    def expand_container(self, e: ControlEvent) -> None:
        if self.controls[0].height != self.full_height:
            self.controls[0].height = self.full_height
            self.expand_icon.icon = icons.KEYBOARD_ARROW_UP
            self.controls[0].update()
        else:
            self.controls[0].height = self.hidden_height
            self.expand_icon.icon = icons.KEYBOARD_ARROW_DOWN
            self.controls[0].update()

    def build(self) -> Container:
        return Container(
            Column(
                [
                    Row(
                        [
                            Icon(icons.SETTINGS),
                            self.name,
                            self.expand_icon
                        ],
                        spacing=10
                    ),
                    *self.content
                ],
                spacing=12
            ),
            width=self.width,
            height=self.hidden_height,
            bgcolor="white10",
            border_radius=11,
            animate=animation.Animation(400, "decelerate"),
            padding=padding.only(left=10, right=10, top=10)
        )
