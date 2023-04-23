from domain.event_system.event_system import EventSystem
from domain.math.vector2 import Vector2
from infrastructure.control_window.control_window import create_control_window
from infrastructure.main_window.main_window import MainWindow
import pyglet
import multiprocessing
import functools


class Application:

    def __init__(self, main_window: MainWindow):
        self.__main_window = main_window
        self.__control_window_conn, self.__app_conn = multiprocessing.Pipe()

    def __create_control_window(self):
        loc = self.__main_window.get_location()
        self.__control_window_process = multiprocessing.Process(
            target=functools.partial(create_control_window, self.__control_window_conn, Vector2(loc[0], loc[1])))
        self.__control_window_process.start()

    def run(self):
        self.__main_window.set_visible(True)
        self.__create_control_window()
        pyglet.app.run()
        self.__control_window_process.kill()
