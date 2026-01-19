from .humanoid import *
from ..bone_gen import BoneGroup

HUMAN: list[list[BoneGroup]] = [
    [SPINE],
    [ARM_R],
    [ARM_L],
    [LEG_R],
    [LEG_L],
    [SKIRT_R],
]