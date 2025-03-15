from argparse import ArgumentParser, Namespace
import logging

import gui.flet_window as flet_window


def parse_args() -> Namespace:
    parser = ArgumentParser(description='')
    parser.add_argument('--debug',
                        '--dev',
                        help='Режим отладки',
                        action='store_true')
    return parser.parse_args()


def main_gui() -> None:
    args = parse_args()

    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(
        filename="randomizer.log",
        level=log_level,
        format=" ".join([
            "[%(levelname)s]",
            "%(asctime)s",
            "%(name)s:",
            "%(message)s",
        ]),
        filemode="w",
        datefmt="%d/%m %H:%M:%S",
        encoding="utf-8"
    )
    logging.getLogger("flet_core").setLevel(logging.ERROR)
    logging.getLogger("flet_runtime").setLevel(logging.ERROR)
    logging.getLogger("asyncio").setLevel(logging.ERROR)

    flet_window.start()


if __name__ == "__main__":
    main_gui()
