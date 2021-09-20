import asyncio
from bleak import BleakScanner
from bleak import BleakClient
import pyautogui


CHARACTERISTIC_UUID = "1b2ffc7b-ba3d-4577-9c5e-ed01287faaf3"


def notification_callback(sender: int, data: bytearray):
    message = data.decode(encoding="utf-8")

    print(message)
    if message == "toggle_hand":
        pyautogui.hotkey("alt", "y")

    if message == "leave_comfirm":
        pyautogui.hotkey("alt", "q")
        pyautogui.press("enter")


disconnected_event = asyncio.Event()


def disconnected_callback():
    print("Disconnected callback called!")
    disconnected_event.set()


async def run():
    devices = await BleakScanner.discover()
    address = (next(filter(lambda d: d.name == "ESP32", devices), None)).address

    client = BleakClient(address, disconnected_callback=disconnected_callback)

    print(address)

    await client.connect(timeout=120.0)
    print("connected!")
    await client.start_notify(CHARACTERISTIC_UUID, notification_callback)
    print("listen")
    await disconnected_event.wait()
    await client.stop_notify()


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
