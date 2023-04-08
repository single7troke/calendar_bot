import logging
from time import sleep

from core.config import Config
from core.utils import event_list, message_sender
from core.models import EventType


config = Config()

current_events = dict()
logging.basicConfig(format="%(asctime)s %(message)s",
                    datefmt="%m/%d/%Y %I:%M:%S %p %Z",
                    level=logging.INFO)


def fill_current_events():
    data = event_list()
    for event in data["events"]:
        current_events[event["id"]] = {"start": event["start"], "description": event["description"]}


def event_watcher():
    global current_events
    while True:
        data = event_list()
        new_events = {
            event["id"]: {"start": event["start"], "description": event["description"]} for event in data["events"]
        }
        messages = dict()

        # Если все события идентичны, ничего не делаем.
        if current_events == new_events:
            logging.info("nothing happened")
            sleep(config.refresh_time)
            continue

        # Иначе сравниваем события
        for event in new_events:
            # если события идентичны, то убираем событие из словоря current_events
            if event in current_events and new_events[event]["description"] == current_events[event]["description"]:
                current_events.pop(event)

            # Если события отличаются описанием, создаем сообщение об обновлении события
            elif event in current_events and new_events[event]["description"] != current_events[event]["description"]:
                logging.info(f"event {new_events[event]['start']} updated")
                current_events.pop(event)
                messages[event] = f"{EventType.UPDATE.value} {new_events[event]['start']}"

            # Если события нет в словаре current_events, создаем сообщение о новом событии
            elif event not in current_events:
                logging.info(f"new event {new_events[event]['start']}")
                messages[event] = f"{EventType.NEW.value} {new_events[event]['start']}"

        # Если в current_events остались события значит эти события были удалены.
        # Создаем сообщение/сообщения об удалении
        if current_events:
            for event in current_events:
                logging.info(f"event {current_events[event]['start']} deleted")
                messages[event] = f"{EventType.DELETE.value} {current_events[event]['start']}"

        current_events = new_events
        message_sender(messages=messages)

        sleep(config.refresh_time)


if __name__ == "__main__":
    fill_current_events()
    event_watcher()
