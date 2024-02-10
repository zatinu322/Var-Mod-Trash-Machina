import struct

from icecream import ic

from working_set_manager import WorkingSetManager
from data import OFFSETS_EXE, generate_offsets


class ExecutableRandomizer(WorkingSetManager):
    def __init__(self, working_set: dict) -> None:
        super().__init__(working_set)

    def generate_offsets(self, offsets_exe: dict) -> dict:
        # we should not overwrite global const
        offsets = generate_offsets()

        if "Render" in self.exe["content"]:
            offsets_exe.update(offsets["render"])
        if "Gravity" in self.exe["content"]:
            offsets_exe.update(offsets["gravity"])
        if "FOV" in self.exe["content"]:
            offsets_exe.update(offsets["fov"])
        if "Armor" in self.exe["content"]:
            offsets_exe.update(offsets["armor"])

        return offsets_exe

    def collect_info(self, config: dict):
        info = {}
        if "Render" in self.exe["content"]:
            info.update({"new_models_render": config.get(0x30808B)})
        if "Gravity" in self.exe["content"]:
            info.update({"new_gravity": config.get(0x202D25)})
        if "FOV" in self.exe["content"]:
            info.update({"new_fov": round(config.get(0x5E5A74), 3)})

        return info

    def randomize(self) -> dict:
        file_path = self.game_path / self.exe["file"]
        offsets_exe = self.generate_offsets(OFFSETS_EXE.copy())
        ic(offsets_exe)

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
        if not self.exe["content"]:
            self.logger.info("Nothing to randomize.")
            return
        ic(self.exe)

        offsets_exe = self.randomize()

        ic(self.collect_info(offsets_exe))
