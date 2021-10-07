from abc import ABCMeta, abstractmethod


class Meeting(metaclass=ABCMeta):
    @abstractmethod
    def leave_meeting(self):
        raise NotImplementedError()

    @abstractmethod
    def toggle_hand(self):
        raise NotImplementedError()
