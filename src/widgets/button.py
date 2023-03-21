import pyglet

from pyglet.gl import *
from widgets.control import Control


def draw_rect(x, y, width, height, color=(1, 1, 1, 1)):
    pyglet.graphics.draw(
        4,
        GL_LINE_LOOP,
        position=('f', (x, y, 0,
                        x + width, y, 0,
                        x + width, y + height, 0,
                        x, y + height, 0,
                        )
                  ),
        colors=('f', color * 4)
    )

class Button(Control):
    charged = False

    def draw(self):
        if self.charged:
            draw_rect(self.x, self.y, self.width, self.height)
        else:
            draw_rect(self.x, self.y, self.width, self.height, color=(1, 0, 0, 1))
        self.draw_label()

    def on_mouse_press(self, x, y, button, modifiers):
        self.capture_events()
        self.charged = True

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.charged = self.hit_test(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        self.release_events()
        if self.hit_test(x, y):
            self.dispatch_event('on_press')
        self.charged = False

Button.register_event_type('on_press')