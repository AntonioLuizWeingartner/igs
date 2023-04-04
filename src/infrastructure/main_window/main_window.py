import pyglet
from domain.event_system.event_system import Event, EventSystem
from domain.math.vector2 import Vector2
from domain.world_object.manager import WorldObjectManager
from infrastructure.renderer.line_renderer import LineRenderer


class MainWindow(pyglet.window.Window):

    def __init__(self, width: int, height: int, event_system: EventSystem, line_renderer: LineRenderer, object_manager: WorldObjectManager):
        super().__init__(width=width, height=height)
        self.__event_sysyem = event_system
        self.__line_renderer = line_renderer
        self.__object_manager = object_manager

    def on_draw(self):
        self.clear()
        self.__line_renderer.draw()
        self.__object_manager.update()

    def on_key_press(self, symbol, modifiers):
        self.__event_sysyem.fire(Event.KEY_PRESS, symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.__event_sysyem.fire(Event.KEY_RELEASE, symbol, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.__event_sysyem.fire(
            Event.MOUSE_MOVE, Vector2(x, y), Vector2(dx, dy))

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.__event_sysyem.fire(Event.MOUSE_SCROLL, Vector2(
            x, y), Vector2(scroll_x, scroll_y))

    def on_mouse_press(self, x, y, button, modifiers):
        self.__event_sysyem.fire(
            Event.MOUSE_PRESS, Vector2(x, y), button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.__event_sysyem.fire(
            Event.MOUSE_RELEASE, Vector2(x, y), button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.__event_sysyem.fire(Event.MOUSE_DRAG, Vector2(
            x, y), Vector2(dx, dy), buttons, modifiers)
