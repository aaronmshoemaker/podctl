class PixelMapper:
    strands = None
    total_leds = 0
    max_brightness = 128    # Max is 256. Artificially cap brightness to limit amperage draw. Todo: automatically set based on available power supply.
    base_color = (0, 0, 0)
    base_color_changed = False

    def __init__(self, strands):
        self.strands = sorted(strands, key=lambda x: x.start_index, reverse=False)
        self.validate()
        self.total_leds = self.strands[-1].start_index + self.strands[-1].length

    def validate(self):
        led_count = 0

        for s in self.strands:
            if s.start_index < led_count:
                raise ValueError('Strand starting at %s overlaps with another strand' % s.start_index)

            led_count = s.start_index + s.length - 1

    def change_base_color(self, r=0, g=0, b=0):
        self.base_color = (
            (self.base_color[0] + r) % self.max_brightness,
            (self.base_color[1] + g) % self.max_brightness,
            (self.base_color[2] + b) % self.max_brightness
        )

        self.base_color_changed = True

    def get_map(self):
        pixel_map = [(0, 0, 0)] * self.total_leds

        for s in self.strands:
            pixel_map[s.start_index:s.end_index] = s.leds

        return pixel_map


class Strand:
    start_index = 0
    length = 64
    end_index = length
    leds = []
    attributes = dict()

    def __init__(self, start_index, length):
        self.start_index = start_index
        self.length = length
        self.end_index = start_index + length
        self.leds = None

        self.set_solid_color()

    def set_solid_color(self, r=0, g=0, b=0):
        self.leds = [(r, g, b)] * self.length
