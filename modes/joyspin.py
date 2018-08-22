class Joyspin:
    pixelmapper = None
    pixelcontroller = None
    axis_state = None
    pressed_buttons = None

    def __init__(self, pixelmapper, pixelcontroller):
        self.pixelmapper = pixelmapper
        self.pixelcontroller = pixelcontroller

    def start(self):
        for s in self.pixelmapper.strands:
            color = self.pixelmapper.base_color
            trail = int(s.length / 2)
            trail_pixels = []
            for i in range(0, trail):
                trail_pixels.append((color[0] - i * 10, color[1] - i * 10, color[2] - i * 10))

            s.set_solid_color()
            s.set_range(trail_pixels)

        print("%s started" % __name__)

    def stop(self):
        self.pixelcontroller.set_color(0, 0, 0)
        print("%s stopped" % __name__)

    def input(self, event, axis, buttons):
        self.axis_state = axis
        self.pressed_buttons = buttons

        self.tick()

    def tick(self):
        if self.axis_state and self.axis_state[0] != 0:
            for s in self.pixelmapper.strands:
                s.leds = self.rotate(s.leds, self.axis_state[0])

            self.pixelcontroller.set_pixel_map(self.pixelmapper)

    @staticmethod
    def rotate(l, n):
        return l[-n:] + l[:-n]
