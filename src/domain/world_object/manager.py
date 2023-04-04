from domain.coordinate_transformer.transformer import CoordinateTransformer
from domain.graphics.window import Window
from domain.world_object.object import WorldObject
from uuid import UUID, uuid4
from typing import Dict, List
from domain.event_system.event_system import EventSystem
from domain.shapes.line import Line


class WorldObjectManager:

    def __init__(self, event_system: EventSystem, window: Window) -> None:
        self.__event_system = event_system
        self.__registered_objects: Dict[UUID, WorldObject] = dict()
        self.__window = window

    def create(self) -> WorldObject:
        uuid = uuid4()
        object = WorldObject(uuid, self.__event_system, self.__window)
        self.__registered_objects[uuid] = object
        return object

    def remove(self, id: UUID):
        if id in self.__registered_objects:
            del self.__registered_objects[id]

    def get(self, id: UUID):
        if id in self.__registered_objects:
            return self.__registered_objects[id]
        else:
            raise RuntimeError('Failed to find world object')

    def update(self):
        for world_obj in self.__registered_objects.values():
            world_obj.update()

    def draw(self) -> List[Line]:
        """
        Returns the representation of all objects in the scene as a list of lines in world coordinates
        """
        lines: List[Line] = list()
        for world_obj in self.__registered_objects.values():
            object_lines = world_obj.draw()
            for local_line in object_lines:
                local_to_world_matrix = CoordinateTransformer.local_to_world(
                    world_obj)
                world_line = Line(
                    local_line.start * local_to_world_matrix, local_line.end * local_to_world_matrix)
                lines.append(world_line)
        return lines
