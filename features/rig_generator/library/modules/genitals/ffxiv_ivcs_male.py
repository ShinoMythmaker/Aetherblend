"""Male IVCS genitals."""
from ....definitions import RigModule
from ....instructions import *
from ....rigify.settings import BoneCollection, UI_Collections

COLLECTION = "Genitals (Male)"
PENIS_SOURCES = ["iv_ochinko_a", "iv_ochinko_b", "iv_ochinko_c", "iv_ochinko_d", "iv_ochinko_e", "iv_ochinko_f"]
PENIS_BONES = ["Penis", "Penis.001", "Penis.002", "Penis.003", "Penis.004", "Penis.005"]
TESTICLES = (("Testicle.R", "iv_kougan_r"), ("Testicle.L", "iv_kougan_l"))


class Module(RigModule):
    name = "XIV-IVCS Male"
    ui_collections = UI_Collections([
        BoneCollection(name=COLLECTION, ui=True, color_set="IVCS", row_index=1, title=COLLECTION, visible=False),
    ])

    def meta_edit(self, rig):
        if has_bone(rig, PENIS_SOURCES[0]) and has_bone(rig, PENIS_SOURCES[1]):
            connect(rig, "Penis", PENIS_SOURCES[0], PENIS_SOURCES[1], parent=["Spine.001", "j_kosi"])
            for index in range(1, 5):
                connect(rig, PENIS_BONES[index], PENIS_SOURCES[index], PENIS_SOURCES[index + 1], parent=PENIS_BONES[index - 1], connected=True)
            extend(rig, "Penis.005", PENIS_SOURCES[5], parent="Penis.004", connected=True)

        for name, source in TESTICLES:
            if has_bone(rig, source):
                extend(rig, name, source, start_point="head", size_factor=0.5, parent=["Spine.001", "j_kosi"])

    def meta_pose(self, rig):
        if "Penis" in rig.pose.bones:
            rigify.limbs_spline_tentacle(rig, "Penis", sik_stretch_control="MANUAL_STRETCH")
            collection(rig, PENIS_BONES, COLLECTION)
            for source, bone in zip(PENIS_SOURCES, PENIS_BONES):
                link(rig, source, f"DEF-{bone}")

        for name, source in TESTICLES:
            if name in rig.pose.bones:
                rigify.skin_basic_chain(rig, name, control_orientation_bone="Spine.001")
                collection(rig, [name], COLLECTION)
                link(rig, source, f"DEF-{name}")
