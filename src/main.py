import logging
from argparse import ArgumentParser, Namespace

from flet import run

from gui.app import start_app


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
        # filename="randomizer.log",
        # filemode="w",
        # encoding="utf-8",
    )
    logging.getLogger("flet").setLevel(logging.ERROR)
    logging.getLogger("flet_desktop").setLevel(logging.ERROR)


def main() -> None:
    arguments = parse_arguments()
    set_log_config(arguments.debug)

    run(start_app)


if __name__ == "__main__":
    main()
