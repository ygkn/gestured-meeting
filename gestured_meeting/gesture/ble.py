import asyncio

from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from ..event import Event
from .base import Gesture, GestureType

name = "gestured meeting"
characteristic_uuid = "1b2ffc7b-ba3d-4577-9c5e-ed01287faaf3"


class BLEGesture(Gesture):
    __clients: set[BleakClient]
    __scanner: BleakScanner

    def __init__(self) -> None:
        super().__init__()

        self.running = False

        self.__clients = set()

        self.gestured_event = Event()
        self.observation_changed_event = Event()

        self.__scanner = BleakScanner()

        self.__scanner.register_detection_callback(self.__detection_callback)

    async def __detection_callback(
        self, device: BLEDevice, _: AdvertisementData
    ):
        if isinstance(device.name, str) and device.name.lower() == name:
            client = BleakClient(device)
            client.set_disconnected_callback(self.__disconnected_callback)
            await client.connect()
            await client.start_notify(
                characteristic_uuid, self.__notification_callback
            )
            self.__clients.add(client)

            self.observation_changed_event.emit(len(self.__clients) != 0)

    def __disconnected_callback(self, client: BleakClient):
        self.__clients.discard(client)

        self.observation_changed_event.emit(len(self.__clients) != 0)

    def __notification_callback(self, _: int, data: bytearray):
        message = data.decode(encoding="utf-8")
        if message in GestureType.__members__:
            self.gestured_event.emit(GestureType[message])

    async def run(self):
        await self.__scanner.start()
        self.running = True

    async def stop(self):
        self.running = False

        await self.__scanner.stop()

        await asyncio.gather(
            *(
                client.stop_notify(characteristic_uuid)
                for client in self.__clients
            )
        )

        await asyncio.gather(
            *(client.disconnect() for client in self.__clients)
        )
