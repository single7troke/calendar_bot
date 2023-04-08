import os

from pydantic import BaseSettings


class Config(BaseSettings):
    refresh_time: int = 5  # watcher loop delay in seconds
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    web_app_url: str = "http://app:8000/api/v1/"
    tg_bot_token: str
