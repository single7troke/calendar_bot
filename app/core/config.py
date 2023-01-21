import os
from pydantic import BaseSettings


class Config(BaseSettings):
    app_name: str = "calendar_api"
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
