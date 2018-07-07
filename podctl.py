#!/usr/bin/env python

import lighting.opc
import time

# Config
panelCount = 6
edgesPerPanel = 6
pixelsPerEdge = 20
pixelsPerPanel = edgesPerPanel * pixelsPerEdge


class PodCtl:
    client = None

    def __init__(self):
        print 'PodCtl init...'
        self.client = lighting.opc.Client('localhost:7890', True, False)
        pass

    def sparkle(self, r, g, b, delay, iterations):
        print 'Sparkling...'

        iterations *= 2  # A single 'sparkle' is an alternation between 2 states

        for i in range(iterations):
            self.set_pod_color_alternating(i % 2 == 0, r, g, b)
            time.sleep(delay)

    def pulse(self, r, g, b, cycleTime=1, steps=10):

        total_steps = steps * 2
        r_step = int(r / steps)
        g_step = int(g / steps)
        b_step = int(b / steps)

        r, g, b = 0

        for i in range(total_steps):
            self.set_pod_color(r, g, b)

            if i < steps:
                r += r_step
                b += b_step
                g += g_step
            else:
                r -= r_step
                b -= b_step
                g -= g_step

            time.sleep(cycleTime / total_steps)

    def set_pod_color(self, r, g, b):
        for i in range(panelCount):
            self.client.put_pixels(self.get_pixels_solid(r, g, b), channel=i)

    def set_pod_color_alternating(self, even, r, g, b):
        for i in range(panelCount):
            print "Alternating channel %s, even=%s" % (i, even)
            self.client.put_pixels(self.get_pixels_alternating(even, r, g, b), channel=i)

    @staticmethod
    def get_pixels_solid(r=0, g=0, b=0, count=pixelsPerPanel):
        return [(r, g, b)] * count

    @staticmethod
    def get_pixels_alternating(even=True, r=0, g=0, b=0, count=pixelsPerPanel):
        if even:
            return [(0, 0, 0), (r, g, b)] * int(count / 2)
        else:
            return [(r, g, b), (0, 0, 0)] * int(count / 2)


def main():
    print 'main'
    ctl = PodCtl();
    ctl.sparkle(100, 100, 100, 0.01, 1)


if __name__ == '__main__':
    main()
