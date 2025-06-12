import os
from datetime import datetime
from logging import exception
from typing import List, Any
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.remindhub_device.calendar_event import CalendarEntry
from src.remindhub_device.calendar_provider import CalendarProvider


class GoogleCalendarProvider(CalendarProvider):
    _scopes = ['https://www.googleapis.com/auth/calendar.readonly']


    def __init__(self, calender_url: str):
        super().__init__(calender_url)
        self.cred_file = os.path.join(self.base_dir, "google", "credentials.json")
        self._token_file = os.path.join(self.base_dir, "google", "token.json")


    def fetch_events_from_range(self, start_time: datetime, end_time: datetime) -> List[CalendarEntry]:

        # Authenticate the user
        self._authenticate()

        if self.credentials is None:
            print("Credentials not found. Exiting.")
            # TODO: Implement logging system
            return []

        events = self._fetch_events(start_time, end_time)

        # Parse calendar events into the CalendarEntries
        return _parse_to_calender_entry(events)


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
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.cred_file, scopes=self._scopes
                    )
                    creds = flow.run_local_server(port=0, open_browser=True)
                    with open(self._token_file, 'w') as token:
                        token.write(creds.to_json())
                except exception as error:
                    print("An error occurred while authenticating the user: %s" % error)
                    # TODO: Implement logging system

        self.credentials = creds


    def _fetch_events(self, start_time: datetime, end_time: datetime) -> list[Any]:

        # Start API service
        service = build('calendar', 'v3', credentials=self.credentials)

        try:
            # Fetch calendar events
            events_result = (
                service.events()
                .list(
                    calendarId=self.calender_url,
                    timeMin=start_time.isoformat(),
                    timeMax=end_time.isoformat(),
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
        except HttpError as e:
            print("An error occurred: %s" % e)
            # TODO: Implement logging system
            return []

        return events_result.get("items", [])


# --- Static-Scope --- #

def _parse_to_calender_entry(events) -> list[CalendarEntry]:
    entry_list = []

    for event in events:
        title = event["summary"]
        description = event["description"]
        start_time = event["start"].get("dateTime")
        end_time = event["end"].get("dateTime")
        attendees = []

        # fetch attendee mail
        for i in event.get("attendees", []):
            attendees.append(i["email"])

        entry_list.append(
            CalendarEntry(title=title, description=description, start_time=start_time, end_time=end_time,
                          attendees=attendees))

    return entry_list
