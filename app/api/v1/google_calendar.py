from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from core.google.calendar import get_calendar
from models.models import GoogleEvent, GoogleEventList

router = APIRouter()


@router.get("/{event_id}", response_model=GoogleEvent)
async def event_details(event_id: str, calendar=Depends(get_calendar)):
    data = await calendar.get_event_by_id(event_id)

    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='event not found')

    return GoogleEvent(**data)


@router.get("", response_model=GoogleEventList)
async def event_list(calendar=Depends(get_calendar)):
    events = await calendar.event_list()
    data = GoogleEventList()
    data.events = [GoogleEvent(**i) for i in events["items"]]

    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='events not found')

    return data
