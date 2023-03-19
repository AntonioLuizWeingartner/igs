from system import System
from peripheral_manager import PeripheralManager
from event_system import EventSystem
from window import Window
from igs_math import Vector2
from functools import partial
import pyglet.window.key as key


class ViewportSystem(System):

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

    def add_to_dir(self, dir: Vector2):
        self.__direction += dir

    def set_mul_factor(self, factor: float):
        self.__multiply_factor = factor

    def update(self):
        self.__window.w_max += self.__direction
        self.__window.w_min += self.__direction
        self.__window.w_max += Vector2(10, 10)*self.__multiply_factor
        self.__window.w_min += Vector2(-10, -10)*self.__multiply_factor
