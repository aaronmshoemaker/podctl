AXIS_X = 0
AXIS_Y = 1

BTN_BLUE = 0
BTN_RED = 1
BTN_YELLOW = 2
BTN_GREEN = 3
BTN_L_BUMBER = 4
BTN_R_BUMBER = 5
BTN_SELECT = 8
BTN_START = 9

SHUTDOWN_SEQUENCE = [BTN_SELECT, BTN_START, BTN_L_BUMBER, BTN_R_BUMBER]

# Todo: automatically set based on available power supply.
MAX_BRIGHTNESS = 128  # Max is 256. Artificially cap brightness to limit amperage draw.
COLOR_BLANK = (0, 0, 0)
COLOR_STATUS_READY = (0, 96, 0)
COLOR_STATUS_READY_ALT = (64, 0, 64)
COLOR_STATUS_SHUTDOWN = (128, 0, 0)
COLOR_STATUS_SHUTDOWN_ALT = (64, 64, 0)
