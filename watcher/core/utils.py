import requests

from core.config import Config

config = Config()
TOKEN = config.tg_bot_token


def event_list() -> dict:
    url = f"{config.web_app_url}google-calendar"
    data = requests.get(url=url).json()
    return data


def get_all_users() -> list:
    url = f"{config.web_app_url}users/"
    data = requests.get(url).json()
    return data["users_id"]


def send_message(chat_id, msg) -> None:
    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={msg}"
    )


def message_sender(messages: dict) -> None:
    ids = get_all_users()
    for message in messages:
        for chat_id in ids:
            message_text = f"{messages[message]}"
            send_message(chat_id, message_text)