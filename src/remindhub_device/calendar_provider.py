import datetime
from abc import ABC, abstractmethod
from typing import List

from calendar_event import CalendarEntry


class CalendarProvider(ABC):

    @property
    def cred_file(self) -> str:
        return self._cred_file

    @cred_file.setter
    def cred_file(self, cred_file: str) -> None:
        self._cred_file = cred_file

    @property
    def calender_url(self) -> str:
        return self._calender_url

    @calender_url.setter
    def calender_url(self, calender_url: str) -> None:
        self._calender_url = calender_url

    @property
    def event_list (self) -> list[CalendarEntry]:
        return self._event_list

    @event_list.setter
    def event_list(self, event_list: list[CalendarEntry]) -> None:
        self._event_list = event_list

    def __init__(self, cred_file: str, calender_url: str) -> None:
        self.cred_file = cred_file
        self.calender_url = calender_url
        self.event_list = []

    @abstractmethod
    def fetch_events_from_range(self, start_time: datetime, end_time: datetime) -> List[CalendarEntry]:
        pass

    def fetch_events_from_today(self) -> List[CalendarEntry]:
        return self.fetch_events_from_range(datetime.datetime.today(), datetime.datetime.today() + datetime.timedelta(days=1))
