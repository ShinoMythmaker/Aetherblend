"""Hair module: every hair and head accessory bone chain becomes a controllable chain."""

import typing

import bpy

from .... import definitions
from .... import instructions as abi


class Pattern(typing.NamedTuple):
    """Source bone names to rig, and the bone collection their controls go to."""

    regex: str
    collection: str


PATTERNS = (
    Pattern(r"^j_ex_h.*", "Hair"),
    Pattern(r"^j_kami.*", "Hair"),
    Pattern(r"^j_ex_met.*", "Accessory"),
)


class Module(definitions.RigModule):
    """Build FFXIV player hair and head accessory controls."""

    name = "FFXIV Player Hair"

    def __init__(self) -> None:
        self.chains: list[tuple[list[str], str]] = []

    # ------------------------------------------------------------------------

    def meta_edit(self, rig: bpy.types.Object) -> None:
        """Discover and build hair and accessory chains."""
        self.chains = []
        # Hair and accessory chains
        for pattern in PATTERNS:
            for chain in abi.find_chains(rig, pattern.regex):
                self.chains.append((chain, pattern.collection))

                if len(chain) == 1:
                    abi.extend(
                        rig,
                        f"HAIR_{chain[0]}",
                        chain[0],
                        start_point="head",
                        size_factor=10.0,
                        parent=["Head", "j_kao"],
                    )
                    continue

                for index, source in enumerate(chain[:-1]):
                    parent_bone = ["Head", "j_kao"] if index == 0 else f"HAIR_{chain[index - 1]}"
                    abi.connect(
                        rig,
                        f"HAIR_{source}",
                        source,
                        chain[index + 1],
                        parent=parent_bone,
                        connected=index > 0,
                    )
                last = chain[-1]
                abi.extend(
                    rig,
                    f"HAIR_{last}",
                    last,
                    start_point="head",
                    parent=f"HAIR_{chain[-2]}",
                    connected=True,
                )

    # ------------------------------------------------------------------------

    def meta_pose(self, rig: bpy.types.Object) -> None:
        """Configure the discovered controls and deform mappings."""
        # Chain controls
        for chain, collection_name in self.chains:
            bones = [f"HAIR_{source}" for source in chain]
            if len(chain) == 1:
                abi.rigify.basic_super_copy(rig, bones[0], widget_type="bone")
            else:
                abi.rigify.basic_copy_chain(rig, bones[0])
            abi.collection(rig, bones, collection_name)

            # Source-to-deform mappings
            for source, bone in zip(chain, bones):
                abi.link(rig, source, f"DEF-{bone}")
