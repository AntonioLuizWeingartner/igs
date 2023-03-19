from abc import ABC, abstractmethod
from typing import Dict
from peripheral_manager import PeripheralManager
from event_system import EventSystem
import uuid


class System(ABC):

    """
    A system is an abstraction that executes arbitray code every frame
    """

    def __init__(self, key_manager: PeripheralManager, mouse_manager: PeripheralManager, evt_system: EventSystem) -> None:
        super().__init__()
        self.__key_manager = key_manager
        self.__mouse_manager = mouse_manager
        self.__evt_system = evt_system

    @abstractmethod
    def update(self):
        pass

    @property
    def key_manager(self) -> PeripheralManager:
        return self.__key_manager

    @property
    def mouse_manager(self) -> PeripheralManager:
        return self.__mouse_manager

    @property
    def evt_system(self) -> EventSystem:
        return self.__evt_system


class SystemManager:

    def __init__(self):
        self.__systems: Dict[uuid.UUID, System] = dict()

    def add(self, system: System) -> uuid.UUID:
        sys_id = uuid.uuid4()
        self.__systems[sys_id] = system
        return sys_id

    def remove(self, sys_id: uuid.UUID):
        if sys_id in self.__systems:
            del self.__systems[sys_id]

    def update(self):
        for sys_key in self.__systems:
            self.__systems[sys_key].update()
