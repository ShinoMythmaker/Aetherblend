from .humanoid import *
from .hand import *

HUMAN: list[list[list[GenerativeBone]]] = [
    [SPINE],
    [ARM_L],
    [ARM_R],
    [LEG_L],
    [LEG_R],
    [TAIL],

    [THUMB_L],
    [THUMB_R],
    [POINTER_L_IV, POINTER_L],
    [POINTER_R_IV, POINTER_R],
    [MIDDLE_L_IV, MIDDLE_L],
    [MIDDLE_R_IV, MIDDLE_R],
    [RING_L_IV, RING_L],
    [RING_R_IV, RING_R],
    [PINKY_L_IV, PINKY_L],
    [PINKY_R_IV, PINKY_R],

    [HEAD],
    [CHEEK_L],
    [CHEEK_R],
    [BROW_L],
    [BROW_R],
    [JAW],
    [MOUTH],
    [EAR_L],
    [EAR_R],

    [EYE_L],
    [EYE_R],

    [SKIRT]
]
