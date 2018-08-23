from constants import *


class SimpleColor:
    pixelmapper = None
    pixelcontroller = None
    tick_ms = None

    def __init__(self, pixelmapper, pixelcontroller, tick_ms=100):
        self.pixelmapper = pixelmapper
        self.pixelcontroller = pixelcontroller
        self.tick_ms = tick_ms

    def start(self):
        print("%s started" % __name__)

        # If the base color is currently off, give it an initial value
        if sum(self.pixelmapper.base_color) == 0:
            self.pixelmapper.base_color = self.pixelmapper.get_random_color(min_brightness=32)

    def stop(self):
        self.pixelcontroller.set_color()

        print("%s stopped" % __name__)

    def input(self, event, axis, buttons):
        pass

    def tick(self):
        self.pixelcontroller.set_color(self.pixelmapper.base_color)
