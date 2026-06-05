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


xiv_tail_bones = ["n_sippo_a", "n_sippo_b", "n_sippo_c", "n_sippo_d", "n_sippo_e"]
sb_tail_parent_bone = "j_kosi"
sb_tail_collection = "SB_Tail"

xiv_ear_bone_r = ["j_mimi_r"]
sb_ear_target_bone_r = ["n_ear_a_r"]
xiv_ear_bone_l = ["j_mimi_l"]
sb_ear_target_bone_l = ["n_ear_a_l"]
sb_ear_parent_bone = "j_kao"
sb_ears_collection = "SB_Ear"

xiv_breast_bone_r = ["j_mune_r"]
xiv_breast_bone_l = ["j_mune_l"]
sb_breast_parent_bone = "j_sebo_b"
sb_breast_collection = "SB_Breast"

spring_prefix = "sb_"
spring_bone_collection = "Spring Bones"
