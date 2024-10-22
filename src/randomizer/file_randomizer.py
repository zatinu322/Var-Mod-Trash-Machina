import shutil
import os
from random import shuffle
import logging
from pathlib import Path

from config.randomization_config import RandomizationParams

logger = logging.getLogger(Path(__file__).name)


class FileRandomizer:
    def __init__(self, params: RandomizationParams) -> None:
        self.params = params
        self.temp_dir = params.game_path / "temp_random"

    def copy_files(self,
                   groups: list[dict],
                   repeated_files: list | None = None,
                   dest: str = "temp") -> list:
        repeatitions = 0
        if not repeated_files:
            repeated_files = []

        for group in groups:
            for file_path, files_list in group.items():
                for file in files_list:
                    data_path = self.params.game_path / file_path / file
                    temp_path = self.temp_dir / file
                    try:
                        if dest == "temp":
                            if temp_path.exists():
                                new_temp_path = self.temp_dir / f"{file}\
                                _{str(repeatitions)}"
                                repeated_files.append(
                                    (data_path, new_temp_path)
                                )
                                repeatitions += 1
                                temp_path = new_temp_path
                            shutil.copyfile(data_path, temp_path)
                        elif dest == "data":
                            if temp_path.exists():
                                shutil.copyfile(temp_path, data_path)
                                os.remove(temp_path)
                            else:
                                for dp, ntp in repeated_files:
                                    if dp == data_path:
                                        os.rename(ntp, temp_path)
                                        shutil.copyfile(temp_path, data_path)
                                        os.remove(temp_path)
                    except FileNotFoundError as e:
                        logger.error(e)
                        # self.report_error(e)
        return repeated_files

    def rename_files(self, files_list: list, bckw: bool = False) -> bool:
        filename = 0
        for file in files_list:
            old_file_path = self.temp_dir / file
            new_file_path = self.temp_dir / str(filename)
            try:
                if not bckw:
                    os.rename(old_file_path, new_file_path)
                elif bckw:
                    os.rename(new_file_path, old_file_path)
            except FileNotFoundError as exc:
                logger.error(exc)
                # self.report_error(exc)
            except FileExistsError as exc:
                logger.error(exc)
                # self.report_error(exc)

            filename += 1

        return True

    def randomize(self, groups: list) -> bool:
        if not self.temp_dir.exists():
            os.mkdir(self.temp_dir)
        repeatitions = self.copy_files(groups, dest="temp")

        files_list = os.listdir(self.temp_dir)

        self.rename_files(files_list)

        shuffle(files_list)

        self.rename_files(files_list, bckw=True)

        if repeatitions:
            self.copy_files(groups, repeated_files=repeatitions, dest="data")
        else:
            self.copy_files(groups, dest="data")

        os.rmdir(self.temp_dir)

        return True

    def start_randomization(self) -> bool:
        if not self.params.files:
            logger.info("Nothing to randomize.")
            return False
        for groups in self.params.files:
            self.randomize(groups)

        return True
