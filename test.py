#!/usr/bin/env python

from podctl import PodCtl

ctl = PodCtl()
# ctl.sparkle(100, 100, 100, 0.1, 10)
# ctl.pulse(128, 0, 0, 0, 0, 128, 2)
# ctl.fade(0, 0, 0, 192, 4, 4, 3)
# ctl.play_sound('C:/Users/xinco/Music/test.mp3', lambda: ctl.sparkle(128, 8, 4, 0.1, 1))
ctl.sound_pulse('C:/Users/xinco/Music/test.mp3', 0, 0, 0, 128, 4, 12)

# Cycle colors
# current_color = (0, 0, 0)
# next_color = (128, 0, 64)
# options = (3, 10)
#
# for i in range(5):
#     params = current_color + next_color + options
#     print params
#     ctl.fade(*params)
#
#     current_color = next_color
#     next_color = ((current_color[0] + 32) % 256, (current_color[1] + 32) % 256, (current_color[2] + 32) % 256)

# Reset to black
ctl.set_pod_color(0, 0, 0)

