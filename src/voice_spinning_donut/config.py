import os

import numpy as np

TITLE = "Spinning Donut with Voice Control"
ICON_PATH = os.path.join("assets", "images", "donut.png")
SCREEN_SIZE = 640
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

A = 1
B = 1
R1 = 1
R2 = 2
K2 = 5
K1 = SCREEN_SIZE * K2 * 3 / (8 * (R1 + R2))

THETA_SPACING = 0.07
PHI_SPACING = 0.02
ILLUMINATION = np.fromiter(".,-~:;=!*#$@", dtype="<U1")
INITIAL_ANGLE = 1.0
CIRCLE_POINTS = 90

INITIAL_ROTATION_SPEED = 4
MAX_ROTATION_SPEED = 20
MIN_ROTATION_SPEED = 0

VOICE_UPDATE_INTERVAL = 1.0

COLOR_THEMES = {
    "white": [(255, 255, 255)] * len(ILLUMINATION),
    "red": [(i * 15 % 255, 0, 0) for i in range(len(ILLUMINATION))],
    "green": [(0, i * 15 % 255, 0) for i in range(len(ILLUMINATION))],
    "blue": [(0, 0, i * 15 % 255) for i in range(len(ILLUMINATION))],
}

DEFAULT_THEME = "white"
