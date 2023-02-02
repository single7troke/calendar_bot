import os
from time import sleep

from core.utils import event_list, message_sender
from core.models import EventType


current_events = dict()
chat_id_list = os.getenv("CHAT_IDS").split(",")


def fill_current_events():
    data = event_list()
    for event in data["events"]:
        current_events[event["id"]] = [event["start"], event["description"]]


def event_watcher():
    TICK_TACK = "Tick"
    global current_events
    while True:
        if TICK_TACK == "Tick":
            print(TICK_TACK)
            TICK_TACK = "Tack"
        else:
            print(TICK_TACK)
            TICK_TACK = "Tick"

        data = event_list()
        new_events = {event["id"]: [event["start"], event["description"]] for event in data["events"]}
        messages = dict()

        # Если все события идентичны, ничего не делаем.
        if current_events == new_events:
            sleep(5)
            continue

        # Иначе сравниваем события
        for event in new_events:
            # если события идентичны, то убираем событие из словоря current_events
            if event in current_events and new_events[event][1] == current_events[event][1]:
                current_events.pop(event)

            # Если события отличаются описанием, создаем сообщение об обновлении события
            elif event in current_events and new_events[event][1] != current_events[event][1]:
                current_events.pop(event)
                messages[event] = f"{EventType.UPDATE.value} {new_events[event][0]}"

            # Если события нет в словаре current_events, создаем сообщение о новом событии
            elif event not in current_events:
                messages[event] = f"{EventType.NEW.value} {new_events[event][0]}"

        # Если в current_events остались события значит эти события были удалены.
        # Создаем сообщение/сообщения об удалении
        if current_events:
            for event in current_events:
                messages[event] = f"{EventType.DELETE.value} {current_events[event][0]}"

        current_events = new_events
        message_sender(chat_id_list, messages)

        sleep(5)


if __name__ == "__main__":
    fill_current_events()
    event_watcher()
