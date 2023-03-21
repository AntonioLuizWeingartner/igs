import pyglet

from widgets.button import Button


class TextButton(Button):
    def __init__(self, label, width, y, x, height, on_press, *args, **kwargs):
        super(TextButton, self).__init__(*args, **kwargs)
        self._text = pyglet.text.Label('', anchor_x='center', anchor_y='center', color=(0,0,0,255))
        self.set_text(label)
        self.width = width
        self.y = y
        self.x = x
        self.height = height
        self.on_press = on_press

    def draw_label(self):
        self._text.x = self.x + self.width / 2
        self._text.y = self.y + self.height / 2
        self._text.draw()

    def set_text(self, text):
        self._text.text = text

    text = property(lambda self: self._text.text,
                    set_text)