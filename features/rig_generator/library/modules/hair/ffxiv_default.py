"""Hair module: every hair and head accessory bone chain becomes a controllable chain."""

from typing import NamedTuple

import bpy

from ....definitions import RigModule
from ....instructions import *
from ....rigify.settings import BoneCollection, UI_Collections

HEAD_PARENT = ["Head", "j_kao"]
BONE_PREFIX = "HAIR"
SINGLE_BONE_SIZE_FACTOR = 10.0


class Pattern(NamedTuple):
    """Source bone names to rig, and the bone collection their controls go to."""

    regex: str
    collection: str


PATTERNS = (
    Pattern(r"^j_ex_h.*", "Hair"),
    Pattern(r"^j_kami.*", "Hair"),
    Pattern(r"^j_ex_met.*", "Accessory"),
)


class Module(RigModule):
    name = "XIV-Default"
    ui_collections = UI_Collections(
        [
            BoneCollection(name="Hair", ui=True, color_set="Head", row_index=1, title="Hair", visible=False),
            BoneCollection(name="Accessory", ui=True, color_set="Head", row_index=1, title="Accessory", visible=False),
        ]
    )

    def __init__(self) -> None:
        self.chains: list[tuple[list[str], str]] = []

    def meta_edit(self, rig: bpy.types.Object) -> None:
        self.chains = []
        for pattern in PATTERNS:
            for chain in find_chains(rig, pattern.regex):
                self.chains.append((chain, pattern.collection))

                if len(chain) == 1:
                    extend(
                        rig,
                        f"{BONE_PREFIX}_{chain[0]}",
                        chain[0],
                        start_point="head",
                        size_factor=SINGLE_BONE_SIZE_FACTOR,
                        parent=HEAD_PARENT,
                    )
                    continue

                for index, source in enumerate(chain[:-1]):
                    parent_bone = HEAD_PARENT if index == 0 else f"{BONE_PREFIX}_{chain[index - 1]}"
                    connect(
                        rig,
                        f"{BONE_PREFIX}_{source}",
                        source,
                        chain[index + 1],
                        parent=parent_bone,
                        connected=index > 0,
                    )
                last = chain[-1]
                extend(
                    rig,
                    f"{BONE_PREFIX}_{last}",
                    last,
                    start_point="head",
                    parent=f"{BONE_PREFIX}_{chain[-2]}",
                    connected=True,
                )

    def meta_pose(self, rig: bpy.types.Object) -> None:
        for chain, collection_name in self.chains:
            bones = [f"{BONE_PREFIX}_{source}" for source in chain]
            if len(chain) == 1:
                rigify.basic_super_copy(rig, bones[0], widget_type="bone")
            else:
                rigify.basic_copy_chain(rig, bones[0])
            collection(rig, bones, collection_name)

            for source, bone in zip(chain, bones):
                link(rig, source, f"DEF-{bone}")
