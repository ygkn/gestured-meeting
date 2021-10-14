from enum import Enum

from .base import Gesture
from .ble import BLEGesture


class GestureKey(Enum):
    ble = "BLE"


gestures: dict[GestureKey, type[Gesture]] = {GestureKey.ble: BLEGesture}
