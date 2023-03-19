from event_system import EventSystem, Event
from peripheral_manager import PeripheralManager
from system import System
from window import Window
from wireframe import WireframeRenderer, Line, Polygon
from enum import Enum
from typing import List
from igs_math import Vector2
import pyglet


class PlacementMode(Enum):
    LINE = 0
    POLYGON = 1


class WireframeSpawner(System):

    def __init__(self, key_manager: PeripheralManager, mouse_manager: PeripheralManager,
                 evt_system: EventSystem, wireframe_renderer: WireframeRenderer, window: Window) -> None:
        super().__init__(key_manager, mouse_manager, evt_system)
        self.__current_points: List[Vector2] = list()
        self.__active = True
        self.__current_mouse_pos: Vector2 = Vector2(0.0, 0.0)
        self.__placement_mode: PlacementMode = PlacementMode.LINE
        self.__window = window
        self.__batch = pyglet.graphics.Batch()
        self.__wireframe_renderer = wireframe_renderer
        self.__poly_preview = False
        self.mouse_manager.register_callback(self.add_point, 1, 0, True)
        self.mouse_manager.register_callback(self.build_shape, 1, 2, True)
        self.key_manager.register_callback(
            self.change_mode, pyglet.window.key.F1, 0, True)
        self.key_manager.register_callback(
            self.toggle_poly_preview, 65507, 0, True)
        self.key_manager.register_callback(
            self.toggle_poly_preview, 65507, 2, False)
        self.evt_system.register_callback(
            Event.MOUSE_MOVE, self.update_mouse_pos)

    def toggle_poly_preview(self):
        self.__poly_preview = not self.__poly_preview

    def change_mode(self):
        self.__current_points.clear()
        if self.__placement_mode == PlacementMode.LINE:
            self.__placement_mode = PlacementMode.POLYGON
        else:
            self.__placement_mode = PlacementMode.LINE

    def add_point(self, pos: Vector2):
        world_pos = self.__window.viewport_to_world(pos)
        self.__current_points.append(world_pos)
        if self.__placement_mode == PlacementMode.LINE and len(self.__current_points) == 2:
            self.build_shape()

    def update_mouse_pos(self, pos: Vector2, delta: Vector2):
        world_pos = self.__window.viewport_to_world(pos)
        self.__current_mouse_pos = world_pos

    def build_shape(self, *args):
        match self.__placement_mode:
            case PlacementMode.LINE:
                if len(self.__current_points) < 2:
                    return
                line = Line(self.__current_points[0], self.__current_points[1])
                self.__wireframe_renderer.addWireframe(line)
            case PlacementMode.POLYGON:
                if len(self.__current_points) < 3:
                    return
                self.__wireframe_renderer.addWireframe(
                    Polygon(self.__current_points))
        self.__current_points.clear()

    def enable(self):
        self.__active = True

    def disable(self):
        self.__active = False
        self.__current_points.clear()

    def update(self):
        point_amount = len(self.__current_points)
        if not self.__active or point_amount == 0:
            return
        m = self.__window.world_to_viewport(self.__current_mouse_pos)

        if point_amount == 1:
            p = self.__window.world_to_viewport(self.__current_points[0])
            line = pyglet.shapes.Line(p.x, p.y, m.x, m.y, batch=self.__batch)
            self.__batch.draw()
            return

        lines = []  # previne as linhas que foram adicionadas aqui de serem coletadas pelo gc antes de serem desenhadas
        for i in range(1, point_amount):
            pi = self.__window.world_to_viewport(self.__current_points[i])
            pj = self.__window.world_to_viewport(self.__current_points[i-1])
            l = pyglet.shapes.Line(
                pj.x, pj.y, pi.x, pi.y, batch=self.__batch)
            lines.append(l)
        p = self.__window.world_to_viewport(
            self.__current_points[point_amount - 1])

        m = self.__window.world_to_viewport(
            self.__current_points[0]) if self.__poly_preview else m
        l = pyglet.shapes.Line(p.x, p.y, m.x, m.y, batch=self.__batch)
        lines.append(l)
        self.__batch.draw()
