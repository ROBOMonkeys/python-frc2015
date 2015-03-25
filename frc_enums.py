from enum import Enum


class XboxButtons(Enum):
    A = 1
    B = 2
    X = 3
    Y = 4
    L_bump = 5
    R_bump = 6
    start = 7
    select = 8


class XboxAxis(Enum):
    R_X = 1
    R_Y = 2
    L_X = 4
    L_Y = 5
    Z = 3
