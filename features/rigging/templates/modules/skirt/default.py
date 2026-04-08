from ......core.rigify.settings import UI_Collections, BoneCollection
from ......core.generators import ConnectBone, ExtensionBone
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify

SKIRT_R = BoneGroup(
        name="Skirt Right",
        transform_link= [
            TransformLink(target="DEF-Skirt_Front.R", bone="j_sk_f_a_r"),
            TransformLink(target="DEF-Skirt_Front.R.001", bone="j_sk_f_b_r"),
            TransformLink(target="DEF-Skirt_Front.R.002", bone="j_sk_f_c_r"),
            TransformLink(target="DEF-Skirt_Side.R", bone="j_sk_s_a_r"),
            TransformLink(target="DEF-Skirt_Side.R.001", bone="j_sk_s_b_r"),
            TransformLink(target="DEF-Skirt_Side.R.002", bone="j_sk_s_c_r"),
            TransformLink(target="DEF-Skirt_Back.R", bone="j_sk_b_a_r"),
            TransformLink(target="DEF-Skirt_Back.R.001", bone="j_sk_b_b_r"),
            TransformLink(target="DEF-Skirt_Back.R.002", bone="j_sk_b_c_r"),
            ],
        bones = [
            #Front
            ConnectBone(
                name="Skirt_Front.R",
                bone_a="j_sk_f_a_r",
                bone_b="j_sk_f_b_r",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_f_a_r", "j_sk_f_b_r"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, primary_layer_extra="Skirt", skin_chain_falloff_length=True, skin_chain_falloff_spherical=[True, False, True]),
                    b_collection="Skirt (Tweak)"
                )
            ),
            ConnectBone(
                name="Skirt_Front.R.001",
                bone_a="j_sk_f_b_r",
                bone_b="j_sk_f_c_r",
                parent="Skirt_Front.R",
                is_connected=True,
                req_bones=["j_sk_f_b_r", "j_sk_f_c_r"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
            ExtensionBone(
                name="Skirt_Front.R.002",
                bone_a="j_sk_f_c_r",
                parent="Skirt_Front.R.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="tail",
                req_bones=["j_sk_f_c_r"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
            #Side
            ConnectBone(
                name="Skirt_Side.R",
                bone_a="j_sk_s_a_r",
                bone_b="j_sk_s_b_r",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_s_a_r", "j_sk_s_b_r"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, primary_layer_extra="Skirt", skin_chain_falloff_length=True, skin_chain_falloff_spherical=[True, False, True]),
                    b_collection="Skirt (Tweak)"
                )
            ),
            ConnectBone(
                name="Skirt_Side.R.001",
                bone_a="j_sk_s_b_r",
                bone_b="j_sk_s_c_r",
                parent="Skirt_Side.R",
                is_connected=True,
                req_bones=["j_sk_s_b_r", "j_sk_s_c_r"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
            ExtensionBone(
                name="Skirt_Side.R.002",
                bone_a="j_sk_s_c_r",
                parent="Skirt_Side.R.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="head",
                req_bones=["j_sk_s_c_r"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
            #Back
            ConnectBone(
                name="Skirt_Back.R",
                bone_a="j_sk_b_a_r",
                bone_b="j_sk_b_b_r",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_b_a_r", "j_sk_b_b_r"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, primary_layer_extra="Skirt", skin_chain_falloff_length=True, skin_chain_falloff_spherical=[True, False, True]),
                    b_collection="Skirt (Tweak)"
                )
            ),
            ConnectBone(
                name="Skirt_Back.R.001",
                bone_a="j_sk_b_b_r",
                bone_b="j_sk_b_c_r",
                parent="Skirt_Back.R",
                is_connected=True,
                req_bones=["j_sk_b_b_r", "j_sk_b_c_r"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
            ExtensionBone(
                name="Skirt_Back.R.002",
                bone_a="j_sk_b_c_r",
                parent="Skirt_Back.R.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="head",
                req_bones=["j_sk_b_c_r"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
             #Front
            ConnectBone(
                name="Skirt_Front.R.mch",
                bone_a="shin.R",
                bone_b="Skirt_Front.R.002",
                parent="shin.R",
                is_connected=False,
                end="tail",
                req_bones=["Skirt_Front.R.002"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_basic_chain(skin_chain_priority=1, skin_control_orientation_bone="Skirt_Front.R.002"),
                    b_collection="Skirt MCH"
                )
            ),
            ConnectBone(
                name="Skirt_Side.R.mch",
                bone_a="shin.R",
                bone_b="Skirt_Side.R.002",
                parent="shin.R",
                is_connected=False,
                end="tail",
                req_bones=["Skirt_Side.R.002"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_basic_chain(skin_chain_priority=1, skin_control_orientation_bone="Skirt_Side.R.002"),
                    b_collection="Skirt MCH"
                )
            ),
            ConnectBone(
                name="Skirt_Back.R.mch",
                bone_a="shin.R",
                bone_b="Skirt_Back.R.002",
                parent="shin.R",
                is_connected=False,
                end="tail",
                req_bones=["Skirt_Back.R.002"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_basic_chain(skin_chain_priority=1, skin_control_orientation_bone="Skirt_Back.R.002"),
                    b_collection="Skirt MCH"
                )
            ),
        ],
)

SKIRT_L = BoneGroup(
        name="Skirt Left",
        transform_link= [
            TransformLink(target="DEF-Skirt_Front.L", bone="j_sk_f_a_l"),
            TransformLink(target="DEF-Skirt_Front.L.001", bone="j_sk_f_b_l"),
            TransformLink(target="DEF-Skirt_Front.L.002", bone="j_sk_f_c_l"),
            TransformLink(target="DEF-Skirt_Side.L", bone="j_sk_s_a_l"),
            TransformLink(target="DEF-Skirt_Side.L.001", bone="j_sk_s_b_l"),
            TransformLink(target="DEF-Skirt_Side.L.002", bone="j_sk_s_c_l"),
            TransformLink(target="DEF-Skirt_Back.L", bone="j_sk_b_a_l"),
            TransformLink(target="DEF-Skirt_Back.L.001", bone="j_sk_b_b_l"),
            TransformLink(target="DEF-Skirt_Back.L.002", bone="j_sk_b_c_l"),
            ],
        bones = [
            #Front
            ConnectBone(
                name="Skirt_Front.L",
                bone_a="j_sk_f_a_l",
                bone_b="j_sk_f_b_l",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_f_a_l", "j_sk_f_b_l"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, primary_layer_extra="Skirt", skin_chain_falloff_length=True, skin_chain_falloff_spherical=[True, False, True]),
                    b_collection="Skirt (Tweak)"
                )
            ),
            ConnectBone(
                name="Skirt_Front.L.001",
                bone_a="j_sk_f_b_l",
                bone_b="j_sk_f_c_l",
                parent="Skirt_Front.L",
                is_connected=True,
                req_bones=["j_sk_f_b_l", "j_sk_f_c_l"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
            ExtensionBone(
                name="Skirt_Front.L.002",
                bone_a="j_sk_f_c_l",
                parent="Skirt_Front.L.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="tail",
                req_bones=["j_sk_f_c_l"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
            #Side
            ConnectBone(
                name="Skirt_Side.L",
                bone_a="j_sk_s_a_l",
                bone_b="j_sk_s_b_l",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_s_a_l", "j_sk_s_b_l"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, primary_layer_extra="Skirt", skin_chain_falloff_length=True, skin_chain_falloff_spherical=[True, False, True]),
                    b_collection="Skirt (Tweak)"
                )
            ),
            ConnectBone(
                name="Skirt_Side.L.001",
                bone_a="j_sk_s_b_l",
                bone_b="j_sk_s_c_l",
                parent="Skirt_Side.L",
                is_connected=True,
                req_bones=["j_sk_s_b_l", "j_sk_s_c_l"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
            ExtensionBone(
                name="Skirt_Side.L.002",
                bone_a="j_sk_s_c_l",
                parent="Skirt_Side.L.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="head",
                req_bones=["j_sk_s_c_l"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
            #Back
            ConnectBone(
                name="Skirt_Back.L",
                bone_a="j_sk_b_a_l",
                bone_b="j_sk_b_b_l",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_b_a_l", "j_sk_b_b_l"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, primary_layer_extra="Skirt", skin_chain_falloff_length=True, skin_chain_falloff_spherical=[True, False, True]),
                    b_collection="Skirt (Tweak)"
                )
            ),
            ConnectBone(
                name="Skirt_Back.L.001",
                bone_a="j_sk_b_b_l",
                bone_b="j_sk_b_c_l",
                parent="Skirt_Back.L",
                is_connected=True,
                req_bones=["j_sk_b_b_l", "j_sk_b_c_l"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
            ExtensionBone(
                name="Skirt_Back.L.002",
                bone_a="j_sk_b_c_l",
                parent="Skirt_Back.L.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="head",
                req_bones=["j_sk_b_c_l"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
            #Front
            ConnectBone(
                name="Skirt_Front.L.mch",
                bone_a="shin.L",
                bone_b="Skirt_Front.L.002",
                parent="shin.L",
                is_connected=False,
                end="tail",
                req_bones=["Skirt_Front.L.002"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_basic_chain(skin_chain_priority=1, skin_control_orientation_bone="Skirt_Front.L.002"),
                    b_collection="Skirt MCH"
                )
            ),
            #Side
            ConnectBone(
                name="Skirt_Side.L.mch",
                bone_a="shin.L",
                bone_b="Skirt_Side.L.002",
                parent="shin.L",
                is_connected=False,
                end="tail",
                req_bones=["Skirt_Side.L.002"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_basic_chain(skin_chain_priority=1, skin_control_orientation_bone="Skirt_Side.L.002"),
                    b_collection="Skirt MCH"
                )
            ),
            #Back
            ConnectBone(
                name="Skirt_Back.L.mch",
                bone_a="shin.L",
                bone_b="Skirt_Back.L.002",
                parent="shin.L",
                is_connected=False,
                end="tail",
                req_bones=["Skirt_Back.L.002"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_basic_chain(skin_chain_priority=1, skin_control_orientation_bone="Skirt_Back.L.002"),
                    b_collection="Skirt MCH"
                )
            ),
        ],
)

def get_rig_module() -> RigModule:
    return RigModule(
        name="Default",
        type="Generation",
        bone_groups=[SKIRT_R, SKIRT_L],
        ui = UI_Collections([
            BoneCollection(name="Skirt", ui=True, color_set="Torso", row_index=1, title="Skirt", visible=False),
            BoneCollection(name="Skirt (Tweak)", ui=True, color_set="Torso", row_index=2, title="Skirt (Tweak)", visible=False),
        ])
    )
