from .humanoid import *
from ..bone_gen import BoneGroup

HUMAN: list[list[BoneGroup]] = [
    [SPINE],
    [ARM_R],
    [ARM_L],
    [LEG_R],
    [LEG_L],
    [SKIRT_R],
    [SKIRT_R_MCH],
    [SKIRT_L],
    [SKIRT_L_MCH],
    [HAND_R],
    [HAND_L],
    [TAIL],
    [HEAD],
]