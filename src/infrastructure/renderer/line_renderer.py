from domain.world_object.manager import WorldObjectManager
from domain.coordinate_transformer.transformer import CoordinateTransformer
from domain.shapes.line import Line
from typing import List
from pyglet.graphics import Batch
import pyglet.shapes


class LineRenderer:

    def __init__(self, object_manager: WorldObjectManager, coordinate_transformer: CoordinateTransformer):
        self.__object_manager = object_manager
        self.__batch: Batch = Batch()
        self.__current_frame_lines: List[pyglet.shapes.Line] = list()
        self.__coord_transformer = coordinate_transformer

    def draw(self):
        """
        Renders all world lines into the screen, clipping can be performed here later
        """
        self.__current_frame_lines.clear()
        for line in self.__object_manager.draw():
            world_to_screen = self.__coord_transformer.world_to_screen()
            ls_screen = line.start * world_to_screen
            le_screen = line.end * world_to_screen
            self.__current_frame_lines.append(pyglet.shapes.Line(
                ls_screen.x, ls_screen.y, le_screen.x, le_screen.y, batch=self.__batch))
        self.__batch.draw()
