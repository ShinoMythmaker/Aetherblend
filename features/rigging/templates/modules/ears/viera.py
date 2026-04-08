from ......core.generators import ConnectBone
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify

VIERA_EARS = BoneGroup(
    name="Viera Ears",
    transform_link=[
        TransformLink(target="DEF-V_Ear.R", bone="j_zera_a_r"),
        TransformLink(target="DEF-V_Ear.R.001", bone="j_zera_b_r"),
        TransformLink(target="DEF-V_Ear.R", bone="j_zerb_a_r"),
        TransformLink(target="DEF-V_Ear.R.001", bone="j_zerb_b_r"),
        TransformLink(target="DEF-V_Ear.R", bone="j_zerc_a_r"),
        TransformLink(target="DEF-V_Ear.R.001", bone="j_zerc_b_r"),
        TransformLink(target="DEF-V_Ear.R", bone="j_zerd_a_r"),
        TransformLink(target="DEF-V_Ear.R.001", bone="j_zerd_b_r"),

        TransformLink(target="DEF-V_Ear.L", bone="j_zera_a_l"),
        TransformLink(target="DEF-V_Ear.L.001", bone="j_zera_b_l"),
        TransformLink(target="DEF-V_Ear.L", bone="j_zerb_a_l"),
        TransformLink(target="DEF-V_Ear.L.001", bone="j_zerb_b_l"),
        TransformLink(target="DEF-V_Ear.L", bone="j_zerc_a_l"),
        TransformLink(target="DEF-V_Ear.L.001", bone="j_zerc_b_l"),
        TransformLink(target="DEF-V_Ear.L", bone="j_zerd_a_l"),
        TransformLink(target="DEF-V_Ear.L.001", bone="j_zerd_b_l"),
    ],
    bones=[
        ConnectBone(
            name="V_Ear.R",
            bone_a="j_zera_a_r",
            bone_b="j_zera_b_r",
            parent="Head",
            is_connected=False,
            req_bones=["j_zera_a_r", "j_zera_b_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.basic_copy_chain(),
                b_collection="Head",
            )
        ),
        ConnectBone(
            name="V_Ear.R.001",
            bone_a="j_zera_b_r",
            bone_b="j_zera_b_r",
            parent="V_Ear.R",
            is_connected=True,
            start="head",
            end="tail",
            req_bones=["j_zera_b_r", "j_zera_b_r"],
            pose_operations=PoseOperations(
                b_collection="Head",
            )
        ),
        ConnectBone(
            name="V_Ear.L",
            bone_a="j_zera_a_l",
            bone_b="j_zera_b_l",
            parent="Head",
            is_connected=False,
            req_bones=["j_zera_a_l", "j_zera_b_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.basic_copy_chain(),
                b_collection="Head",
            )
        ),
        ConnectBone(
            name="V_Ear.L.001",
            bone_a="j_zera_b_l",
            bone_b="j_zera_b_l",
            parent="V_Ear.L",
            is_connected=True,
            start="head",
            end="tail",
            req_bones=["j_zera_b_l", "j_zera_b_l"],
            pose_operations=PoseOperations(
                b_collection="Head",
            )
        ),
    ]
)

def get_rig_module() -> RigModule:
    rig_module = RigModule(
        name="Viera",
        type="Generation",
        bone_groups=[VIERA_EARS]
    )
    return rig_module