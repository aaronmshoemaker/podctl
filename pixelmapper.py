import random
from constants import *


class PixelMapper(object):
    strands = None
    max_led_index = 0
    total_leds = 0
    base_color = COLOR_BLANK
    base_color_changed = False

    def __init__(self, strands):
        self.strands = sorted(strands, key=lambda x: x.start_index, reverse=False)
        self.validate()
        self.max_led_index = self.strands[-1].start_index + self.strands[-1].length
        self.total_leds = sum(s.length for s in self.strands)

    def validate(self):
        led_count = 0

        for s in self.strands:
            if s.start_index < led_count:
                raise ValueError('Strand starting at %s overlaps with another strand' % s.start_index)

            led_count = s.start_index + s.length - 1

    def change_base_color(self, r=0, g=0, b=0):
        self.base_color = (
            (self.base_color[0] + r) % MAX_BRIGHTNESS,
            (self.base_color[1] + g) % MAX_BRIGHTNESS,
            (self.base_color[2] + b) % MAX_BRIGHTNESS
        )

        self.base_color_changed = True

    def get_map(self):
        pixel_map = [COLOR_BLANK] * self.max_led_index

        for s in self.strands:
            pixel_map[s.start_index:s.end_index] = s.leds

        return pixel_map

    def get_random_color(self):
        return (
            random.randint(0, MAX_BRIGHTNESS),
            random.randint(0, MAX_BRIGHTNESS),
            random.randint(0, MAX_BRIGHTNESS)
        )

    @staticmethod
    def get_pixels_solid(r=0, g=0, b=0, count=512):
        return [(r, g, b)] * count

    @staticmethod
    def get_pixels_alternating(even=True, r=0, g=0, b=0, count=512):
        if even:
            return [COLOR_BLANK, (r, g, b)] * int(count / 2)
        else:
            return [(r, g, b), COLOR_BLANK] * int(count / 2)

    @staticmethod
    def get_trail(length, head_color, tail_color=COLOR_BLANK, invert=False):
        trail_pixels = PixelMapper.get_color_sequence(head_color, tail_color, length)

        return trail_pixels if invert else trail_pixels[::-1]

    @staticmethod
    def shift_color(color, amount):
        return PixelMapper.bounded_value(color[0] + amount), PixelMapper.bounded_value(color[1] + amount),\
               PixelMapper.bounded_value(color[2] + amount)

    @staticmethod
    def shift_color_offset(color, color_offset):
        return PixelMapper.bounded_value(color[0] + color_offset[0]), PixelMapper.bounded_value(
            color[1] + color_offset[1]), PixelMapper.bounded_value(color[2] + color_offset[2])

    @staticmethod
    def bounded_value(val, minimum=0, maximum=MAX_BRIGHTNESS):
        return min(max(val, minimum), maximum)

    @staticmethod
    def get_color_sequence(color_1, color_2, steps):
        color_sequence = []
        step_color_offset = (
            int((color_2[0] - color_1[0]) / steps),
            int((color_2[1] - color_1[1]) / steps),
            int((color_2[2] - color_1[2]) / steps)
        )

        current_color = color_1

        for i in range(steps):
            current_color = PixelMapper.shift_color_offset(current_color, step_color_offset)
            color_sequence.append(current_color)

        return color_sequence


class Strand(object):
    start_index = 0
    length = 64
    end_index = length
    inverted = False
    attributes = dict()

    def __init__(self, start_index, length, inverted=False):
        self.__leds = []

        self.start_index = start_index
        self.length = length
        self.end_index = start_index + length
        self.inverted = inverted

        self.set_solid_color()

    @property
    def leds(self):
        return self.__leds[::-1] if self.inverted else self.__leds

    @leds.setter
    def leds(self, value):
        self.__leds = value

    @leds.deleter
    def leds(self):
        del self.__leds

    def set_solid_color(self, r=0, g=0, b=0):
        self.__leds = PixelMapper.get_pixels_solid(r, g, b, self.length)

    def set_range(self, pixels, index=0):
        self.__leds[index:len(pixels)] = pixels
        pass
