from typing import List
from domain.math.vector2 import Vector2


class Polygon:

    def __init__(self, points: List[Vector2]):
        self.points = points
