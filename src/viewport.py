from igs_math import Vector2


class Viewport:
    def __init__(self, vp_min: Vector2, vp_max: Vector2) -> None:
        self.vp_min = vp_min
        self.vp_max = vp_max
