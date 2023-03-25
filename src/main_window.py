import multiprocessing.connection
import pyglet
import numpy as np
from drawable import Line, ObjectRenderer
from igs_math import Vector2
from viewport import Viewport
from window import Window
from peripheral_manager import PeripheralManager
from event_system import EventSystem, Event
from system import SystemManager
from typing import Any


class MainWindow(pyglet.window.Window):

    def __init__(self, width: int, height: int, keyboard_manager: PeripheralManager, mouse_manager: PeripheralManager,
                 event_system: EventSystem, viewport: Viewport, window: Window,
                 sys_manager: SystemManager,
                 object_renderer: ObjectRenderer, conn: multiprocessing.connection.Connection):
        super().__init__(width, height)
        self.__viewport: Viewport = viewport
        self.__window: Window = window
        self.__keyboard_manager: PeripheralManager = keyboard_manager
        self.__mouse_manager: PeripheralManager = mouse_manager
        self.__event_system: EventSystem = event_system
        self.__wireframe_renderer: ObjectRenderer = object_renderer
        self.__sys_manager: SystemManager = sys_manager
        self.__conn: multiprocessing.connection.Connection = conn
        self.__event_system.register_callback(
            Event.DRAWABLE_ADDED, lambda drawable: self.__conn.send((Event.DRAWABLE_ADDED, drawable)))
        self.__event_system.register_callback(
            Event.DRAWABLE_REMOVED, lambda drawable: self.__conn.send(
                (Event.DRAWABLE_REMOVED, drawable))
        )

    def on_draw(self):
        self.clear()

        if self.__conn.poll():
            message: tuple[Event, Any] = self.__conn.recv()
            self.__event_system.fire(message[0], message[1])

        self.__sys_manager.update()
        self.__wireframe_renderer.draw()

    def on_key_press(self, key: int, modifiers: int):
        self.__keyboard_manager.fire(key, modifiers, True)

    def on_key_release(self, key: int, modifiers: int):
        self.__keyboard_manager.fire(key, modifiers, False)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.__mouse_manager.fire(button, modifiers, True, Vector2(x, y))

    def on_mouse_release(self, x, y, button, modifiers):
        self.__mouse_manager.fire(button, modifiers, False, Vector2(x, y))

    def on_mouse_motion(self, x, y, dx, dy):
        self.__event_system.fire(
            Event.MOUSE_MOVE, Vector2(x, y), Vector2(dx, dy))
