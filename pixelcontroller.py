import lighting.opc
import time
from pixelmapper import PixelMapper
from constants import *


class PixelController(object):
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

    def set_color(self, color=COLOR_BLANK, channel_count=1):
        for i in range(channel_count):
            self.fadecandy.put_pixels(PixelMapper.get_pixels_solid(color), channel=i)

    def set_color_alternating(self, color_1, color_2=COLOR_BLANK, even=False, channel_count=1):
        for i in range(channel_count):
            self.fadecandy.put_pixels(PixelMapper.get_pixels_alternating(color_1, color_2, even=even), channel=i)
