import pyautogui

from .base import Meeting


class ZoomMeeting(Meeting):
    def toggle_hand(self):
        pyautogui.hotkey("alt", "y")

    def leave_meeting(self):
        pyautogui.hotkey("alt", "q")
        pyautogui.press("enter")
