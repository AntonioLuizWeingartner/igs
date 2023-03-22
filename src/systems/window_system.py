from system import System
from peripheral_manager import PeripheralManager
from event_system import EventSystem, Event
from window import Window
from igs_math import Vector2
from functools import partial
import pyglet.window.key as key


class WindowSystem(System):

    def __init__(self, key_manager: PeripheralManager, mouse_manager: PeripheralManager,
                 evt_system: EventSystem, window: Window):
        super().__init__(key_manager, mouse_manager, evt_system)
        self.__window = window
        self.__direction: Vector2 = Vector2(0, 0)
        self.__multiply_factor: float = 0.0
        self.key_manager.register_callback(
            partial(self.add_to_dir, Vector2(-1, 0)), key.A, 0, True)
        self.key_manager.register_callback(partial(
            self.add_to_dir, Vector2(1, 0)), key.A, 0, False)
        self.key_manager.register_callback(
            partial(self.add_to_dir, Vector2(1, 0)), key.D, 0, True)
        self.key_manager.register_callback(
            partial(self.add_to_dir, Vector2(-1, 0)), key.D, 0, False)
        self.key_manager.register_callback(
            partial(self.add_to_dir, Vector2(0, 1)), key.W, 0, True)
        self.key_manager.register_callback(
            partial(self.add_to_dir, Vector2(0, -1)), key.W, 0, False)
        self.key_manager.register_callback(
            partial(self.add_to_dir, Vector2(0, -1)), key.S, 0, True)
        self.key_manager.register_callback(
            partial(self.add_to_dir, Vector2(0, 1)), key.S, 0, False)
        self.key_manager.register_callback(
            partial(self.set_mul_factor, 1.0), key.NUM_SUBTRACT, 0, True
        )
        self.key_manager.register_callback(
            partial(self.set_mul_factor, 0.0), key.NUM_SUBTRACT, 0, False
        )
        self.key_manager.register_callback(
            partial(self.set_mul_factor, -1.0), key.NUM_ADD, 0, True
        )
        self.key_manager.register_callback(
            partial(self.set_mul_factor, 0.0), key.NUM_ADD, 0, False
        )
        self.evt_system.register_callback(
            Event.MOVE_WINDOW, self.__window.move)
        self.evt_system.register_callback(
            Event.ZOOM_WINDOW, self.__window.zoom
        )

    def add_to_dir(self, dir: Vector2):
        self.__direction += dir*10.0

    def set_mul_factor(self, factor: float):
        self.__multiply_factor = factor

    def update(self):
        self.__window.move(self.__direction)
        self.__window.zoom(Vector2(-10, -10)*self.__multiply_factor)
