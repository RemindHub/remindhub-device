from dataclasses import dataclass
import datetime


@dataclass
class CalendarEntry:
    title: str
    attendees: list[str]
    description: str
    start_time: datetime.datetime
    end_time: datetime.datetime
