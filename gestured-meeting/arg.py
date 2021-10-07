from argparse import ArgumentParser, BooleanOptionalAction

from gesture import GestureKey
from meeting import MeetingKey

description = "Online meeting with gesture."


def parse_args():
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--gesture",
        "-g",
        default="ble",
        choices=GestureKey.__members__,
        help="Gesture provider. Right now, supported BLE only.",
    )
    parser.add_argument(
        "--meeting",
        "-m",
        default="zoom",
        choices=MeetingKey.__members__,
        help="Meeting platform",
    )
    parser.add_argument(
        "--run",
        "-r",
        action=BooleanOptionalAction,
        help="Run on start.",
        default=True,
    )

    return parser.parse_args()
