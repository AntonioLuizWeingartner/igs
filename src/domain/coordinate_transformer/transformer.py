from domain.graphics.viewport import Viewport
from domain.graphics.window import Window
from domain.math.matrix3x3 import Matrix3x3
from domain.math.vector2 import Vector2


class CoordinateTransformer:

    def __init__(self, viewport: Viewport, window: Window):
        self.__viewport = viewport
        self.__window = window

    def local_to_world(self, point: Vector2, model_matrix: Matrix3x3) -> Vector2:
        """
        Converts an arbitrary point in object local space to world space using its modelMatrix
        """
        return point * model_matrix

    def world_to_normalized_window(self) -> Matrix3x3:
        """
        Returns a matrix that converts an arbitray world space point into normalized window space
        """
        s = self.__window.max - self.__window.min
        s = Vector2(2.0/s.x, 2.0/s.y)
        window_center = (self.__window.max + self.__window.min) / 2.0
        transformation = Matrix3x3()
        transformation.translate(-window_center)
        transformation.rotate(self.__window.orientation)
        transformation.scale(s)
        return transformation

    def window_to_viewport(self) -> Matrix3x3:
        """
        Converts an arbitrary point in window normalized space to viewport space
        """
        viewport_half_size = (self.__viewport.max - self.__viewport.min)/2.0
        transformation = Matrix3x3()
        transformation.scale(
            Vector2(viewport_half_size.x, viewport_half_size.y))
        transformation.translate(viewport_half_size)
        return transformation

    def viewport_to_screen(self) -> Matrix3x3:
        """
        Converts an arbitrary point in viewport space to screen space
        """
        transformation = Matrix3x3()
        transformation.translate(self.__viewport.min)
        return transformation
