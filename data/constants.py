from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class MetaRigCollectionInfo:
    name: str
    color_type: str
    row_index: int
    title: str


@dataclass(frozen=True)
class RigifySettings:
    rigify_type: str | None = None
    fk_coll: str | None = None
    tweak_coll: str | None = None
    copy_rot_axes: Dict[str, bool] | None = None


@dataclass(frozen=True)
class BoneChainInfo:
    ffxiv_bones: list[str]
    gen_bones: dict[str, RigifySettings | None]
    parent_bone: str | None
    extend_last: bool
    extension_factor: float
