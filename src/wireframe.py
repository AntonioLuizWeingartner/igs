import pyglet
import uuid
import numpy as np
from igs_math import Vector2, Matrix3x3
from window import Window
from typing import List
from copy import deepcopy


class Wireframe:

    def __init__(self):
        self.__position = Vector2(0, 0)
        self.__rotation = 0.0
        self.__scale = Vector2(1, 1)
        self.__update_transformation_matrix()
        self.__id = uuid.uuid4()

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

    def __eq__(self, other: "Wireframe") -> bool:
        return self.id == other.id


class Line(Wireframe):

    def __init__(self, start: Vector2, end: Vector2):
        super().__init__()
        self.__start: Vector2 = start
        self.__end: Vector2 = end

    @property
    def start(self) -> Vector2:
        return self.__start * self.transformation

    @property
    def end(self):
        return self.__end * self.transformation


class Polygon(Wireframe):

    def __init__(self, points: list[Vector2]):
        super().__init__()
        if len(points) < 3:
            raise RuntimeError('A polygon must have at least 3 points')
        self.__points: list[Vector2] = deepcopy(points)

    @property
    def points(self) -> List[Vector2]:
        transformed_points: List[Vector2] = []
        for p in self.__points:
            transformed_points.append(p * self.transformation)
        return transformed_points


class WireframeRenderer:

    def __init__(self, window: Window):
        self.__objects: list[Wireframe] = []
        self.__window = window
        self.__batch = pyglet.graphics.Batch()

    def hasObject(self, object: Wireframe):
        return object in self.__objects

    def removeWireframe(self, object: Wireframe):
        if self.hasObject(object):
            self.__objects.remove(object)

    def addWireframe(self, object: Wireframe):
        if self.hasObject(object):
            return
        self.__objects.append(object)

    def __create_polygon_lines(self, polygon: Polygon) -> list[pyglet.shapes.ShapeBase]:
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
        for wireframe in self.__objects:
            if isinstance(wireframe, Line):
                lsvp = self.__window.world_to_viewport(wireframe.start)
                levp = self.__window.world_to_viewport(wireframe.end)
                shapes.append(pyglet.shapes.Line(
                    lsvp.x, lsvp.y, levp.x, levp.y, batch=self.__batch))
            elif isinstance(wireframe, Polygon):
                lines = self.__create_polygon_lines(wireframe)
                shapes.extend(lines)
        self.__batch.draw()
