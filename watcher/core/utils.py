import os

import requests


TOKEN = os.getenv("TG_BOT_TOKEN")


def event_list():
    url = "http://app:8000/api/v1/google-calendar"
    data = requests.get(url=url).json()
    return data


def send_message(chat_id, msg):
    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={msg}"
    )


def message_sender(ids: list, messages: dict):
    for message in messages:
        for chat_id in ids:
            message_text = f"{messages[message]}"
            send_message(chat_id, message_text)