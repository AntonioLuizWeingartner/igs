from domain.coordinate_transformer.transformer import CoordinateTransformer
from domain.event_system.event_system import EventSystem
from domain.graphics.viewport import Viewport
from domain.graphics.window import Window
from domain.math.vector2 import Vector2
from domain.primitive_components.line import LineComponent
from domain.primitive_components.window_controller import WindowController
from domain.world_object.manager import WorldObjectManager
from infrastructure.application.app import Application
from infrastructure.main_window.main_window import MainWindow
from infrastructure.obj_loader.obj_loader import WaveFrontParser
from infrastructure.renderer.line_renderer import LineRenderer


def setup(object_manager: WorldObjectManager):
    managerObj = object_manager.create()
    managerObj.add_component(WindowController)


if __name__ == '__main__':
    evt_sys = EventSystem()
    viewport = Viewport(Vector2(0, 0), Vector2(800, 600))
    window = Window(Vector2(-50.0, -50.0), Vector2(50.0, 50.0), 0.0)
    object_manager = WorldObjectManager(evt_sys, window)
    setup(object_manager)
    coord_transformer = CoordinateTransformer(viewport, window)
    line_renderer = LineRenderer(object_manager, coord_transformer)
    main_window = MainWindow(800, 600, evt_sys, line_renderer, object_manager)
    app = Application(main_window)
    parser = WaveFrontParser(object_manager)
    parser.parse('models/square.obj')
    parser.build_object()
    app.run()


# a renderer has a object manager and a coordinate transformer
# every frame it and gathers all lines and builds the scene
