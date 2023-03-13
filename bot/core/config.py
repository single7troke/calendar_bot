import os

from pydantic import BaseSettings


class Config(BaseSettings):
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    google_calendar_events_url: str = "http://app:8000/api/v1/google-calendar/"
    path_to_pem_file: str = "/etc/ssl/certs/YOURPUBLIC.pem"
    server_ip: str
    server_url: str
    tg_bot_token: str
