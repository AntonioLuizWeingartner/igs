from __future__ import annotations, division
import numpy as np


class Matrix3x3:
    """
    Nice interface to encapsulate a numpy matrix
    """

    def __init__(self):
        self.identity()

    def __repr__(self) -> str:
        return self.__np_mat.__repr__()

    def identity(self):
        self.__np_mat: np.ndarray = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def translate(self, offset: Vector2):
        trans_mat = np.array([[1, 0, 0], [0, 1, 0], [offset.x, offset.y, 1]])
        self.__np_mat = self.__np_mat @ trans_mat

    def rotate(self, angle: float):
        cos, sin = np.cos(angle), np.sin(angle)
        rot_mat = np.array([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])
        self.__np_mat = self.__np_mat @ rot_mat

    def scale(self, scale: Vector2):
        scale_mat = np.array([[scale.x, 0, 0], [0, scale.y, 0], [0, 0, 1]])
        self.__np_mat = self.__np_mat @ scale_mat

    def invert(self):
        self.__np_mat = np.linalg.inv(self.__np_mat)

    @property
    def np_mat(self) -> np.ndarray:
        return np.copy(self.__np_mat)


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


myVec = Vector2(1, 0)
myMat = Matrix3x3()
myMat.rotate(np.pi/4)
