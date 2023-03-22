from functools import partial
import multiprocessing
import threading
import sys
import pyglet
from control_window import create_control_window
from main_window import MainWindow
from systems.object_spawner import ObjectSpawner
from viewport import Viewport
from window import Window
from peripheral_manager import PeripheralManager
from event_system import EventSystem
from igs_math import Vector2
from system import SystemManager
from systems.window_system import WindowSystem
from drawable import ObjectRenderer
from PyQt5.QtWidgets import QApplication

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

wireframe_renderer: ObjectRenderer = ObjectRenderer(window, event_system)

window_sys: WindowSystem = WindowSystem(
    keyboard_manager, mouse_manager, event_system, window)

wireframe_spawner: ObjectSpawner = ObjectSpawner(
    keyboard_manager, mouse_manager, event_system, wireframe_renderer, window)

sys_manager.add(window_sys)
sys_manager.add(wireframe_spawner)

control_window_conn, main_window_conn = multiprocessing.Pipe()

main_window: MainWindow = MainWindow(
    main_window_width, main_window_height, keyboard_manager, mouse_manager, event_system, viewport, window, sys_manager, wireframe_renderer, main_window_conn)

# control window needs to be a separate process because pyqt cant run in the same thread as pyglet
# annnd both pyqt and pyglet need to use the 'main' thread
control_window_process = multiprocessing.Process(
    target=partial(create_control_window, control_window_conn))

control_window_process.start()


pyglet.app.run()
control_window_process.kill()
