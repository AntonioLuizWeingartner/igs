from system import System
from peripheral_manager import PeripheralManager
from event_system import EventSystem
from wireframe import WireframeRenderer, Line
from igs_math import Vector2
import random


class LineSpawner(System):

    def __init__(self, key_manager: PeripheralManager, mouse_manager: PeripheralManager,
                 evt_system: EventSystem, wireframe_renderer: WireframeRenderer, minPos: Vector2, maxPos: Vector2, amount: int):
        super().__init__(key_manager, mouse_manager, evt_system)
        size = maxPos - minPos
        for _ in range(amount):
            line_start = Vector2(size.x*random.random(),
                                 size.y*random.random()) + minPos
            line_end = Vector2(size.x*random.random(),
                               size.y*random.random()) + minPos
            line = Line(line_start, line_end)
            wireframe_renderer.addWireframe(line)

    def update(self):
        pass
