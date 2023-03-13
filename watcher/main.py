import json
import logging
import os
from time import sleep

from core.utils import event_list, message_sender
from core.models import EventType


current_events = dict()
users_id = []
logging.basicConfig(format="%(asctime)s %(message)s",
                    datefmt="%m/%d/%Y %I:%M:%S %p %Z",
                    level=logging.INFO)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "users_id.json")) as file:
    data = json.load(file)
    for user_id in data["users"].values():
        users_id.append(user_id)


def fill_current_events():
    data = event_list()
    for event in data["events"]:
        current_events[event["id"]] = [event["start"], event["description"]]


def event_watcher():
    global current_events
    while True:
        data = event_list()
        new_events = {event["id"]: [event["start"], event["description"]] for event in data["events"]}
        messages = dict()

        # Если все события идентичны, ничего не делаем.
        if current_events == new_events:
            logging.info("nothing happened")
            sleep(5)
            continue

        # Иначе сравниваем события
        for event in new_events:
            # если события идентичны, то убираем событие из словоря current_events
            if event in current_events and new_events[event][1] == current_events[event][1]:
                current_events.pop(event)

            # Если события отличаются описанием, создаем сообщение об обновлении события
            elif event in current_events and new_events[event][1] != current_events[event][1]:
                logging.info(f"event {new_events[event][0]} updated")
                current_events.pop(event)
                messages[event] = f"{EventType.UPDATE.value} {new_events[event][0]}"

            # Если события нет в словаре current_events, создаем сообщение о новом событии
            elif event not in current_events:
                logging.info(f"new event {new_events[event][0]}")
                messages[event] = f"{EventType.NEW.value} {new_events[event][0]}"

        # Если в current_events остались события значит эти события были удалены.
        # Создаем сообщение/сообщения об удалении
        if current_events:
            for event in current_events:
                logging.info(f"event {current_events[event][0]} deleted")
                messages[event] = f"{EventType.DELETE.value} {current_events[event][0]}"

        current_events = new_events
        message_sender(users_id, messages)

        sleep(5)


if __name__ == "__main__":
    fill_current_events()
    event_watcher()
