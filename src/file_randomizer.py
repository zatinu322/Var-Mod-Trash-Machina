import shutil
import os
from random import shuffle
from pathlib import Path

from icecream import ic

from working_set_manager import WorkingSetManager


class FileRandomizer(WorkingSetManager):
    def __init__(self, working_set: dict) -> None:
        super().__init__(working_set)

        self.temp_dir = self.game_path / "temp_random"
        # self.options = self.manifest.get("files")

    def copy_files(self,
                   groups: list[dict],
                   repeated_files: list = None,
                   dest="temp") -> list[bool]:
        repeatitions = 0
        if not repeated_files:
            repeated_files = []

        for group in groups:
            ic(group)
            for file_path, files_list in group.items():
                for file in files_list:
                    data_path = self.game_path / file_path / file
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
                        self.logger.error(e)
                        # self.report_error(e)
        return [True, repeated_files]

    def rename_files(self, files_list: list, bckw=False) -> bool:
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
                self.logger.error(exc)
                # self.report_error(exc)
            except FileExistsError as exc:
                self.logger.error(exc)
                # self.report_error(exc)

            filename += 1

        return True

    def randomize(self, groups: list) -> bool:
        if not self.temp_dir.exists():
            os.mkdir(self.temp_dir)
        status, repeatitions = self.copy_files(groups, dest="temp")

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
        if not self.files:
            self.logger.info("Nothing to randomize.")
            return False
        for groups in self.files:
            self.randomize(groups)

        return True
