from __future__ import annotations, division
import numpy as np
from domain.math.matrix3x3 import Matrix3x3
from typing import List


class Vector2:

    """
    This class encapsulates a numpy matrix to provide a nice interface for creating points and transforming them
    """

    def __init__(self, x: float, y: float):
        self.__np_vec: np.ndarray = np.array([[x, y, 1.0]])

    @property
    def x(self) -> float:
        return self.__np_vec[0, 0]

    @property
    def y(self) -> float:
        return self.__np_vec[0][1]

    @x.setter
    def x(self, value: float):
        self.__np_vec[0, 0] = value

    @y.setter
    def y(self, value: float):
        self.__np_vec[0, 1] = value

    def __repr__(self) -> str:
        return self.__np_vec.__repr__()

    def __add__(self, other: Vector2) -> Vector2:
        return Vector2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Vector2) -> Vector2:
        self.__np_vec += np.array([[other.x, other.y, 0.0]])
        return self

    def __sub__(self, other: Vector2) -> Vector2:
        return Vector2(self.x - other.x, self.y - other.y)

    def __isub__(self, other: Vector2) -> Vector2:
        self.__np_vec -= np.array([[other.x, other.y, 0.0]])
        return self

    @property
    def np_vec(self):
        return self.__np_vec

    def __mul__(self, other: Matrix3x3 | float) -> Vector2:
        if isinstance(other, Matrix3x3):
            result = self.__np_vec @ other.np_mat
        elif isinstance(other, float):
            result = self.__np_vec * other
        return Vector2(result[0, 0], result[0, 1])

    def __imul__(self, other: Matrix3x3 | float):
        if isinstance(other, Matrix3x3):
            self.__np_vec = self.__np_vec @ other.np_mat
        elif isinstance(other, float):
            self.__np_vec *= other
        return self

    def __truediv__(self, other: float) -> Vector2:
        return Vector2(self.x/other, self.y/other)

    def __neg__(self) -> Vector2:
        return Vector2(-self.x, -self.y)

    @classmethod
    def average(cls, vectors: List[Vector2]) -> Vector2:
        avg_x = np.mean(np.array(list((map(lambda vec: vec.x, vectors)))))
        avg_y = np.mean(np.array(list((map(lambda vec: vec.y, vectors)))))
        return Vector2(float(avg_x), float(avg_y))


        
        
