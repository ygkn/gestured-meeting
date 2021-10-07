from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from enum import Enum, auto


class GestureEvent(Enum):
    toggle_hand = auto()
    leave_comfirm = auto()


GestureEventHandler = Callable[[GestureEvent], None]


ObservationChangedEventHandler = Callable[[bool], None]


class Gesture(metaclass=ABCMeta):
    running: bool

    @abstractmethod
    def on_gestured(self, handler: GestureEventHandler):
        raise NotImplementedError()

    @abstractmethod
    def on_observation_changed(self, handler: ObservationChangedEventHandler):
        raise NotImplementedError()

    @abstractmethod
    async def run(self):
        raise NotImplementedError()

    @abstractmethod
    async def stop(self):
        raise NotImplementedError()
