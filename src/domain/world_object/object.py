from __future__ import annotations
from typing import Dict, Type, List

import numpy as np
from domain.event_system.event_system import EventSystem
from domain.graphics.window import Window
from domain.math.vector2 import Vector2
from uuid import UUID, uuid4

from domain.shapes.line import Line


class WorldObjectComponent:

    def __init__(self, owner: WorldObject, id: UUID, event_system: EventSystem, window: Window):
        self.__owner = owner
        self.__id = id
        self.__event_system = event_system
        self.__window = window

    @property
    def id(self) -> UUID:
        return self.__id

    @property
    def owner(self) -> WorldObject:
        return self.__owner

    @property
    def event_system(self) -> EventSystem:
        return self.__event_system

    @property
    def window(self) -> Window:
        return self.__window

    def on_init(self):
        pass

    def draw(self) -> List[Line] | None:
        """
        Returns an array of lines that represents the component in local space coordiantes
        """
        pass

    def update(self):
        pass


class WorldObject:
    """
    An arbitrary entity that has a position, a scale and an orientation in the world
    Its behaviour is defined by the components that it has
    """
    next_obj_id = 0

    def __init__(self, id: UUID, event_system: EventSystem, window: Window, position: Vector2 = Vector2(0, 0), scale: Vector2 = Vector2(1, 1), rotation: float = 0.0, name: str | None = None):
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.__registered_components: Dict[UUID, WorldObjectComponent] = dict()
        self.__event_system = event_system
        self.__id = id
        self.__window = window
        self.__name = "Object " + \
            str(WorldObject.next_obj_id) if name is None else name

    def add_component(self, cp: Type[WorldObjectComponent]) -> WorldObjectComponent:
        uuid = uuid4()
        component = cp(self, uuid, self.__event_system, self.__window)
        component.on_init()
        self.__registered_components[uuid] = component
        return component

    def remove_component(self, cp_id: UUID):
        if cp_id in self.__registered_components:
            del self.__registered_components[cp_id]

    def get_component(self, cp_id: UUID) -> WorldObjectComponent:
        if cp_id in self.__registered_components:
            return self.__registered_components[cp_id]
        else:
            raise RuntimeError('Component id not found')

    def update(self):
        for cp in self.__registered_components.values():
            cp.update()

    def draw(self) -> List[Line]:
        """
        Returns an array of lines that represents the object in local space coordinates
        """
        lines = list()
        for cp in self.__registered_components.values():
            cp_lines = cp.draw()
            if cp_lines is not None:
                lines = lines + cp_lines
        return lines

    @property
    def id(self) -> UUID:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name
