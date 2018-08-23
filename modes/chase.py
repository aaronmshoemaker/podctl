
class Chase:
    pixelmapper = None
    pixelcontroller = None
    tick_ms = None
    axis_state = None
    pressed_buttons = None
    switch_direction = False

    def __init__(self, pixelmapper, pixelcontroller, tick_ms=100):
        self.pixelmapper = pixelmapper
        self.pixelcontroller = pixelcontroller
        self.tick_ms = tick_ms

    def start(self):
        pass

        print("%s started" % __name__)

    def stop(self):
        self.pixelcontroller.set_color()
        print("%s stopped" % __name__)

    def input(self, event, axis, buttons):
        if axis[0] != 0:
            self.switch_direction = axis[0] == 1

    def tick(self):
        rotate_step = -1 if self.switch_direction else 1

        for s in self.pixelmapper.strands:
            trail_len = int(s.length)
            chase_head = 0 if "chase_head" not in s.attributes else int(s.attributes["chase_head"])
            s.set_solid_color()
            s.leds[0:trail_len] = self.pixelmapper.get_trail(trail_len, self.pixelmapper.base_color,
                                                             invert=self.switch_direction)
            s.leds = self.pixelmapper.rotate(s.leds, chase_head)

            s.attributes["chase_head"] = (chase_head + rotate_step) % s.length

        self.pixelcontroller.set_pixel_map(self.pixelmapper)
