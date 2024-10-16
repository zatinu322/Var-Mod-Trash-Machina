import logging
import sys

import randomizer_flet


def main_gui() -> None:
    logging.basicConfig(
        filename="randomizer.log",
        level=logging.INFO,
        format="%(levelname)s - %(asctime)s - "
               "%(name)s: %(message)s",
        filemode="w",
        datefmt="%d/%m/%Y %H:%M:%S",
        encoding="utf-8"
    )
    randomizer_flet.start()


if __name__ == "__main__":
    sys.exit(main_gui())
