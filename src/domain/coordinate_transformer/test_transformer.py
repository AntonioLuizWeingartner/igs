import unittest
from domain.coordinate_transformer.transformer import CoordinateTransformer
from domain.graphics.viewport import Viewport
from domain.graphics.window import Window
from domain.math.vector2 import Vector2
import math


class WorldToWindowNormalizedCoordinatesTransformationTest(unittest.TestCase):

    def setUp(self) -> None:
        self.window = Window(Vector2(-50, -50), Vector2(50, 50), 0.0)
        self.viewport = Viewport(Vector2(0, 0), Vector2(800, 600))
        self.transformer = CoordinateTransformer(self.viewport, self.window)

    def test_world_to_window_transformation(self):
        # should be Vector2(0,0, 0.0) in normalized coords
        window_bottom_left_world = self.window.min
        # should be Vector2(1.0, 1.0) in normalized coords
        window_top_right_world = self.window.max
        window_center_world = Vector2(0, 0)

        world_to_window_matrix = self.transformer.world_to_normalized_window()

        window_bottom_left_normalized = window_bottom_left_world * world_to_window_matrix
        window_top_right_normalized = window_top_right_world * world_to_window_matrix
        window_center_normalized = window_center_world * world_to_window_matrix
        # basic tests
        self.assertAlmostEqual(window_bottom_left_normalized.x, -1.0)
        self.assertAlmostEqual(window_bottom_left_normalized.y, -1.0)
        self.assertAlmostEqual(window_top_right_normalized.x, 1.0)
        self.assertAlmostEqual(window_top_right_normalized.y, 1.0)
        self.assertAlmostEqual(window_center_normalized.x, 0.0)
        self.assertAlmostEqual(window_center_normalized.y, 0.0)

        # testing rotation
        self.window.rotate(math.radians(45))

        world_to_window_matrix = self.transformer.world_to_normalized_window()

        window_top_right_world = Vector2(0, 70.7106781186)
        window_bottom_left_world = Vector2(0, -70.7106781186)

        window_top_right_normalized = window_top_right_world * world_to_window_matrix
        window_bottom_left_world = window_bottom_left_world * world_to_window_matrix
        window_center_normalized = window_center_world * world_to_window_matrix

        self.assertAlmostEqual(window_top_right_normalized.x, 1.0)
        self.assertAlmostEqual(window_top_right_normalized.y, 1.0)
        self.assertAlmostEqual(window_bottom_left_world.x, -1.0)
        self.assertAlmostEqual(window_bottom_left_world.y, -1.0)

        # testing translation
        self.window.translate(Vector2(50, 50))
        world_to_window_matrix = self.transformer.world_to_normalized_window()
        window_center_world = Vector2(50, 50)
        window_top_right_world = Vector2(50, 70.7106781186+50)
        window_bottom_left_world = Vector2(50, -70.7106781186+50)

        window_top_right_normalized = window_top_right_world * world_to_window_matrix
        window_bottom_left_world = window_bottom_left_world * world_to_window_matrix
        window_center_normalized = window_center_world * world_to_window_matrix

        self.assertAlmostEqual(window_top_right_normalized.x, 1.0)
        self.assertAlmostEqual(window_top_right_normalized.y, 1.0)
        self.assertAlmostEqual(window_bottom_left_world.x, -1.0)
        self.assertAlmostEqual(window_bottom_left_world.y, -1.0)

    def test_window_to_viewport_transformation(self):
        viewport_size = self.viewport.max - self.viewport.min
        window_top_right = Vector2(1.0, 1.0)
        window_to_viewport_matrix = self.transformer.window_to_viewport()
        viewport_top_right = window_top_right * window_to_viewport_matrix

        self.assertAlmostEqual(viewport_top_right.x, viewport_size.x)
        self.assertAlmostEqual(viewport_top_right.y, viewport_size.y)

    def test_viewport_to_screen_transformation(self):
        viewport_bottom_left = Vector2(0, 0)
        viewport_to_screen_matrix = self.transformer.viewport_to_screen()
        viewport_bottom_left_screen_coords = viewport_bottom_left * viewport_to_screen_matrix

        self.assertAlmostEqual(
            viewport_bottom_left_screen_coords.x, self.viewport.min.x)
        self.assertAlmostEqual(
            viewport_bottom_left_screen_coords.y, self.viewport.min.y)
