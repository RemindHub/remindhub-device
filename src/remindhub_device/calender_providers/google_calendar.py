import os
from datetime import datetime
from logging import exception
from typing import List

from src.remindhub_device.calendar_event import CalendarEntry
from src.remindhub_device.calendar_provider import CalendarProvider
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleCalendarProvider(CalendarProvider):
    _scopes = ['https://www.googleapis.com/auth/calendar.readonly']
    _token_file = "./token.json"

    def fetch_events_from_range(self, start_time: datetime, end_time: datetime) -> List[CalendarEntry]:
        self._authenticate()

        if self.credentials is None:
            print("Credentials not found. Exiting.")
            # TODO: Implement logging system
            return []

        return []



    def _authenticate(self):
        creds = None
        # load in existing cred_file
        if os.path.exists(self._token_file):
            creds = Credentials.from_authorized_user_file(self._token_file, scopes=self._scopes)

        if not creds or not creds.valid:
            # refresh token if needed
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            # initialize credentials via Googles OAuth system
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.cred_file, scopes=self._scopes
                )
                creds = flow.run_local_server(port=0, open_browser=True)
                with open(self._token_file, 'w') as token:
                    token.write(creds.to_json())

        self.credentials = creds