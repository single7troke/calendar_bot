import os
from pydantic import BaseSettings


class GoogleServiceAccount(BaseSettings):
    path_to_keyfile: str = os.path.dirname(os.path.abspath(__file__)) + "/google/keyfile.json"
    scopes = ['https://www.googleapis.com/auth/calendar']
    calendarId: str


class RedisSettings(BaseSettings):
    host: str = 'localhost'
    port: int = 6379

    class Config:
        env_prefix = 'redis_'


class Config(BaseSettings):
    app_name: str = "calendar_api"
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    google_service_account: GoogleServiceAccount = GoogleServiceAccount()
    redis: RedisSettings = RedisSettings()
