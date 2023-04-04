from typing import List
from uuid import UUID
from domain.event_system.event_system import EventSystem
from domain.graphics.window import Window
from domain.math.vector2 import Vector2
from domain.shapes.line import Line
from domain.world_object.object import WorldObject, WorldObjectComponent


class LineComponent(WorldObjectComponent):

    def __init__(self, owner: WorldObject, id: UUID, event_system: EventSystem, window: Window):
        super().__init__(owner, id, event_system, window)
        self.line_start = Vector2(0, 0)
        self.line_end = Vector2(0, 0)

    def draw(self) -> List[Line] | None:
        return [Line(self.line_start, self.line_end)]
