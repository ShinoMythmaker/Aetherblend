import mathutils

from ......core.rigify.settings import UI_Collections, BoneCollection
from ......core.operations import CollectionOperation, ParentBoneOperation, RigifyTypeOperation
from ......core.generators import ConnectBone, ExtensionBone, CenterBone, CopyBone, SkinBone, BridgeBone
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify

MOUTH_AUTO = BoneGroup(
    name="Mouth",
    transform_link=[],
    generators=[
        #Jaw
        CenterBone(
            name="jaw_master_ref",
            ref_bones=["j_f_dlip_01_r", "j_f_dlip_01_l"],
            axis="Y",
            inverted=False,
            parent="Head",
            req_bones=["j_f_dlip_01_r", "j_f_dlip_01_l"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="jaw_master_ref", collection_name="MCH")
                        ]
        ),
        ConnectBone(
            name="jaw_master",
            bone_a="j_f_ago",
            bone_b="jaw_master_ref",
            parent="Head",
            req_bones=["j_f_ago", "jaw_master_ref"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="jaw_master", rigify_type=rigify.types.face_skin_jaw(jaw_mouth_influence = 1)),
                        CollectionOperation(time="Pre", bone_name="jaw_master", collection_name="Face (Primary)")
            ]
        ),
                #Mouth Center Reference
        CenterBone(
            name="Mouth.Center",
            ref_bones=["j_f_ulip_01_r", "j_f_ulip_01_l"],
            axis="Y",
            inverted=False,
            parent="Head",
            req_bones=["j_f_ulip_01_r", "j_f_ulip_01_l"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="Mouth.Center", collection_name="MCH")
                        ]
        ),
        #Mouth Right
        ConnectBone(
            name="Lip.T.R",
            bone_a="Mouth.Center",
            bone_b="j_f_ulip_01_r",
            parent="jaw_master",
            req_bones=["j_f_ulip_01_r", "Mouth.Center"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Lip.T.R", rigify_type=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Head", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 0.0, -1.0], primary_layer_extra="Mouth (Primary)")),
                        CollectionOperation(time="Pre", bone_name="Lip.T.R", collection_name="Mouth (Primary)")
                        ]
        ),
        ConnectBone(
            name="Lip.T.R.001",
            bone_a="j_f_ulip_01_r",
            bone_b="j_f_umlip_01_r",
            parent="Lip.T.R",
            is_connected=True,
            req_bones=["j_f_umlip_01_r", "j_f_ulip_01_r"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="Lip.T.R.001", collection_name="Mouth (Primary)")
                        ]
        ),
        ConnectBone(
            name="Lip.B.R",
            bone_a="jaw_master_ref",
            bone_b="j_f_dlip_01_r",
            parent="jaw_master",
            req_bones=["j_f_dlip_01_r", "jaw_master_ref"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Lip.B.R", rigify_type=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Head", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 0.0, -1.0], primary_layer_extra="Mouth (Primary)")),
                        CollectionOperation(time="Pre", bone_name="Lip.B.R", collection_name="Mouth (Primary)")
                        ]
        ),
        ConnectBone(
            name="Lip.B.R.001",
            bone_a="j_f_dlip_01_r",
            bone_b="j_f_dmlip_01_r",
            parent="Lip.B.R",
            is_connected=True,
            req_bones=["j_f_dmlip_01_r", "j_f_dlip_01_r"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="Lip.B.R.001", collection_name="Mouth (Primary)")
                        ]
        ),
        
        #This is a reference point for the last bone in the chain
        CenterBone(
            name="Corner.R",
            ref_bones=["j_f_uslip_r", "j_f_dslip_r", "Cheek.B.R"],
            axis="Y",
            inverted=False,
            parent="Head",
            req_bones=["j_f_uslip_r", "j_f_dslip_r", "Cheek.B.R"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="Corner.R", collection_name="MCH")
            ]
        ),
        ConnectBone(
            name="Lip.T.R.002",
            bone_a="j_f_umlip_01_r",
            bone_b="j_f_uslip_r",
            parent="Lip.T.R.001",
            is_connected=True,
            req_bones=["j_f_uslip_r", "j_f_umlip_01_r"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="Lip.T.R.002", collection_name="Mouth (Primary)")
                        ]
        ),
        ConnectBone(
            name="Lip.T.R.003",
            bone_a="j_f_uslip_r",
            bone_b="Corner.R",
            parent="Lip.T.R.002",
            is_connected=True,
            req_bones=["j_f_uslip_r", "Corner.R"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="Lip.T.R.003", collection_name="Mouth (Primary)")
                        ]
        ),
        ConnectBone(
            name="Lip.B.R.002",
            bone_a="j_f_dmlip_01_r",
            bone_b="j_f_dslip_r",
            parent="Lip.B.R.001",
            is_connected=True,
            req_bones=["j_f_dmlip_01_r", "j_f_dslip_r"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="Lip.B.R.002", collection_name="Mouth (Primary)")
                        ]
        ),
        ConnectBone(
            name="Lip.B.R.003",
            bone_a="j_f_dslip_r",
            bone_b="Corner.R",
            parent="Lip.B.R.002",
            is_connected=True,
            req_bones=["j_f_dslip_r", "Corner.R"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="Lip.B.R.003", collection_name="Face")
                        ]
        ),

        #Left Mouth
        ConnectBone(
            name="Lip.T.L",
            bone_a="Mouth.Center",
            bone_b="j_f_ulip_01_l",
            parent="jaw_master",
            req_bones=["j_f_ulip_01_l", "Mouth.Center"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Lip.T.L", rigify_type=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Head", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 0.0, -1.0], primary_layer_extra="Mouth (Primary)")),
                        CollectionOperation(time="Pre", bone_name="Lip.T.L", collection_name="Mouth (Primary)"),
                        ]
        ),
        ConnectBone(
            name="Lip.T.L.001",
            bone_a="j_f_ulip_01_l",
            bone_b="j_f_umlip_01_l",
            parent="Lip.T.L",
            is_connected=True,
            req_bones=["j_f_umlip_01_l", "j_f_ulip_01_l"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="Lip.T.L.001", collection_name="Mouth (Primary)")
            ]
        ),
        ConnectBone(
            name="Lip.B.L",
            bone_a="jaw_master_ref",
            bone_b="j_f_dlip_01_l",
            parent="jaw_master",
            req_bones=["j_f_dlip_01_l", "jaw_master_ref"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Lip.B.L", rigify_type=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Head", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 0.0, -1.0], primary_layer_extra="Mouth (Primary)")),
                        CollectionOperation(time="Pre", bone_name="Lip.B.L", collection_name="Mouth (Primary)")
            ]
        ),
        ConnectBone(
            name="Lip.B.L.001",
            bone_a="j_f_dlip_01_l",
            bone_b="j_f_dmlip_01_l",
            parent="Lip.B.L",
            is_connected=True,
            req_bones=["j_f_dmlip_01_l", "j_f_dlip_01_l"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="Lip.B.L.001", collection_name="Mouth (Primary)")
            ]
        ),
        #This is a reference point for the last bone in the chain
        CenterBone(
            name="Corner.L",
            ref_bones=["j_f_uslip_l", "j_f_dslip_l", "Cheek.B.L"],
            axis="Y",
            inverted=False,
            parent="Head",
            req_bones=["j_f_uslip_l", "j_f_dslip_l", "Cheek.B.L"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="Corner.L", collection_name="MCH")
            ]
        ),
        ConnectBone(
           name = "Lip.T.L.002",
           bone_a = "j_f_umlip_01_l",
           bone_b = "j_f_uslip_l",
           parent="Lip.T.L.001",
           is_connected=True,
           req_bones = ["j_f_umlip_01_l", "j_f_uslip_l"],
           operations=[
                       CollectionOperation(time="Pre", bone_name="Lip.T.L.002", collection_name="Mouth (Primary)")
           ]
       ),
        ConnectBone(
           name = "Lip.T.L.003",
           bone_a = "j_f_uslip_l",
           bone_b = "Corner.L",
           parent="Lip.T.L.002",
           is_connected=True,
           req_bones = ["j_f_uslip_l", "Corner.L"],
           operations=[
                       CollectionOperation(time="Pre", bone_name="Lip.T.L.003", collection_name="Mouth (Primary)")
           ]
       ),
        ConnectBone(
           name = "Lip.B.L.002",
           bone_a = "j_f_dmlip_01_l",
           bone_b = "j_f_dslip_l",
           parent="Lip.B.L.001",
           is_connected=True,
           req_bones = ["j_f_dmlip_01_l", "j_f_dslip_l"],
           operations=[
                       CollectionOperation(time="Pre", bone_name="Lip.B.L.002", collection_name="Mouth (Primary)")
           ]
       ),
        ConnectBone(
           name = "Lip.B.L.003",
           bone_a = "j_f_dslip_l",
           bone_b = "Corner.L",
           parent="Lip.B.L.002",
           is_connected=True,
           req_bones = ["Corner.L", "j_f_dslip_l"],
           operations=[
                       CollectionOperation(time="Pre", bone_name="Lip.B.L.003", collection_name="Mouth (Primary)")
           ]
       ),
        #Teeth
        ExtensionBone(
            name="Teeth.T",
            bone_a="j_f_hagukiup",
            size_factor=1,
            axis_type="local",
            axis="Y",
            start="head",
            parent="Head",
            req_bones=["j_f_hagukiup"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Teeth.T", rigify_type=rigify.types.basic_super_copy(widget_type="teeth")),
                        CollectionOperation(time="Pre", bone_name="Teeth.T", collection_name="Mouth (Secondary)")
            ]
        ),
        ExtensionBone(
            name="Teeth.B",
            bone_a="j_f_hagukidn",
            size_factor=1,
            axis_type="local",
            axis="Y",
            start="head",
            parent="jaw_master",
            req_bones=["j_f_hagukidn"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Teeth.B", rigify_type=rigify.types.basic_super_copy(widget_type="teeth")),
                        CollectionOperation(time="Pre", bone_name="Teeth.B", collection_name="Mouth (Secondary)")
            ]
        ),
        #Tongue
        ConnectBone(
            name="Tongue",
            bone_a="j_f_bero_01",
            bone_b="j_f_bero_02",
            parent="jaw_master",
            req_bones=["j_f_bero_01", "j_f_bero_02"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Tongue", rigify_type=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Tongue", collection_name="Mouth (Secondary)")
            ]
        ),
        ConnectBone(
            name="Tongue.001",
            bone_a="j_f_bero_02",
            bone_b="j_f_bero_03",
            parent="Tongue",
            is_connected=True,
            req_bones=["j_f_bero_02", "j_f_bero_03"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="Tongue.001", collection_name="Mouth (Secondary)")
            ]
        ),
        ExtensionBone(
            name="Tongue.002",
            bone_a="Tongue.001",
            axis_type="local",
            axis="Y",
            parent="Tongue.001",
            is_connected=True,
            req_bones=["Tongue.001"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="Tongue.002", collection_name="Mouth (Secondary)")
            ]
        ),
    ]
)
def get_rig_module() -> RigModule:
    return RigModule(
        name="Default",
        type="Generation",
        bone_groups=[MOUTH_AUTO],
        ui = UI_Collections([
            BoneCollection(name="Mouth (Primary)", ui=True, color_set="Face_Primary", row_index=2, title="Mouth (Primary)", visible=True),
            BoneCollection(name="Mouth (Secondary)", ui=True, color_set="Face_Secondary", row_index=2, title="Mouth (Secondary)", visible=False),
        ])
    )