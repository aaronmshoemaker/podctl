from collections import deque

class Pulse:
    pixelmapper = None
    pixelcontroller = None
    tick_ms = None
    pulse_steps = 10
    color_queue = deque()

    def __init__(self, pixelmapper, pixelcontroller, tick_ms=100):
        self.pixelmapper = pixelmapper
        self.pixelcontroller = pixelcontroller
        self.tick_ms = tick_ms

    def start(self):
        print("%s started" % __name__)

    def stop(self):
        self.pixelcontroller.set_color()
        print("%s stopped" % __name__)

    def input(self, event, axis, buttons):
        pass

    def tick(self):
        if len(self.color_queue) == 0:
            self.load_color_queue(self.pixelmapper.base_color, self.pixelmapper.get_random_color())

        self.pixelmapper.base_color = self.color_queue.popleft()
        self.pixelcontroller.set_color(*self.pixelmapper.base_color)

    def load_color_queue(self, start_color, end_color):
        for c in self.pixelmapper.get_color_sequence(start_color, end_color, self.pulse_steps):
            self.color_queue.append(c)
        pass