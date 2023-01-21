from pydantic import BaseModel


class GoogleEventShort(BaseModel):
    summary: str = None
    start: dict = None


class GoogleEvent(GoogleEventShort):
    description: str = None


class GoogleEventList(BaseModel):
    events: list[GoogleEventShort] = []
