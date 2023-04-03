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

    def translate(self, offset: "Vector2"):
        trans_mat = np.array([[1, 0, 0], [0, 1, 0], [offset.x, offset.y, 1]])
        self.__np_mat = self.__np_mat @ trans_mat

    def rotate(self, angle: float):
        cos, sin = np.cos(angle), np.sin(angle)
        rot_mat = np.array([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])
        self.__np_mat = self.__np_mat @ rot_mat

    def scale(self, scale: "Vector2"):
        scale_mat = np.array([[scale.x, 0, 0], [0, scale.y, 0], [0, 0, 1]])
        self.__np_mat = self.__np_mat @ scale_mat

    def invert(self):
        self.__np_mat = np.linalg.inv(self.__np_mat)

    @property
    def np_mat(self) -> np.ndarray:
        return np.copy(self.__np_mat)
