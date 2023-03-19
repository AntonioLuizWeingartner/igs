import pyglet
from main_window import MainWindow
from systems.wireframe_spawner import WireframeSpawner
from viewport import Viewport
from window import Window
from peripheral_manager import PeripheralManager
from event_system import EventSystem
from igs_math import Vector2
from system import SystemManager
from systems.viewport_system import ViewportSystem
from systems.line_spawner import LineSpawner
from wireframe import WireframeRenderer

main_window_width = 800
main_window_height = 600

viewport: Viewport = Viewport(Vector2(0, 0), Vector2(
    main_window_width, main_window_height))

window: Window = Window(Vector2(-main_window_width/2, -main_window_width/2),
                        Vector2(main_window_width/2, main_window_width/2), viewport)

keyboard_manager: PeripheralManager = PeripheralManager()
mouse_manager: PeripheralManager = PeripheralManager()

event_system: EventSystem = EventSystem()

sys_manager: SystemManager = SystemManager()

wireframe_renderer: WireframeRenderer = WireframeRenderer(window)

viewport_sys: ViewportSystem = ViewportSystem(
    keyboard_manager, mouse_manager, event_system, window)

# line_spawner: LineSpawner = LineSpawner(
#     keyboard_manager, mouse_manager, event_system, wireframe_renderer, Vector2(-10000, -10000), Vector2(10000, 10000), 100)

wireframe_spawner: WireframeSpawner = WireframeSpawner(
    keyboard_manager, mouse_manager, event_system, wireframe_renderer, window)

sys_manager.add(viewport_sys)
sys_manager.add(wireframe_spawner)

main_window: MainWindow = MainWindow(
    main_window_width, main_window_height, keyboard_manager, mouse_manager, event_system, viewport, window, sys_manager, wireframe_renderer)

pyglet.app.run()
