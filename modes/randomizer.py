from constants import *
from datetime import datetime, timedelta
import random
import inspect
from modes.chase import Chase
from modes.pulse import Pulse
from modes.rainbow import Rainbow

class Randomizer:
    pixelmapper = None
    pixelcontroller = None
    tick_ms = None
    active_mode = None
    seconds_per_mode = None
    change_mode_dt = None

    def __init__(self, pixelmapper, pixelcontroller, tick_ms=100, seconds_per_mode=10):
        self.pixelmapper = pixelmapper
        self.pixelcontroller = pixelcontroller
        self.tick_ms = tick_ms
        self.seconds_per_mode = seconds_per_mode

    def start(self):
        self.set_random_mode()

        print("%s started" % __name__)

    def stop(self):
        self.pixelcontroller.set_color()

        print("%s stopped" % __name__)

    def input(self, event, axis, buttons):
        pass

    def tick(self):
        if self.change_mode_dt and datetime.now() >= self.change_mode_dt:
            self.set_random_mode()

        # if isinstance(self.active_mode, Chase):

        if self.active_mode:
            self.active_mode.tick()

    def set_random_mode(self):
        if self.active_mode:
            self.active_mode.stop()

        mode_idx = random.randint(0, 3)

        if mode_idx == 0:
            self.pixelmapper.base_color = self.pixelmapper.get_random_color(min_brightness=64)
            self.active_mode = Chase(self.pixelmapper, self.pixelcontroller)
        elif mode_idx == 1:
            self.active_mode = Pulse(self.pixelmapper, self.pixelcontroller)
        elif mode_idx == 2:
            self.active_mode = Pulse(self.pixelmapper, self.pixelcontroller,
                                     explicit_color_sequence=self.pixelmapper.get_rainbow(5))
        elif mode_idx == 3:
            self.active_mode = Rainbow(self.pixelmapper, self.pixelcontroller)

        self.change_mode_dt = datetime.now() + timedelta(seconds=self.seconds_per_mode)
        self.active_mode.start()
