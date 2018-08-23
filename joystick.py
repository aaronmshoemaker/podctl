#!/usr/bin/env python

import pygame
from constants import *
from pixelcontroller import PixelController
from pixelmapper import PixelMapper, Strand
from modes.joyspin import Joyspin
from modes.chase import Chase
from modes.simplecolor import SimpleColor
from modes.pulse import Pulse
from modes.rainbow import Rainbow
from os import environ
import os
import time

# TODO: Fix class variable names
pixelmapper = PixelMapper(
    [
        Strand(0, 34),
        Strand(64, 34),
        Strand(128, 34),
        Strand(192, 34),
        Strand(256, 34),
     ]
)
pixelcontroller = PixelController()
OPTS = None
JOYSTICKS = []
AXIS_INPUT = [0, 0]
PRESSED_BUTTONS = set()
MODES = [
    # SimpleColor(pixelmapper, pixelcontroller),
    # Chase(pixelmapper, pixelcontroller),
    # Joyspin(pixelmapper, pixelcontroller),
    # Pulse(pixelmapper, pixelcontroller, 300),
    Rainbow(pixelmapper, pixelcontroller, length=20),
]
ACTIVE_MODE_IDX = -1
ACTIVE_MODE = None


def proc_event(event):
    """Parse and act upon event"""
    # Update global control state
    if event.type == pygame.QUIT:
        print("Received event 'Quit', exiting.")
        exit(0)
    elif event.type == pygame.JOYAXISMOTION:
        AXIS_INPUT[event.axis] = int(event.value)
    elif event.type == pygame.JOYBUTTONDOWN:
        PRESSED_BUTTONS.add(event.button)
    elif event.type == pygame.JOYBUTTONUP:
        PRESSED_BUTTONS.remove(event.button)
    elif event.type == pygame.USEREVENT and ACTIVE_MODE:
        ACTIVE_MODE.tick()

    if OPTS.debug:
        print PRESSED_BUTTONS
        print AXIS_INPUT

    # Handle mode changes
    if event.type == pygame.JOYBUTTONUP and event.button == BTN_SELECT:
        cycle_mode()
    elif event.type == pygame.JOYBUTTONUP and event.button == BTN_START:
        restart_mode()

    # Handle shutdown signal
    if event.type == pygame.JOYBUTTONDOWN and len(PRESSED_BUTTONS.intersection(SHUTDOWN_SEQUENCE)) == len(SHUTDOWN_SEQUENCE):
        shutdown()

    if ACTIVE_MODE:
        ACTIVE_MODE.input(event, AXIS_INPUT, PRESSED_BUTTONS)


def cycle_mode():
    """Cycles to the next available mode"""
    global MODES, ACTIVE_MODE_IDX, ACTIVE_MODE

    if ACTIVE_MODE:
        ACTIVE_MODE.stop()

    ACTIVE_MODE_IDX = (ACTIVE_MODE_IDX + 1) % len(MODES)
    ACTIVE_MODE = MODES[ACTIVE_MODE_IDX]

    ACTIVE_MODE.start()

    pygame.time.set_timer(pygame.USEREVENT, ACTIVE_MODE.tick_ms)


def restart_mode():
    """Cycles to the next available mode"""
    global MODES, ACTIVE_MODE_IDX, ACTIVE_MODE

    if ACTIVE_MODE:
        ACTIVE_MODE.stop()

    ACTIVE_MODE.start()


def shutdown():
    pixelcontroller.set_color_alternating(COLOR_STATUS_SHUTDOWN, COLOR_STATUS_SHUTDOWN_ALT)
    time.sleep(2)

    try:
        os.system("init 0")
    except:
        pass


def get_opts():
    """Parse command line options"""
    from argparse import ArgumentParser
    parser = ArgumentParser()
    arg = parser.add_argument
    arg('-d', '--debug', action='store_true', default=False, help="Prints debug messages")
    return parser.parse_args()


def main():
    global OPTS
    OPTS = get_opts()

    environ["SDL_VIDEODRIVER"] = "dummy"
    environ["SDL_AUDIODRIVER"] = "dummy"

    pygame.init()
    clock = pygame.time.Clock()

    for i in range(0, pygame.joystick.get_count()):
        JOYSTICKS.append(pygame.joystick.Joystick(i))
        JOYSTICKS[-1].init()

        if OPTS.debug:
            print("Detected joystick '%s'" % JOYSTICKS[-1].get_name())

    # Set initial color to indicate readiness
    pixelcontroller.set_color_alternating(COLOR_STATUS_READY, COLOR_STATUS_READY_ALT)

    while 1:
        try:
            clock.tick(30)
            for event in pygame.event.get():
                proc_event(event)

            # Handle color change inputs
            if PRESSED_BUTTONS and sum(AXIS_INPUT) != 0:
                if BTN_RED in PRESSED_BUTTONS or BTN_YELLOW in PRESSED_BUTTONS:
                    pixelmapper.change_base_color(r=-AXIS_INPUT[1])
                if BTN_GREEN in PRESSED_BUTTONS or BTN_YELLOW in PRESSED_BUTTONS:
                    pixelmapper.change_base_color(g=-AXIS_INPUT[1])
                if BTN_BLUE in PRESSED_BUTTONS or BTN_YELLOW in PRESSED_BUTTONS:
                    pixelmapper.change_base_color(b=-AXIS_INPUT[1])

        except KeyboardInterrupt:
            print("\n" "Interrupted")
            exit(0)


if __name__ == "__main__":
    main()
