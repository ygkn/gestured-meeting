import asyncio
import threading

from arg import parse_args
from gesture import GestureKey, gestures
from gesture.base import Gesture, GestureType
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

    async def __listen_gestured(self):
        while True:
            gesture_type = await self.__gesture.gestured_event.listen()

            if gesture_type == GestureType.toggle_hand:
                self.__meeting.toggle_hand()

            if gesture_type == GestureType.leave_comfirm:
                self.__meeting.leave_meeting()

    async def __listen_observation_changed(self):
        while True:
            observation = (
                await self.__gesture.observation_changed_event.listen()
            )
            self.__ui.set_loading(not observation)

    async def __listen_change_gesture(self):
        while True:
            gesture_key = await self.__ui.change_gesture_event.listen()

            if gesture_key == self.__gesture_key:
                continue

            old_gesture = self.__gesture

            self.__gesture_key = gesture_key
            self.__gesture = gestures[self.__gesture_key]()

            if old_gesture is not None and old_gesture.running:

                await asyncio.gather(old_gesture.stop(), self.__gesture.run())

    async def __listen_change_meeting(self):
        while True:
            meeting_key = await self.__ui.change_meeting_event.listen()

            if meeting_key == self.__meeting:
                continue

            self.__meeting_key = meeting_key
            self.__meeting = meetings[self.__meeting_key]()

    async def __listen_change_watching(self):
        while True:
            watching = await self.__ui.change_watching_event.listen()

            if watching == self.__watching:
                continue

            self.__watching = watching

            if watching:
                await self.__gesture.run()
                self.__ui.set_loading(True)

            if not watching:
                self.__ui.set_loading(False)
                await self.__gesture.stop()

    async def __run(self):
        await self.__gesture.run()

    async def __stop(self):
        if self.__gesture.running:
            await self.__gesture.stop()

    async def __run_async(self):
        try:
            _, pending = await asyncio.wait(
                (
                    asyncio.gather(
                        self.__run(),
                        self.__listen_gestured(),
                        self.__listen_observation_changed(),
                        self.__listen_change_gesture(),
                        self.__listen_change_meeting(),
                        self.__listen_change_watching(),
                    ),
                    asyncio.create_task(self.__ui.exit_event.listen()),
                ),
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()
            try:
                await asyncio.wait(pending)
            except asyncio.exceptions.CancelledError:
                pass
            finally:
                self.__ui.stop()
        except KeyboardInterrupt:
            pass
        finally:
            await self.__stop()

    def run(self):
        thread = threading.Thread(
            target=asyncio.run, args=(self.__run_async(),)
        )
        thread.start()
        self.__ui.run()


if __name__ == "__main__":
    gestured_meeting = GesturedMeeting()
    gestured_meeting.run()
