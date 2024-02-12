import logging

from yaml_parser import YamlConfig

logger = logging.getLogger("pavlik")


class Config(YamlConfig):
    def __init__(self, yaml_path: str) -> None:
        super().__init__(yaml_path)

        self.pos_x: int = 0
        self.pos_y: int = 0
        self.width: float | None = None
        self.height: float | None = None
        self.is_maximized: bool = False
        self.lang: str = "eng"
        self.game_path: str = ""
        self.game_version: str = ""
        self.preset: str = ""
        self.manifest = ""

        self.chkbxs: dict = {
            "cb_ai_vehs": False,
            "cb_aim": False,
            "cb_armor": False,
            "cb_bkgd": False,
            "cb_books_history": False,
            "cb_cab_cargo": False,
            "cb_clans": False,
            "cb_controls": False,
            "cb_crashes": False,
            "cb_descriptions": False,
            "cb_dialogues": False,
            "cb_digits": False,
            "cb_dwellers": False,
            "cb_engines": False,
            "cb_env_models": False,
            "cb_env_textures": False,
            "cb_explosions": False,
            "cb_fadingmsgs": False,
            "cb_fov": False,
            "cb_goods_guns": False,
            "cb_gravity": False,
            "cb_gui_icons": False,
            "cb_gui_text": False,
            "cb_guns": False,
            "cb_guns_lua": False,
            "cb_hits": False,
            "cb_horns": False,
            "cb_humans": False,
            "cb_landscape": False,
            "cb_lightmaps": False,
            "cb_maps": False,
            "cb_masks": False,
            "cb_music": False,
            "cb_names": False,
            "cb_npc_look": False,
            "cb_other_sounds": False,
            "cb_pl_veh": False,
            "cb_quests": False,
            "cb_radar": False,
            "cb_radio": False,
            "cb_render": False,
            "cb_shooting": False,
            "cb_skybox": False,
            "cb_speech": False,
            "cb_splashes": False,
            "cb_tiles": False,
            "cb_towns": False,
            "cb_trees": False,
            "cb_veh_skins": False,
            "cb_weather": False,
            "cb_wheels": False
        }

        if self.yaml:
            self.load_app_config()
        else:
            logger.info("Unable to load settings. Setting defaults.")

    def load_app_config(self) -> None:
        if not isinstance(self.yaml, dict):
            return

        self.pos_x = self.yaml.get("pos_x", 0)
        self.pos_y = self.yaml.get("pos_y", 0)
        self.width = self.yaml.get("width", None)
        self.height = self.yaml.get("height", None)
        self.is_maximized = self.yaml.get("is_maximized", False)
        self.lang = self.yaml.get("language", "eng")
        self.game_path = self.yaml.get("game_path", "")
        self.game_version = self.yaml.get("version", "")
        self.preset = self.yaml.get("preset", "")

        for k in self.chkbxs.keys():
            self.chkbxs.update({k: self.yaml.get(k, False)})

    def update_config(self) -> None:
        self.yaml.update(
            {
                "language": self.lang,
                "game_path": self.game_path,
                "pos_x": self.pos_x,
                "pos_y": self.pos_y,
                "width": self.width,
                "height": self.height,
                "is_maximized": self.is_maximized,
                "preset": self.preset,
                "version": self.game_version,
                **self.chkbxs
            }
        )

    def save_config(self):
        self.dump_yaml(self.yaml)
