
from uuid import UUID
from domain.event_system.event_system import Event, EventSystem
from domain.graphics.window import Window
from domain.math.vector2 import Vector2
from domain.world_object.object import WorldObject, WorldObjectComponent


class WindowController(WorldObjectComponent):

    def __init__(self, owner: WorldObject, id: UUID, event_system: EventSystem, window: Window):
        super().__init__(owner, id, event_system, window)
        self.event_system.register_callback(
            Event.MOUSE_PRESS, self.__handle_mouse_press)
        self.event_system.register_callback(
            Event.MOUSE_RELEASE, self.__handle_mouse_release)
        self.event_system.register_callback(
            Event.KEY_PRESS, self.__handle_key_press)
        self.event_system.register_callback(
            Event.KEY_RELEASE, self.__handle_key_release)
        self.event_system.register_callback(
            Event.MOUSE_DRAG, self.__move_window
        )
        self.event_system.register_callback(
            Event.MOUSE_SCROLL, self.__zoom_window
        )
        self.__scroll_pressed = False
        self.__shift_pressed = False
        self.__rotate_window = False
        self.__rotate_amount = 0.0

    def __handle_mouse_press(self, pos, key, modifiers):
        if (key == 2):
            self.__scroll_pressed = True

    def __handle_mouse_release(self, pos, key, modifiers):
        if (key == 2):
            self.__scroll_pressed = False

    def __handle_key_press(self, key, modifiers):
        if (key == 65505):
            self.__shift_pressed = True
        elif (key == 65430 and modifiers == 1):
            self.__rotate_amount = 0.1
            self.__rotate_window = True
        elif (key == 65432 and modifiers == 1):
            self.__rotate_amount = -0.1
            self.__rotate_window = True

    def __handle_key_release(self, key, modifiers):
        if (key == 65505 or key == 65430 or key == 65432):
            self.__rotate_window = False
        if (key == 65505):
            self.__shift_pressed = False

    def __zoom_window(self, pos, delta):
        zoom = delta.y
        # zoom seems to be working fine with rotation
        self.window.zoom(Vector2(zoom, zoom))

    def __move_window(self, pos, delta, buttons, modifiers):
        if self.__scroll_pressed and self.__shift_pressed:
            # rotate delta to match windows orientation
            up_vec = self.window.up
            right_vec = self.window.right
            self.window.translate(Vector2(
                up_vec.x*delta.y, up_vec.y*delta.y)+Vector2(right_vec.x*delta.x, right_vec.y*delta.x))

    def update(self):
        if self.__rotate_window:
            self.window.rotate(self.__rotate_amount)
