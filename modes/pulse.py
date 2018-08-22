import random


class Pulse:
    pixelmapper = None
    pixelcontroller = None
    tick_ms = None
    axis_state = None
    pressed_buttons = None
    cycle_steps = 10
    step_count = 0
    current_color = (0, 0, 0)
    step_color_offset = None

    def __init__(self, pixelmapper, pixelcontroller, tick_ms=100):
        self.pixelmapper = pixelmapper
        self.pixelcontroller = pixelcontroller
        self.tick_ms = tick_ms

    def start(self):
        self.set_random_color_target()
        print("%s started" % __name__)

    def stop(self):
        self.pixelcontroller.set_color(0, 0, 0)
        print("%s stopped" % __name__)

    def input(self, event, axis, buttons):
        pass

    def tick(self):
        self.current_color = self.pixelmapper.shift_color_offset(self.current_color, self.step_color_offset)
        self.step_count = (self.step_count + 1) % self.cycle_steps
        self.pixelcontroller.set_color(*self.current_color)

        if self.step_count == 0:
            # Choose a new target color
            self.set_random_color_target()

    def set_random_color_target(self):
        self.pixelmapper.base_color = self.pixelmapper.get_random_color()
        self.recalculate_offsets()

    def recalculate_offsets(self):
        self.step_color_offset = (
            int((self.pixelmapper.base_color[0] - self.current_color[0]) / self.cycle_steps),
            int((self.pixelmapper.base_color[1] - self.current_color[1]) / self.cycle_steps),
            int((self.pixelmapper.base_color[2] - self.current_color[2]) / self.cycle_steps)
        )
