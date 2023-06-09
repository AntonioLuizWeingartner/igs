import pyglet
import uuid
import numpy as np
from event_system import Event, EventSystem
from igs_math import Vector2, Matrix3x3
from window import Window
from typing import List
from copy import deepcopy


class DrawableObject:

    obj_count = 0

    def __init__(self, name: str | None = None):
        self.__position = Vector2(0, 0)
        self.__rotation = 0.0
        self.__scale = Vector2(1, 1)
        self.__update_transformation_matrix()
        self.__id = uuid.uuid4()
        if name is None:
            self.__name = self.__class__.__name__ + " " + \
                str(DrawableObject.obj_count)
        else:
            self.__name = name
        DrawableObject.obj_count += 1

    @property
    def name(self) -> str:
        return self.__name

    def __update_transformation_matrix(self):
        self.__transformation_matrix = Matrix3x3()
        self.__transformation_matrix.scale(self.__scale)
        self.__transformation_matrix.rotate(self.__rotation)
        self.__transformation_matrix.translate(self.__position)

    @property
    def transformation(self) -> Matrix3x3:
        return self.__transformation_matrix

    @property
    def position(self) -> Vector2:
        return self.__position

    @property
    def rotation(self) -> float:
        return self.__rotation

    @property
    def scale(self) -> Vector2:
        return self.__scale

    @position.setter
    def position(self, pos: Vector2):
        self.__position = pos
        self.__update_transformation_matrix()

    @rotation.setter
    def rotation(self, rot: float):
        self.__rotation = rot
        self.__update_transformation_matrix()

    @scale.setter
    def scale(self, scale: Vector2):
        self.__scale = scale
        self.__update_transformation_matrix()

    @property
    def id(self):
        return self.__id

    def __eq__(self, other: "DrawableObject") -> bool:
        return self.id == other.id


class Point(DrawableObject):

    def __init__(self, pos: Vector2, name: str | None = None):
        super().__init__(name)
        self.__pos = pos

    @property
    def point(self) -> Vector2:
        return self.__pos * self.transformation


class Line(DrawableObject):

    def __init__(self, start: Vector2, end: Vector2, name: str | None = None):
        super().__init__(name)
        self.__start: Vector2 = start
        self.__end: Vector2 = end

    @property
    def start(self) -> Vector2:
        return self.__start * self.transformation

    @property
    def end(self):
        return self.__end * self.transformation


class Wireframe(DrawableObject):

    def __init__(self, points: list[Vector2], name: str | None = None):
        super().__init__(name)
        if len(points) < 3:
            raise RuntimeError('A polygon must have at least 3 points')
        self.__points: list[Vector2] = deepcopy(points)

    @property
    def points(self) -> List[Vector2]:
        transformed_points: List[Vector2] = []
        for p in self.__points:
            transformed_points.append(p * self.transformation)
        return transformed_points


class ObjectRenderer:

    def __init__(self, window: Window, evt_sys: EventSystem):
        self.__objects: list[DrawableObject] = []
        self.__window = window
        self.__batch = pyglet.graphics.Batch()
        self.__evt_sys = evt_sys
        self.__evt_sys.register_callback(
            Event.REMOVE_DRAWALBE, self.removeObject)
        self.__evt_sys.register_callback(
            Event.ADD_DRAWABLE, self.addObject
        )

    def hasObject(self, object: DrawableObject):
        return object in self.__objects

    def removeObject(self, object: DrawableObject):
        if self.hasObject(object):
            self.__objects.remove(object)
            self.__evt_sys.fire(Event.DRAWABLE_REMOVED, object)

    def addObject(self, object: DrawableObject):
        if self.hasObject(object):
            return
        self.__objects.append(object)
        self.__evt_sys.fire(Event.DRAWABLE_ADDED, object)

    def __create_polygon_lines(self, polygon: Wireframe) -> list[pyglet.shapes.ShapeBase]:
        points = polygon.points
        points_len = len(points)
        lines = []
        for i in range(1, points_len):
            pi = self.__window.world_to_viewport(points[i])
            pj = self.__window.world_to_viewport(points[i-1])
            l = pyglet.shapes.Line(pj.x, pj.y, pi.x, pi.y, batch=self.__batch)
            lines.append(l)
        plast = self.__window.world_to_viewport(points[points_len-1])
        pstart = self.__window.world_to_viewport(points[0])
        l = pyglet.shapes.Line(plast.x, plast.y, pstart.x,
                               pstart.y, batch=self.__batch)
        lines.append(l)
        return lines

    def draw(self):
        shapes: list[pyglet.shapes.ShapeBase] = list()
        for drawable in self.__objects:
            if isinstance(drawable, Line):
                lsvp = self.__window.world_to_viewport(drawable.start)
                levp = self.__window.world_to_viewport(drawable.end)
                shapes.append(pyglet.shapes.Line(
                    lsvp.x, lsvp.y, levp.x, levp.y, batch=self.__batch))
            elif isinstance(drawable, Wireframe):
                lines = self.__create_polygon_lines(drawable)
                shapes.extend(lines)
            elif isinstance(drawable, Point):
                point = self.__window.world_to_viewport(drawable.point)
                shapes.append(pyglet.shapes.Circle(
                    point.x, point.y, 2, batch=self.__batch))
        self.__batch.draw()
