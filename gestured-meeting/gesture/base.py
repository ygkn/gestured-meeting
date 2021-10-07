from abc import ABCMeta, abstractmethod
from enum import Enum, auto

from event import Event


class GestureType(Enum):
    toggle_hand = auto()
    leave_comfirm = auto()


class Gesture(metaclass=ABCMeta):
    running: bool

    gestured_event: Event[GestureType]
    observation_changed_event: Event[bool]

    @abstractmethod
    async def run(self):
        raise NotImplementedError()

    @abstractmethod
    async def stop(self):
        raise NotImplementedError()
