from enum import Enum

from .base import Meeting
from .meet import MeetMeeting
from .zoom import ZoomMeeting


class MeetingKey(Enum):
    zoom = "Zoom"
    meet = "Google Meet"


meetings: dict[MeetingKey, type[Meeting]] = {
    MeetingKey.zoom: ZoomMeeting,
    MeetingKey.meet: MeetMeeting,
}
