from enum import Enum


class EventType(Enum):
    NEW = "Появилась работа"
    DELETE = "Отменилась работа"
    UPDATE = "Изменилось описание работы"
