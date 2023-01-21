import json
from datetime import timezone, datetime

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds
from aiogoogle.excs import HTTPError

from core.config import Config

config = Config()
calendar = None


async def get_calendar():
    return calendar


class Calendar:
    CREDENTIALS = None

    def get_credentials(self):
        if self.CREDENTIALS:
            return self.CREDENTIALS

        service_account_key = json.load(open(config.google_service_account.path_to_keyfile))

        credentials = ServiceAccountCreds(
            scopes=config.google_service_account.scopes,
            **service_account_key
        )
        self.CREDENTIALS = credentials

        return self.CREDENTIALS

    async def event_list(self):
        async with Aiogoogle(service_account_creds=self.get_credentials()) as aiogoogle:
            date = datetime.now(tz=timezone.utc).astimezone().isoformat()
            calendar_v3 = await aiogoogle.discover('calendar', 'v3')
            try:
                events = await aiogoogle.as_service_account(
                    calendar_v3.events.list(calendarId=config.google_service_account.calendarId,
                                            timeMin=date)
                )
            except HTTPError:
                return None
            return events

    async def get_event_by_id(self, event_id):
        async with Aiogoogle(service_account_creds=self.get_credentials()) as aiogoogle:
            calendar_v3 = await aiogoogle.discover('calendar', 'v3')
            try:
                event = await aiogoogle.as_service_account(
                    calendar_v3.events.get(calendarId=config.google_service_account.calendarId,
                                           eventId=event_id)
                )
            except HTTPError:
                return None
            return event
