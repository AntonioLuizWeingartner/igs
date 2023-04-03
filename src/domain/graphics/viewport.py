from domain.math.matrix3x3 import Matrix3x3
from domain.math.vector2 import Vector2


class Viewport:

    def __init__(self, min: Vector2, max: Vector2):
        self.__min = min
        self.__max = max

    @property
    def min(self) -> Vector2:
        return self.__min

    @property
    def max(self) -> Vector2:
        return self.__max
