import pygame
from constants import *


class Chase:
    pixelmapper = None
    pixelcontroller = None
    axis_state = None
    pressed_buttons = None
    head_index = 0
    switch_direction = False

    def __init__(self, pixelmapper, pixelcontroller):
        self.pixelmapper = pixelmapper
        self.pixelcontroller = pixelcontroller

    def start(self):
        for s in self.pixelmapper.strands:
            self.initialize_trail(s)

        print("%s started" % __name__)

    def stop(self):
        self.pixelcontroller.set_color(0, 0, 0)
        print("%s stopped" % __name__)

    def input(self, event, axis, buttons):
        if axis[0] != 0:
            self.switch_direction = axis[0] == 1

            for s in self.pixelmapper.strands:
                self.initialize_trail(s)

    def tick(self):
        if self.pixelmapper.base_color_changed:

            for s in self.pixelmapper.strands:
                self.initialize_trail(s)

            self.pixelmapper.base_color_changed = False
        else:
            rotate_step = -1 if self.switch_direction else 1

            for s in self.pixelmapper.strands:
                s.leds = self.rotate(s.leds, rotate_step)
                chase_head = 0 if "chase_head" not in s.attributes else int(s.attributes["chase_head"])
                s.attributes["chase_head"] = (chase_head + rotate_step) % s.length

        self.pixelcontroller.set_pixel_map(self.pixelmapper)

    def initialize_trail(self, s):
        color = self.pixelmapper.base_color
        trail = int(s.length / 2)
        trail_pixels = []

        start = 0 if self.switch_direction else trail
        end = trail if self.switch_direction else 0
        step = 1 if self.switch_direction else -1

        # Blank the strand
        s.set_solid_color()
        for i in range(start, end, step):
            trail_pixels.append((color[0] - i * 10, color[1] - i * 10, color[2] - i * 10))

        s.leds[0:trail] = trail_pixels

        if "chase_head" in s.attributes:
            s.leds = self.rotate(s.leds, int(s.attributes["chase_head"]))

    @staticmethod
    def rotate(l, n):
        return l[-n:] + l[:-n]
