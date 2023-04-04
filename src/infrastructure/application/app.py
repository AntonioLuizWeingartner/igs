from domain.event_system.event_system import EventSystem
from infrastructure.main_window.main_window import MainWindow
import pyglet


class Application:

    def __init__(self, main_window: MainWindow):
        self.__main_window = main_window

    def run(self):
        self.__main_window.set_visible(True)
        pyglet.app.run()
