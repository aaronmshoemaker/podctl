#!/usr/bin/env python

from podctl import PodCtl

ctl = PodCtl()
# ctl.sparkle(100, 0, 0, 0.1, 10)
ctl.play_sound('C:/Users/xinco/Music/test.mp3', lambda: ctl.sparkle(100, 0, 0, 0.1, 10))

# Reset to black
ctl.set_pod_color(0, 0, 0)

