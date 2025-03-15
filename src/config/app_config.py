from dataclasses import dataclass, field
import logging
from pathlib import Path
from typing import Optional, Dict

logger = logging.getLogger(Path(__file__).name)


@dataclass
class Config:
    resources_path: Path
    pos_x: int = 0
    pos_y: int = 0
    width: Optional[float] = None
    height: Optional[float] = None
    is_maximized: bool = False
    language: str = "eng"
    game_path: str = ""
    game_version: str = ""
    preset: str = ""
    manifest: str = field(default="", repr=False)
    options: str = field(default="", repr=False)

    chkbxs: Dict[str, bool] = field(default_factory=lambda: {
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
    })

    def load_app_config(self, serialized_yaml: dict) -> None:
        """
        Provides data from serialized yaml
        to instance variables.
        """
        if not isinstance(serialized_yaml, dict):
            logger.error('Provided config is not dict.')
            return

        self.pos_x = serialized_yaml.get("pos_x", 0)
        self.pos_y = serialized_yaml.get("pos_y", 0)
        self.width = serialized_yaml.get("width")
        self.height = serialized_yaml.get("height")
        self.is_maximized = serialized_yaml.get("is_maximized", False)
        self.language = serialized_yaml.get("language", "eng")
        self.game_path = serialized_yaml.get("game_path", "")
        self.game_version = serialized_yaml.get("game_version", "")
        self.preset = serialized_yaml.get("preset", "")

        for chkbx in self.chkbxs:
            self.chkbxs[chkbx] = serialized_yaml.get(chkbx, False)

        logger.info("Successfully loaded config from yaml.")

    def to_dict(self) -> dict:
        """
        Returns dict representation of this dataclass.
        """
        return {
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
            "width": self.width,
            "height": self.height,
            "is_maximized": self.is_maximized,
            "language": self.language,
            "game_path": self.game_path,
            "game_version": self.game_version,
            "preset": self.preset,
            **self.chkbxs
        }
