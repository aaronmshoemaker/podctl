from constants import *


class SimpleColor:
    pixelmapper = None
    pixelcontroller = None
    axis_state = None
    pressed_buttons = None

    def __init__(self, pixelmapper, pixelcontroller):
        self.pixelmapper = pixelmapper
        self.pixelcontroller = pixelcontroller

    def start(self):
        print("%s started" % __name__)

        # If the base color is currently off, give it an initial value
        if sum(self.pixelmapper.base_color) == 0:
            self.pixelmapper.base_color = (64, 0, 0)

        for s in self.pixelmapper.strands:
            s.leds = [self.pixelmapper.base_color] * s.length
        self.pixelcontroller.set_pixel_map(self.pixelmapper)

    def stop(self):
        for s in self.pixelmapper.strands:
            s.leds = [(0, 0, 0)] * s.length
        self.pixelcontroller.set_pixel_map(self.pixelmapper)

        print("%s stopped" % __name__)
        pass

    def input(self, event, axis, buttons):
        # self.axis_state = axis
        # self.pressed_buttons = buttons
        #
        # self.tick()
        pass

    def tick(self):
        # if self.pressed_buttons and sum(self.axis_state) != 0:
        #     if BTN_RED in self.pressed_buttons or BTN_YELLOW in self.pressed_buttons:
        #         self.pixelmapper.change_base_color(r=-self.axis_state[1])
        #     if BTN_GREEN in self.pressed_buttons or BTN_YELLOW in self.pressed_buttons:
        #         self.pixelmapper.change_base_color(g=-self.axis_state[1])
        #     if BTN_BLUE in self.pressed_buttons or BTN_YELLOW in self.pressed_buttons:
        #         self.pixelmapper.change_base_color(b=-self.axis_state[1])
        #
        #     self.refresh_color()
        #
        #     print self.pixelmapper.base_color

        if self.pixelmapper.base_color_changed:
            self.refresh_color()



    def refresh_color(self):
        for s in self.pixelmapper.strands:
            s.leds = [self.pixelmapper.base_color] * s.length

        self.pixelcontroller.set_pixel_map(self.pixelmapper)
        self.pixelmapper.base_color_changed = False
