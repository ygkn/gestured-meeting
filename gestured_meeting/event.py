import asyncio
from typing import Generic, TypeVar

V = TypeVar("V")


class Event(Generic[V]):
    __value: V
    __asyncio_events: set[asyncio.Event]

    def __init__(self) -> None:
        super().__init__()
        self.__asyncio_events = set()

    def emit(self, value: V):
        self.__value = value
        for asyncio_event in self.__asyncio_events:
            asyncio_event.set()

    async def listen(self):
        asyncio_event = asyncio.Event()

        self.__asyncio_events.add(asyncio_event)

        await asyncio_event.wait()

        asyncio_event.clear()

        self.__asyncio_events.discard(asyncio_event)

        return self.__value
