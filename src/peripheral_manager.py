import hashlib
import uuid
from typing import Callable


class PeripheralManager:

    def __init__(self):
        self.__callbacks: dict[int, dict[int,
                                         dict[bool, dict[uuid.UUID, Callable]]]] = dict()

    def register_callback(self, callback, key: int, modifiers: int, keyPress: bool) -> uuid.UUID:
        if key not in self.__callbacks:
            self.__callbacks[key] = dict()

        if modifiers not in self.__callbacks[key]:
            self.__callbacks[key][modifiers] = dict()

        if keyPress not in self.__callbacks[key][modifiers]:
            self.__callbacks[key][modifiers][keyPress] = dict()

        callback_id = uuid.uuid4()

        self.__callbacks[key][modifiers][keyPress][callback_id] = callback
        return callback_id

    def remove_callback(self, key: int, modifiers: int, keyPress: bool, callback_id: uuid.UUID):
        if key in self.__callbacks and modifiers in self.__callbacks[modifiers] and keyPress in self.__callbacks[key][modifiers] and callback_id in self.__callbacks[key][modifiers][keyPress]:
            del self.__callbacks[key][modifiers][keyPress][callback_id]

    def fire(self, key: int, modifiers: int, keyPress: bool, *args, **kwargs):
        if key in self.__callbacks and modifiers in self.__callbacks[key] and keyPress in self.__callbacks[key][modifiers]:
            callbackDict = self.__callbacks[key][modifiers][keyPress]
            for callbackId in callbackDict:
                callbackDict[callbackId](*args, **kwargs)
