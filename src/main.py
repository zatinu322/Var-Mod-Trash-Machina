import logging

import gui.flet_window as flet_window


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
    flet_window.start()


if __name__ == "__main__":
    main_gui()
