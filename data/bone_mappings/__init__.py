from .humanoid import *
from .. generate import BoneGroup

HUMAN: list[list[BoneGroup]] = [
    [BoneGroup(
        name="Right Arm",
        bones=ARM_R,
        description="Right arm bones including upper arm, forearm, hand, and tweak bones"
    )],
]