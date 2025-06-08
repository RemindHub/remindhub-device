import dataclasses
import datetime


@dataclasses.dataclass
class CalenderEvent:
    def __init__(self, title: str, attendees: list[str], description: str, start_time: datetime,
                 end_time: datetime) -> None:
        self.title: str = title
        self.attendees: list[str] = attendees
        self.description: str = description
        self.start_time: datetime.datetime = start_time
        self.end_time: datetime.datetime = end_time
