from constants import *


class Rainbow:
    pixelmapper = None
    pixelcontroller = None
    tick_ms = None
    length = None

    def __init__(self, pixelmapper, pixelcontroller, tick_ms=100, length=None):
        self.pixelmapper = pixelmapper
        self.pixelcontroller = pixelcontroller
        self.tick_ms = tick_ms
        self.length = length if length else pixelmapper.total_leds  # If a length isn't set, use the whole metastrand

    def start(self):
        self.pixelmapper.set_metastrand_leds(self.pixelmapper.get_rainbow(self.length))

        print("%s started" % __name__)

    def stop(self):
        self.pixelcontroller.set_color()

        print("%s stopped" % __name__)

    def input(self, event, axis, buttons):
        pass

    def tick(self):
        self.pixelmapper.set_metastrand_leds(self.pixelmapper.rotate(self.pixelmapper.get_metastrand_leds()))
        self.pixelcontroller.set_pixel_map(self.pixelmapper)
