from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn

from api.v1 import google_calendar
from core.config import Config
from core.google import calendar

config = Config()

app = FastAPI(
    title=config.app_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    calendar.calendar = calendar.Calendar()

app.include_router(google_calendar.router, prefix="/api/v1/google-calendar", tags=["google-calendar"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
