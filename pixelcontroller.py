import lighting.opc
import time
from pixelmapper import PixelMapper
from constants import *

class PixelController:
    fadecandy = None

    def __init__(self):
        self.fadecandy = lighting.opc.Client('localhost:7890', True, False)

        # Set initial state for all controllers
        for i in range(0, 7):
            self.fadecandy.put_pixels([COLOR_BLANK] * 512, i)

    def set_pixel_map(self, pixelmapper, channel_count=1):
        for i in range(channel_count):
            pixels = pixelmapper.get_map()
            self.fadecandy.put_pixels(pixels, channel=i)

    def set_color(self, r=0, g=0, b=0, channel_count=1):
        for i in range(channel_count):
            self.fadecandy.put_pixels(PixelMapper.get_pixels_solid(r, g, b), channel=i)

    def set_color_alternating(self, even, r, g, b, channel_count=1):
        for i in range(channel_count):
            # print("Alternating channel %s, even=%s" % (i, even))
            self.fadecandy.put_pixels(PixelMapper.get_pixels_alternating(even, r, g, b), channel=i)

    def sparkle(self, r, g, b, delay, iterations):
        iterations *= 2  # A single 'sparkle' is an alternation between 2 states

        for i in range(iterations):
            self.set_color_alternating(i % 2 == 0, r, g, b)
            time.sleep(delay)

    def fade(self, start_r, start_g, start_b, end_r, end_g, end_b, cycleTime=1, steps=10):

        sleep_time = cycleTime / steps
        r_step = (end_r - start_r) / steps
        g_step = (end_g - start_g) / steps
        b_step = (end_b - start_b) / steps

        r = start_r
        g = start_g
        b = start_b

        for i in range(int(steps)):
            self.set_color(int(r), int(g), int(b))

            if i < steps:
                r += r_step
                b += b_step
                g += g_step
            else:
                r -= r_step
                b -= b_step
                g -= g_step

            time.sleep(sleep_time)

    def pulse(self, start_r, start_g, start_b, end_r, end_g, end_b, cycleTime=1, steps=10):
        self.fade(start_r, start_g, start_b, end_r, end_g, end_b, cycleTime / 2, steps / 2)
        self.fade(end_r, end_g, end_b, start_r, start_g, start_b, cycleTime / 2, steps / 2)
