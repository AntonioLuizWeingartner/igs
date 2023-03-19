from viewport import Viewport
from igs_math import Vector2, Matrix3x3


class Window:

    def __init__(self, w_min: Vector2, w_max: Vector2, viewport):
        self.w_min = w_min
        self.w_max = w_max
        self.vp: Viewport = viewport

    def world_to_viewport(self, worldCoord: Vector2) -> Vector2:
        transformation = self.__build_viewport_matrix()
        return worldCoord * transformation

    def viewport_to_world(self, viewportCoord: Vector2) -> Vector2:
        transformation = self.__build_viewport_matrix()
        transformation.invert()
        return viewportCoord * transformation

    def __build_viewport_matrix(self) -> Matrix3x3:
        world_dim = self.w_max - self.w_min
        viewport_dim = self.vp.vp_max - self.vp.vp_min
        s = Vector2(viewport_dim.x / world_dim.x,
                    viewport_dim.y / world_dim.y)
        t = Vector2((self.vp.vp_min.x - self.w_min.x)
                    * s.x, (self.vp.vp_min.y - self.w_min.y) * s.y)
        transformation = Matrix3x3()
        transformation.scale(s)
        transformation.translate(t)
        return transformation
