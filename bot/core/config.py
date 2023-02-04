import os

from pydantic import BaseSettings


class Config(BaseSettings):
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    url: str = "http://app:8000/api/v1/google-calendar/"
