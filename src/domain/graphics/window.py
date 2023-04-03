from domain.math.vector2 import Vector2


class Window:

    def __init__(self, min: Vector2, max: Vector2, orientation: float):
        self.__min = min
        self.__max = max
        self.__orientation = orientation

    @property
    def min(self) -> Vector2:
        return self.__min

    @property
    def max(self) -> Vector2:
        return self.__max

    @property
    def orientation(self) -> float:
        return self.__orientation

    def rotate(self, amount: float):
        self.__orientation = amount

    def translate(self, amount: Vector2):
        self.__min += amount
        self.__max += amount

    def zoom(self, amount: Vector2):
        self.__min += amount
        self.__max -= amount
