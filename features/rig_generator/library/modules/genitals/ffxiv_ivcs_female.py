"""Female IVCS genitals."""
from ....instructions import *
from ....module import RigModule
from ....rigify.settings import BoneCollection, UI_Collections

COLLECTION = "Genitals (Female)"
PARTS = (
    ("Clitoris", "iv_kuritto", ["Spine.001", "j_kosi"]),
    ("Vulva.R", "iv_inshin_r", "Spine.001"),
    ("Vulva.L", "iv_inshin_l", "Spine.001"),
    ("Vulva", "iv_omanko", "Spine.001"),
)


class Module(RigModule):
    name = "XIV-IVCS Female"
    ui_collections = UI_Collections([
        BoneCollection(name=COLLECTION, ui=True, color_set="IVCS", row_index=1, title=COLLECTION, visible=False),
    ])

    def meta_edit(self, rig):
        for name, source, parent_bone in PARTS:
            if has_bone(rig, source) and has_bone(rig, "j_kosi"):
                connect(rig, name, source, "j_kosi", parent=parent_bone)
        if has_bone(rig, "Clitoris"):
            extend(rig, "Anchor_V", "Clitoris", parent="Spine.001")

    def meta_pose(self, rig):
        for name, source, _ in PARTS:
            if name in rig.pose.bones:
                rigify.skin_basic_chain(rig, name, control_orientation_bone="Spine.001")
                collection(rig, [name], COLLECTION)
                link(rig, source, f"DEF-{name}")
        if "Anchor_V" in rig.pose.bones:
            rigify.skin_anchor(rig, "Anchor_V", hide=True)
            collection(rig, ["Anchor_V"], COLLECTION)

    def final_pose(self, rig):
        for name, _, _ in PARTS:
            widget(rig, name, scale_factor=0.2)
