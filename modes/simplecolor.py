from constants import *


class SimpleColor:
    pixelmapper = None
    pixelcontroller = None
    tick_ms = None
    axis_state = None
    pressed_buttons = None

    def __init__(self, pixelmapper, pixelcontroller, tick_ms=100):
        self.pixelmapper = pixelmapper
        self.pixelcontroller = pixelcontroller
        self.tick_ms = tick_ms

    def start(self):
        print("%s started" % __name__)

        # If the base color is currently off, give it an initial value
        if sum(self.pixelmapper.base_color) == 0:
            self.pixelmapper.base_color = (96, 0, 0)

        for s in self.pixelmapper.strands:
            s.leds = [self.pixelmapper.base_color] * s.length
        self.pixelcontroller.set_pixel_map(self.pixelmapper)

    def stop(self):
        for s in self.pixelmapper.strands:
            s.leds = [COLOR_BLANK] * s.length
        self.pixelcontroller.set_pixel_map(self.pixelmapper)

        print("%s stopped" % __name__)
        pass

    def input(self, event, axis, buttons):
        pass

    def tick(self):
        if self.pixelmapper.base_color_changed:
            self.refresh_color()

    def refresh_color(self):
        for s in self.pixelmapper.strands:
            s.leds = [self.pixelmapper.base_color] * s.length

        self.pixelcontroller.set_pixel_map(self.pixelmapper)
        self.pixelmapper.base_color_changed = False
