from abc import ABC, abstractmethod
from typing import List

from src.remindhub_device.calender_event import CalenderEvent


class CalenderWrapper(ABC):

    @property
    @abstractmethod
    def cred_file(self) -> str:
        return self.cred_file

    @cred_file.setter
    @abstractmethod
    def cred_file(self, cred_file: str) -> None:
        self.cred_file = cred_file

    @property
    @abstractmethod
    def calender_url(self) -> str:
        return self.calender_url

    @calender_url.setter
    @abstractmethod
    def calender_url(self, calender_url: str) -> None:
        self.calender_url = calender_url

    @property
    @abstractmethod
    def event_list (self) -> list[CalenderEvent]:
        return self.event_list

    @abstractmethod
    def fetch_events(self, count: int) -> List[CalenderEvent]:
        pass