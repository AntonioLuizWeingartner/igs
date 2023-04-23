from typing import Dict, Callable
from enum import Enum
import uuid


class Event(Enum):
    KEY_PRESS = 0,
    KEY_RELEASE = 1,
    MOUSE_MOVE = 2,
    MOUSE_PRESS = 3,
    MOUSE_RELEASE = 4,
    MOUSE_SCROLL = 5,
    MOUSE_DRAG = 6,
    CREATE_POLYGON = 7,
    CREATE_POINT = 8,
    CREATE_LINE = 9,


class EventSystem:

    def __init__(self) -> None:
        self.__callbacks: Dict[Event, Dict[uuid.UUID, Callable]] = dict()

    def register_callback(self, event: Event, callback: Callable) -> uuid.UUID:
        callback_id = uuid.uuid4()
        if event not in self.__callbacks:
            self.__callbacks[event] = dict()
        self.__callbacks[event][callback_id] = callback
        return callback_id

    def remove_callback(self, event: Event, callback_id: uuid.UUID):
        if event in self.__callbacks and callback_id in self.__callbacks[event]:
            del self.__callbacks[event][callback_id]

    def fire(self, event: Event, *args, **kwargs):
        print("Firing event: ", event, *args, **kwargs)
        if event in self.__callbacks:
            for callback_id in self.__callbacks[event]:
                self.__callbacks[event][callback_id](*args, **kwargs)
