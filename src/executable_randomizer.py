import struct
import logging
from pathlib import Path

from offsets_utils import OFFSETS_EXE, generate_offsets
from working_set_manager import RandomizationParams

logger = logging.getLogger(Path(__file__).name)


class ExecutableRandomizer:
    def __init__(self, params: RandomizationParams) -> None:
        self.params = params

    def generate_exe_offsets(self, offsets_exe: dict) -> dict:
        # we should not overwrite global const
        offsets = generate_offsets()

        if "Render" in self.params.exe["content"]:
            offsets_exe.update(offsets["render"])
        if "Gravity" in self.params.exe["content"]:
            offsets_exe.update(offsets["gravity"])
        if "FOV" in self.params.exe["content"]:
            offsets_exe.update(offsets["fov"])
        if "Armor" in self.params.exe["content"]:
            offsets_exe.update(offsets["armor"])

        return offsets_exe

    def collect_info(self, config: dict):
        info = {}
        if "Render" in self.params.exe["content"]:
            info.update({"new_models_render": config.get(0x30808B)})
        if "Gravity" in self.params.exe["content"]:
            info.update({"new_gravity": config.get(0x202D25)})
        if "FOV" in self.params.exe["content"]:
            info.update({"new_fov": round(config.get(0x5E5A74), 3)})

        return info

    def randomize(self) -> dict:
        file_path = self.params.game_path / self.params.exe["file"]
        offsets_exe = self.generate_exe_offsets(OFFSETS_EXE.copy())

        # logic by Aleksandr "Seel" Parfenenkov
        with open(file_path, "rb+") as exe:
            for offset in offsets_exe:
                exe.seek(offset)
                if isinstance(offsets_exe[offset], int):
                    exe.write(struct.pack("i", offsets_exe[offset]))
                elif isinstance(offsets_exe[offset], str):  # hex address
                    exe.write(
                        struct.pack("<L", int(offsets_exe[offset], base=16))
                    )
                elif isinstance(offsets_exe[offset], float):
                    exe.write(struct.pack("f", offsets_exe[offset]))

        return offsets_exe

    def start_randomization(self) -> None:
        if not self.params.exe["content"]:
            logger.info("Nothing to randomize.")
            return

        offsets_exe = self.randomize()

        return self.collect_info(offsets_exe)
