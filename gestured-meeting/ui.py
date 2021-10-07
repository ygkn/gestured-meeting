from event import Event
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
    exit_event: Event[None]
    change_gesture_event: Event[GestureKey]
    change_meeting_event: Event[MeetingKey]
    change_watching_event: Event[bool]

    __gesture: GestureKey
    __meeting: MeetingKey
    __watching: bool

    __icon: Icon

    def __init__(
        self, gesture: GestureKey, meeting: MeetingKey, watching: bool
    ):
        self.exit_event = Event()

        self.change_gesture_event = Event()
        self.change_meeting_event = Event()
        self.change_watching_event = Event()

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

    def __handle_change_watching(self, _, item):
        new_watching = not item.checked
        self.__watching = new_watching
        self.change_watching_event.emit(new_watching)

    def __is_checked_watching(self, _):
        return self.__watching

    def __handle_change_gesture(self, gesture_key: GestureKey):
        def inner():
            self.__gesture = gesture_key
            self.change_gesture_event(gesture_key)

        return inner

    def __is__checked__gesture(self, gesture_key: GestureKey):
        def inner(_):
            return self.__gesture == gesture_key

        return inner

    def __handle_change_meeting(self, meeting_key: MeetingKey):
        def inner(_):
            self.__meeting = meeting_key
            self.change_meeting_event.emit(meeting_key)

        return inner

    def __is_checked_meeting(self, meeting_key: MeetingKey):
        def inner(_):
            return self.__meeting == meeting_key

        return inner

    def __handle_click_exit(self):
        self.exit_event.emit(None)

    def set_loading(self, loading: bool):
        if loading:
            self.__icon.icon = icons["loading"]
        else:
            self.__icon.icon = icons["default"]

    def run(self):
        self.__icon.run()

    def stop(self):
        self.__icon.stop()
