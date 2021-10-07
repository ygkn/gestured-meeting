import pyautogui

from .base import Meeting


class MeetMeeting(Meeting):
    def toggle_hand(self):
        pyautogui.hotkey("ctrl", "alt", "h")

    def leave_meeting(self):
        pyautogui.hotkey("ctrl", "w")
