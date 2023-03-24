from pydantic import BaseModel


class GoogleEvent(BaseModel):
    id: str = None
    summary: str = None
    start: str = None
    description: str = None


class GoogleEventList(BaseModel):
    events: list[GoogleEvent] = []


class BasicUser(BaseModel):
    user_id: str


class CreateUser(BasicUser):
    name: str
    role: str


