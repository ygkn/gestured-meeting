from collections.abc import Callable

from gesture import GestureKey
from meeting import MeetingKey
from PIL import Image
from pystray import Icon, Menu, MenuItem

icons = {
    "default": Image.open("icons/default.png"),
    "loading": Image.open("icons/loading.png"),
}


def noop():
    pass


def constTree(_):
    return True


class UI:
    __exit_handlers: set[Callable[[], None]]
    __change_gesture_handlers: set[Callable[[GestureKey], None]]
    __change_meeting_handlers: set[Callable[[MeetingKey], None]]
    __change_watching_handlers: set[Callable[[bool], None]]

    __gesture: GestureKey
    __meeting: MeetingKey
    __watching: bool

    __icon: Icon

    def __init__(
        self, gesture: GestureKey, meeting: MeetingKey, watching: bool
    ):
        self.__exit_handlers = set()

        self.__change_gesture_handlers = set()
        self.__change_meeting_handlers = set()
        self.__change_watching_handlers = set()

        self.__gesture = gesture
        self.__meeting = meeting
        self.__watching = watching

        self.__icon = Icon(
            "Gestured Meeting",
            icon=icons["loading"],
            title="Gestured Meeting",
            menu=Menu(
                MenuItem("Gestured Meeting", noop, enabled=False),
                MenuItem(
                    "Watching",
                    self.__handle_change_watching,
                    checked=self.__is_checked_watching,
                    radio=True,
                ),
                MenuItem(
                    "Gesture Provider",
                    Menu(
                        *(
                            MenuItem(
                                gesture.value,
                                self.__handle_change_gesture(gesture),
                                checked=self.__is__checked__gesture(gesture),
                                radio=True,
                            )
                            for gesture in GestureKey
                        )
                    ),
                ),
                MenuItem(
                    "Meeting Platform",
                    Menu(
                        *(
                            MenuItem(
                                meeting.value,
                                self.__handle_change_meeting(meeting),
                                radio=True,
                                checked=self.__is_checked_meeting(meeting),
                            )
                            for meeting in MeetingKey
                        )
                    ),
                ),
                MenuItem("Exit", self.__handle_click_exit),
            ),
        )

    def on_change_watching(self, handler: Callable[[bool], None]) -> None:
        self.__change_watching_handlers.add(handler)

    def __handle_change_watching(self, _, item):
        new_watching = not item.checked
        self.__watching = new_watching
        for handler in self.__change_watching_handlers:
            handler(new_watching)

    def __is_checked_watching(self, _):
        return self.__watching

    def on_change_gesture(self, handler: Callable[[GestureKey], None]) -> None:
        self.__change_gesture_handlers.add(handler)

    def __handle_change_gesture(self, gesture_key: GestureKey):
        def inner():
            self.__gesture = gesture_key
            for handler in self.__change_gesture_handlers:
                handler(gesture_key)

        return inner

    def __is__checked__gesture(self, gesture_key: GestureKey):
        def inner(_):
            self.__gesture == gesture_key

        return inner

    def on_change_meeting(self, handler: Callable[[MeetingKey], None]) -> None:
        self.__change_meeting_handlers.add(handler)

    def __handle_change_meeting(self, meeting_key: MeetingKey):
        def inner(_):
            self.__meeting = meeting_key
            for handler in self.__change_meeting_handlers:
                handler(meeting_key)

        return inner

    def __is_checked_meeting(self, meeting_key: MeetingKey):
        def inner(_):
            return self.__meeting == meeting_key

        return inner

    def __handle_click_exit(self):
        for handler in self.__exit_handlers:
            handler()

    def on_exit(self, handler: Callable[[], None]) -> None:
        self.__exit_handlers.add(handler)

    def set_loading(self, loading: bool):
        if loading:
            self.__icon.icon = icons["loading"]
        else:
            self.__icon.icon = icons["default"]

    def run(self):
        self.__icon.run()

    def stop(self):
        self.__icon.stop()
