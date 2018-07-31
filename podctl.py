#!/usr/bin/env python

from __future__ import division
import lighting.opc
import sound.audio
import time

# Config
channelCount = 1
pixelsPerChannel = 128


class PodCtl:
    fadecandy = None
    sound_tools = None

    def __init__(self):
        print 'PodCtl init...'
        # Set up Fadecandy board
        self.fadecandy = lighting.opc.Client('localhost:7890', True, False)

        # Set up sound mixer
        self.sound_tools = sound.audio.Audio()
        pass

    def sparkle(self, r, g, b, delay, iterations):
        iterations *= 2  # A single 'sparkle' is an alternation between 2 states

        for i in range(iterations):
            self.set_pod_color_alternating(i % 2 == 0, r, g, b)
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
            self.set_pod_color(int(r), int(g), int(b))

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

    def set_pod_color(self, r, g, b):
        for i in range(channelCount):
            self.fadecandy.put_pixels(self.get_pixels_solid(r, g, b), channel=i)

    def set_pod_color_alternating(self, even, r, g, b):
        for i in range(channelCount):
            # print("Alternating channel %s, even=%s" % (i, even))
            self.fadecandy.put_pixels(self.get_pixels_alternating(even, r, g, b), channel=i)

    def play_sound(self, path, runWhilePlaying=None):
        self.sound_tools.play_sound(path, runWhilePlaying)

    def sound_fade(self, path, start_r, start_g, start_b, end_r, end_g, end_b):
        seconds = self.sound_tools.get_sound_length(path)
        self.sound_tools.play_sound(path)
        self.fade(start_r, start_g, start_b, end_r, end_g, end_b, seconds, int(seconds) * 10)

    def sound_pulse(self, path, start_r, start_g, start_b, end_r, end_g, end_b):
        seconds = self.sound_tools.get_sound_length(path)
        self.sound_tools.play_sound(path)
        self.pulse(start_r, start_g, start_b, end_r, end_g, end_b, seconds, int(seconds) * 10)

    def stop_sound(self):
        self.sound_tools.sound_tools.stop()

    @staticmethod
    def get_pixels_solid(r=0, g=0, b=0, count=pixelsPerChannel):
        return [(r, g, b)] * count

    @staticmethod
    def get_pixels_alternating(even=True, r=0, g=0, b=0, count=pixelsPerChannel):
        if even:
            return [(0, 0, 0), (r, g, b)] * int(count / 2)
        else:
            return [(r, g, b), (0, 0, 0)] * int(count / 2)


# def main():
#     print 'main'
#     ctl = PodCtl()
#     ctl.play_sound('test.mp3', lambda: ctl.sparkle(128, 8, 4, 0.1, 1))
#
#     # Reset to black
#     ctl.set_pod_color(0, 0, 0)
#
#
# if __name__ == '__main__':
#     main()
