import logging
from argparse import ArgumentParser, Namespace

from flet import Page, run

from gui.layout import RandomizerGUI


def parse_arguments() -> Namespace:
    parser = ArgumentParser(description="Ex Machina Randomizer.")
    parser.add_argument(
        "--debug",
        "--dev",
        help="Debug mode.",
        action="store_true",
    )
    return parser.parse_args()


def set_log_config(debug: bool = False) -> None:
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="[%(levelname)s] %(asctime)s %(name)s: %(message)s",
        filename="randomizer.log",
        filemode="w",
        encoding="utf-8",
    )
    logging.getLogger("flet").setLevel(logging.ERROR)


def start(page: Page) -> None:
    arguments = parse_arguments()
    set_log_config(arguments.debug)

    randomizer_app = RandomizerGUI(
        width=800,
    )
    page.add(randomizer_app)


if __name__ == "__main__":
    run(start)
