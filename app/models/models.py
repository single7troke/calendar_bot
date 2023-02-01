from pydantic import BaseModel


class GoogleEvent(BaseModel):
    id: str = None
    summary: str = None
    start: str = None
    description: str = None


class GoogleEventList(BaseModel):
    events: list[GoogleEvent] = []
