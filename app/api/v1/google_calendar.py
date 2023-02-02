from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from core.google.calendar import get_calendar
from core.utils import format_time, sort_by_start_time
from models.models import GoogleEvent, GoogleEventList

router = APIRouter()


@router.get("/{event_id}", response_model=GoogleEvent)
async def event_details(event_id: str, calendar=Depends(get_calendar)):
    data = await calendar.get_event_by_id(event_id)

    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='event not found')

    event = format_time([data])[0]

    return GoogleEvent(**event)


@router.get("", response_model=GoogleEventList)
async def event_list(calendar=Depends(get_calendar)):
    events = await calendar.event_list()
    events = events["items"]

    if not events:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='events not found')

    events = format_time(events)
    events = sort_by_start_time(events)

    data = GoogleEventList()
    data.events = [GoogleEvent(**i) for i in events]

    return data
