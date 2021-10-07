import asyncio
import threading

from arg import parse_args
from gesture import GestureKey, gestures
from gesture.base import Gesture, GestureEvent
from meeting import MeetingKey, meetings
from meeting.base import Meeting
from ui import UI


class GesturedMeeting:
    __gesture_key: GestureKey
    __gesture: Gesture
    __meeting_key: MeetingKey
    __meeting: Meeting
    __watching: bool
    __ui: UI

    __exit_event: asyncio.Event

    def __init__(self):

        args = parse_args()

        self.__gesture_key = GestureKey[args.gesture]
        self.__gesture = gestures[self.__gesture_key]()

        self.__meeting_key = MeetingKey[args.meeting]
        self.__meeting = meetings[self.__meeting_key]()

        self.__watching = args.run

        self.__ui = UI(
            gesture=self.__gesture_key,
            meeting=self.__meeting_key,
            watching=self.__watching,
        )

        self.__gesture.on_gestured(self.__on_gestured)
        self.__gesture.on_observation_changed(self.__on_observation_changed)

        self.__ui.on_change_gesture(self.__on_change_gesture)
        self.__ui.on_change_meeting(self.__on_change_meeting)
        self.__ui.on_change_watching(self.__on_change_watching)
        self.__ui.on_exit(self.__on_exit)

    def __on_gestured(self, event: GestureEvent):
        if event == GestureEvent.toggle_hand:
            self.__meeting.toggle_hand()

        if event == GestureEvent.leave_comfirm:
            self.__meeting.leave_meeting()

    def __on_observation_changed(self, observation: bool):
        self.__ui.set_loading(not observation)

    def __on_change_gesture(self, gesture_key: GestureKey):
        old_gesture = self.__gesture

        self.__gesture_key = gesture_key
        self.__gesture = gestures[self.__gesture_key]()

        if old_gesture is not None and old_gesture.running:

            async def stop_and_run():
                await old_gesture.stop()
                await self.__gesture.run()

            loop = asyncio.get_event_loop()
            loop.run_until_complete(stop_and_run())

    def __on_change_meeting(self, meeting_key: MeetingKey):
        self.__meeting_key = meeting_key
        self.__meeting = meetings[self.__meeting_key]()

    def __on_change_watching(self, watching: bool):
        self.__watching = watching

        if watching and not self.__gesture.running:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.__gesture.run())

        if not watching and self.__gesture.running:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.__gesture.stop())

    def __on_exit(self):
        self.__exit_event.set()
        self.__stop_ui()

    async def __run(self):
        self.__exit_event = asyncio.Event()

        await self.__gesture.run()

    async def __stop(self):
        await self.__gesture.stop()

    async def __wait_for_exit(self):
        await self.__exit_event.wait()

    async def __run_to_exit(self):
        await self.__run()
        await self.__wait_for_exit()
        await self.__stop()

    def __run_ui(self):
        self.__ui.run()

    def __stop_ui(self):
        self.__ui.stop()

    def __thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(self.__run_to_exit())
        except KeyboardInterrupt:
            loop.run_until_complete(self.__stop())

        finally:
            loop.close()

    def run(self):
        thread = threading.Thread(target=self.__thread)
        thread.start()

        self.__run_ui()


if __name__ == "__main__":
    gestured_meeting = GesturedMeeting()
    gestured_meeting.run()
