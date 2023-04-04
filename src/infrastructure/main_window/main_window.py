import pyglet
from domain.event_system.event_system import EventSystem


class MainWindow(pyglet.window.Window):

    def __init__(self, width: int, height: int, event_system: EventSystem):
        super().__init__(width, height)
        self.__event_sysyem = event_system

    # def on_draw(self, dt):
    #     pass

    # def on_key_press(self, symbol, modifiers):
    #     pass

    # def on_key_release(self, symbol, modifiers):
    #     pass

    # def on_mouse_motion(self, x, y, dx, dy):
    #     pass

    # def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
    #     pass

    # def on_mouse_press(self, x, y, button, modifiers):
    #     pass

    # def on_mouse_release(self, x, y, button, modifiers):
    #     pass
