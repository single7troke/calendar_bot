import os

from pydantic import BaseSettings


class Buttons(BaseSettings):
    back: str = "<- Back"
    list: str = "List"
    next: str = "Next"


class Config(BaseSettings):
    admin_commands: list = ["admin", "user_list", "new_user"]
    admin_roles: list = ["admin", "superuser"]
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    web_app_url: str = "http://app:8000/api/v1/"
    path_to_pem_file: str = "/etc/ssl/certs/YOURPUBLIC.pem"
    server_ip: str = ""
    server_url: str = ""
    tg_bot_token: str
    buttons = Buttons()
