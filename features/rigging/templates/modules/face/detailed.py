import mathutils

from ......core.rigify.settings import UI_Collections, BoneCollection
from ......core.operations import CollectionOperation, ParentBoneOperation, RigifyTypeOperation
from ......core.generators import ConnectBone, ExtensionBone, CenterBone, CopyBone, SkinBone, BridgeBone
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify

HEAD = BoneGroup(
    name="Head",
    transform_link= [
        TransformLink(target="DEF-Neck", bone="j_kubi"),
        TransformLink(target="DEF-Head", bone="j_kao"),
        TransformLink(target="DEF-jaw_master", bone="j_f_ago"),
        TransformLink(target="DEF-Cheek.B.R", bone="j_f_shoho_r"),
        TransformLink(target="DEF-Cheek.B.R.001", bone="j_f_dhoho_r"),
        TransformLink(target="DEF-Cheek.T.R", bone="j_f_hoho_r"),
        TransformLink(target="DEF-Cheek.T.R.001", bone="j_f_dmemoto_r"),
        TransformLink(target="DEF-Cheek.B.L", bone="j_f_shoho_l"),
        TransformLink(target="DEF-Cheek.B.L.001", bone="j_f_dhoho_l"),
        TransformLink(target="DEF-Cheek.T.L", bone="j_f_hoho_l"),
        TransformLink(target="DEF-Cheek.T.L.001", bone="j_f_dmemoto_l"),
        TransformLink(target="DEF-Nose", bone="j_f_uhana"),
        TransformLink(target="DEF-Nose.R", bone="j_f_dmiken_r"),
        TransformLink(target="DEF-Nostril.R", bone="j_f_hana_r"),
        TransformLink(target="DEF-Nose.L", bone="j_f_dmiken_l"),
        TransformLink(target="DEF-Nostril.L", bone="j_f_hana_l"),
        TransformLink(target="DEF-Lip.T.R.001", bone="j_f_ulip_01_r"),
        TransformLink(target="DEF-Lip.T.R.002", bone="j_f_umlip_01_r"),
        TransformLink(target="DEF-Lip.T.R.003", bone="j_f_uslip_r"),
        TransformLink(target="DEF-Lip.B.R.001", bone="j_f_dlip_01_r"),
        TransformLink(target="DEF-Lip.B.R.002", bone="j_f_dmlip_01_r"),
        TransformLink(target="DEF-Lip.B.R.003", bone="j_f_dslip_r"),
        TransformLink(target="DEF-Lip.T.L.001", bone="j_f_ulip_01_l"),
        TransformLink(target="DEF-Lip.T.L.002", bone="j_f_umlip_01_l"),
        TransformLink(target="DEF-Lip.T.L.003", bone="j_f_uslip_l"),
        TransformLink(target="DEF-Lip.B.L.001", bone="j_f_dlip_01_l"),
        TransformLink(target="DEF-Lip.B.L.002", bone="j_f_dmlip_01_l"),
        TransformLink(target="DEF-Lip.B.L.003", bone="j_f_dslip_l"),
        TransformLink(target="Lip.T.L.001", bone="j_f_ulip_02_l"),
        TransformLink(target="Lip.T.L.002", bone="j_f_umlip_02_l"),
        TransformLink(target="Lip.T.R.001", bone="j_f_ulip_02_r"),
        TransformLink(target="Lip.T.R.002", bone="j_f_umlip_02_r"),
        TransformLink(target="Lip.B.L.001", bone="j_f_dlip_02_l"),
        TransformLink(target="Lip.B.L.002", bone="j_f_dmlip_02_l"),
        TransformLink(target="Lip.B.R.001", bone="j_f_dlip_02_r"),
        TransformLink(target="Lip.B.R.002", bone="j_f_dmlip_02_r"),
        TransformLink(target="DEF-Teeth.T", bone="j_f_hagukiup"),
        TransformLink(target="DEF-Teeth.B", bone="j_f_hagukidn"),
        TransformLink(target="DEF-Tongue", bone="j_f_bero_01"),
        TransformLink(target="DEF-Tongue.001", bone="j_f_bero_02"),
        TransformLink(target="DEF-Tongue.002", bone="j_f_bero_03"),
    ],
    generators=[
        ConnectBone(
            name="Neck",
            bone_a="j_kubi",
            bone_b="j_kao",
            req_bones=["j_kubi", "j_kao"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Neck", parent=["Spine.004", "j_sebo_c"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Neck", rigify_type=rigify.types.spines_super_head()),
                        CollectionOperation(time="Pre", bone_name="Neck", collection_name="Head"),
            ]
        ),
        ExtensionBone(
            name="Head",
            bone_a="j_kao",
            axis_type="armature",
            axis="Z",
            size_factor=20.0,
            req_bones=["j_kao"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Head", parent=["Neck"], is_connected=True),
                        CollectionOperation(time="Pre", bone_name="Head", collection_name="Head")
                        ]
        ),
        #Cheek Right
        ConnectBone(
            name="Cheek.B.R",
            bone_a="j_f_shoho_r",
            bone_b="j_kao",
            req_bones=["j_f_shoho_r", "j_kao"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Cheek.B.R", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Cheek.B.R", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Cheek.B.R", collection_name="Face (Primary)")
                        ]
        ),
        ConnectBone(
            name="Cheek.B.R.001",
            bone_a="j_f_dhoho_r",
            bone_b="j_kao",
            req_bones=["j_f_dhoho_r", "j_kao"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Cheek.B.R.001", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Cheek.B.R.001", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Cheek.B.R.001", collection_name="Face (Secondary)")
                        ]
        ),
        ConnectBone(
            name="Cheek.T.R",
            bone_a="j_f_hoho_r",
            bone_b="j_kao",
            req_bones=["j_f_hoho_r", "j_kao"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Cheek.T.R", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Cheek.T.R", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Cheek.T.R", collection_name="Face (Primary)")
                        ]
        ),
        ConnectBone(
            name="Cheek.T.R.001",
            bone_a="j_f_dmemoto_r",
            bone_b="j_kao",
            req_bones=["j_f_dmemoto_r", "j_kao"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Cheek.T.R.001", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Cheek.T.R.001", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Cheek.T.R.001", collection_name="Face (Secondary)")
                        ]
        ),
        #Cheek Left
        ConnectBone(
            name="Cheek.B.L",
            bone_a="j_f_shoho_l",
            bone_b="j_kao",
            req_bones=["j_f_shoho_l", "j_kao"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Cheek.B.L", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Cheek.B.L", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Cheek.B.L", collection_name="Face (Primary)")
                        ]

        ),
        ConnectBone(
            name="Cheek.B.L.001",
            bone_a="j_f_dhoho_l",
            bone_b="j_kao",
            req_bones=["j_f_dhoho_l", "j_kao"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Cheek.B.L.001", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Cheek.B.L.001", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Cheek.B.L.001", collection_name="Face (Secondary)")
                        ]
        ),
        ConnectBone(
            name="Cheek.T.L",
            bone_a="j_f_hoho_l",
            bone_b="j_kao",
            req_bones=["j_f_hoho_l", "j_kao"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Cheek.T.L", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Cheek.T.L", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Cheek.T.L", collection_name="Face (Primary)")
                        ]
        ),
        ConnectBone(
            name="Cheek.T.L.001",
            bone_a="j_f_dmemoto_l",
            bone_b="j_kao",
            req_bones=["j_f_dmemoto_l", "j_kao"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Cheek.T.L.001", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Cheek.T.L.001", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Cheek.T.L.001", collection_name="Face (Secondary)")
                        ]
        ),
        #Nose Centre
        ConnectBone(
            name="Nose",
            bone_a="j_f_uhana",
            bone_b="j_kao",
            req_bones=["j_f_uhana", "j_kao"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Nose", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Nose", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Nose", collection_name="Face (Primary)")
                        ]
        ),
        #Nose Right
        ConnectBone(
            name="Nose.R",
            bone_a="j_f_dmiken_r",
            bone_b="j_kao",
            req_bones=["j_f_dmiken_r", "j_kao"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Nose.R", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Nose.R", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Nose.R", collection_name="Face (Primary)")
                        ]
        ),
        ConnectBone(
            name="Nostril.R",
            bone_a="j_f_hana_r",
            bone_b="j_kao",
            req_bones=["j_f_hana_r", "j_kao"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Nostril.R", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Nostril.R", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Nostril.R", collection_name="Face (Primary)")
                        ]
        ),
        #Nose Left
        ConnectBone(
            name="Nose.L",
            bone_a="j_f_dmiken_l",
            bone_b="j_kao",
            req_bones=["j_f_dmiken_l", "j_kao"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Nose.L", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Nose.L", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Nose.L", collection_name="Face (Primary)")
                        ]
        ),
        ConnectBone(
            name="Nostril.L",
            bone_a="j_f_hana_l",
            bone_b="j_kao",
            req_bones=["j_f_hana_l", "j_kao"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Nostril.L", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Nostril.L", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Nostril.L", collection_name="Face (Primary)")
                        ]
        ),
        
        #Anchor
        ExtensionBone(
            name="Face.Suppressor",
            bone_a="j_kao",
            parent="j_kao",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            size_factor=1.0,
            req_bones=["j_kao"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Face.Suppressor", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Face.Suppressor", rigify_type=rigify.types.skin_anchor(skin_anchor_hide=True)),
                        CollectionOperation(time="Pre", bone_name="Face.Suppressor", collection_name="MCH")
                        ]
        ),
        #Jaw
        CenterBone(
            name="jaw_master_ref",
            ref_bones=["j_f_dlip_01_r", "j_f_dlip_01_l"],
            axis="Y",
            inverted=False,
            req_bones=["j_f_dlip_01_r", "j_f_dlip_01_l"],
            operations=[ParentBoneOperation(time="Pre", bone_name="jaw_master_ref", parent=["Head"], is_connected=False),
                        CollectionOperation(time="Pre", bone_name="jaw_master_ref", collection_name="MCH")
                        ]
        ),
        ConnectBone(
            name="jaw_master",
            bone_a="j_f_ago",
            bone_b="jaw_master_ref",
            req_bones=["j_f_ago", "jaw_master_ref"],
            operations=[ParentBoneOperation(time="Pre", bone_name="jaw_master", parent=["Head"], is_connected=False),
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
            req_bones=["j_f_ulip_01_r", "j_f_ulip_01_l"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Mouth.Center", parent=["Head"], is_connected=False),
                        CollectionOperation(time="Pre", bone_name="Mouth.Center", collection_name="MCH")
                        ]
        ),
        #Mouth Right
        ConnectBone(
            name="Lip.T.R",
            bone_a="Mouth.Center",
            bone_b="j_f_ulip_01_r",
            req_bones=["j_f_ulip_01_r", "Mouth.Center"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Lip.T.R", parent=["jaw_master"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Lip.T.R", rigify_type=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Head", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 0.0, -1.0], primary_layer_extra="Face (Primary)")),
                        CollectionOperation(time="Pre", bone_name="Lip.T.R", collection_name="Face (Primary)")
                        ]
        ),
        ConnectBone(
            name="Lip.T.R.001",
            bone_a="j_f_ulip_01_r",
            bone_b="j_f_umlip_01_r",
            req_bones=["j_f_umlip_01_r", "j_f_ulip_01_r"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Lip.T.R.001", parent=["Lip.T.R"], is_connected=True),
                        CollectionOperation(time="Pre", bone_name="Lip.T.R.001", collection_name="Face")
                        ]
        ),
        ConnectBone(
            name="Lip.B.R",
            bone_a="jaw_master_ref",
            bone_b="j_f_dlip_01_r",
            req_bones=["j_f_dlip_01_r", "jaw_master_ref"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Lip.B.R", parent=["jaw_master"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Lip.B.R", rigify_type=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Head", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 0.0, -1.0], primary_layer_extra="Face (Primary)")),
                        CollectionOperation(time="Pre", bone_name="Lip.B.R", collection_name="Face (Primary)")
                        ]
        ),
        ConnectBone(
            name="Lip.B.R.001",
            bone_a="j_f_dlip_01_r",
            bone_b="j_f_dmlip_01_r",
            req_bones=["j_f_dmlip_01_r", "j_f_dlip_01_r"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Lip.B.R.001", parent=["Lip.B.R"], is_connected=True),
                        CollectionOperation(time="Pre", bone_name="Lip.B.R.001", collection_name="Face")
                        ]
        ),
        
        #This is a reference point for the last bone in the chain
        CenterBone(
            name="Corner.R",
            ref_bones=["j_f_uslip_r", "j_f_dslip_r", "Cheek.B.R"],
            axis="Y",
            inverted=False,
            req_bones=["j_f_uslip_r", "j_f_dslip_r", "Cheek.B.R"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Corner.R", parent=["Head"], is_connected=False),
                        CollectionOperation(time="Pre", bone_name="Corner.R", collection_name="MCH")
            ]
        ),
        ConnectBone(
            name="Lip.T.R.002",
            bone_a="j_f_umlip_01_r",
            bone_b="j_f_uslip_r",
            req_bones=["j_f_uslip_r", "j_f_umlip_01_r"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Lip.T.R.002", parent=["Lip.T.R.001"], is_connected=True),
                        CollectionOperation(time="Pre", bone_name="Lip.T.R.002", collection_name="Face")
                        ]
        ),
        ConnectBone(
            name="Lip.T.R.003",
            bone_a="j_f_uslip_r",
            bone_b="Corner.R",
            req_bones=["j_f_uslip_r", "Corner.R"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Lip.T.R.003", parent=["Lip.T.R.002"], is_connected=True),
                        CollectionOperation(time="Pre", bone_name="Lip.T.R.003", collection_name="Face")
                        ]
        ),
        ConnectBone(
            name="Lip.B.R.002",
            bone_a="j_f_dmlip_01_r",
            bone_b="j_f_dslip_r",
            req_bones=["j_f_dmlip_01_r", "j_f_dslip_r"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Lip.B.R.002", parent=["Lip.B.R.001"], is_connected=True),
                        CollectionOperation(time="Pre", bone_name="Lip.B.R.002", collection_name="Face")
                        ]
        ),
        ConnectBone(
            name="Lip.B.R.003",
            bone_a="j_f_dslip_r",
            bone_b="Corner.R",
            req_bones=["j_f_dslip_r", "Corner.R"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Lip.B.R.003", parent=["Lip.B.R.002"], is_connected=True),
                        CollectionOperation(time="Pre", bone_name="Lip.B.R.003", collection_name="Face")
            ]
        ),

        #Left Mouth
        ConnectBone(
            name="Lip.T.L",
            bone_a="Mouth.Center",
            bone_b="j_f_ulip_01_l",
            req_bones=["j_f_ulip_01_l", "Mouth.Center"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Lip.T.L", parent=["jaw_master"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Lip.T.L", rigify_type=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Head", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 0.0, -1.0], primary_layer_extra="Face (Primary)")),
                        CollectionOperation(time="Pre", bone_name="Lip.T.L", collection_name="Face (Primary)"),
            ]
        ),
        ConnectBone(
            name="Lip.T.L.001",
            bone_a="j_f_ulip_01_l",
            bone_b="j_f_umlip_01_l",
            req_bones=["j_f_umlip_01_l", "j_f_ulip_01_l"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Lip.T.L.001", parent=["Lip.T.L"], is_connected=True),
                        CollectionOperation(time="Pre", bone_name="Lip.T.L.001", collection_name="Face")
            ]
        ),
        ConnectBone(
            name="Lip.B.L",
            bone_a="jaw_master_ref",
            bone_b="j_f_dlip_01_l",
            req_bones=["j_f_dlip_01_l", "jaw_master_ref"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Lip.B.L", parent=["jaw_master"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Lip.B.L", rigify_type=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Head", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 0.0, -1.0], primary_layer_extra="Face (Primary)")),
                        CollectionOperation(time="Pre", bone_name="Lip.B.L", collection_name="Face (Primary)")
            ]
        ),
        ConnectBone(
            name="Lip.B.L.001",
            bone_a="j_f_dlip_01_l",
            bone_b="j_f_dmlip_01_l",
            req_bones=["j_f_dmlip_01_l", "j_f_dlip_01_l"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Lip.B.L.001", parent=["Lip.B.L"], is_connected=True),
                        CollectionOperation(time="Pre", bone_name="Lip.B.L.001", collection_name="Face")
            ]
        ),
        #This is a reference point for the last bone in the chain
        CenterBone(
            name="Corner.L",
            ref_bones=["j_f_uslip_l", "j_f_dslip_l", "Cheek.B.L"],
            axis="Y",
            inverted=False,
            req_bones=["j_f_uslip_l", "j_f_dslip_l", "Cheek.B.L"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Corner.L", parent=["Head"], is_connected=False),
                        CollectionOperation(time="Pre", bone_name="Corner.L", collection_name="MCH")
            ]
        ),
        ConnectBone(
           name = "Lip.T.L.002",
           bone_a = "j_f_umlip_01_l",
           bone_b = "j_f_uslip_l",
           req_bones = ["j_f_umlip_01_l", "j_f_uslip_l"],
           operations=[ParentBoneOperation(time="Pre", bone_name="Lip.T.L.002", parent=["Lip.T.L.001"], is_connected=True),
                       CollectionOperation(time="Pre", bone_name="Lip.T.L.002", collection_name="Face")
           ]
       ),
        ConnectBone(
           name = "Lip.T.L.003",
           bone_a = "j_f_uslip_l",
           bone_b = "Corner.L",
           req_bones = ["j_f_uslip_l", "Corner.L"],
           operations=[ParentBoneOperation(time="Pre", bone_name="Lip.T.L.003", parent=["Lip.T.L.002"], is_connected=True),
                       CollectionOperation(time="Pre", bone_name="Lip.T.L.003", collection_name="Face")
           ]
       ),
        ConnectBone(
           name = "Lip.B.L.002",
           bone_a = "j_f_dmlip_01_l",
           bone_b = "j_f_dslip_l",
           req_bones = ["j_f_dmlip_01_l", "j_f_dslip_l"],
           operations=[ParentBoneOperation(time="Pre", bone_name="Lip.B.L.002", parent=["Lip.B.L.001"], is_connected=True),
                       CollectionOperation(time="Pre", bone_name="Lip.B.L.002", collection_name="Face")
           ]
       ),
        ConnectBone(
           name = "Lip.B.L.003",
           bone_a = "j_f_dslip_l",
           bone_b = "Corner.L",
           req_bones = ["Corner.L", "j_f_dslip_l"],
           operations=[ParentBoneOperation(time="Pre", bone_name="Lip.B.L.003", parent=["Lip.B.L.002"], is_connected=True),
                       CollectionOperation(time="Pre", bone_name="Lip.B.L.003", collection_name="Face")
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
            operations=[ParentBoneOperation(time="Pre", bone_name="Teeth.T", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Teeth.T", rigify_type=rigify.types.basic_super_copy(widget_type="teeth")),
                        CollectionOperation(time="Pre", bone_name="Teeth.T", collection_name="Mouth")
            ]
        ),
        ExtensionBone(
            name="Teeth.B",
            bone_a="j_f_hagukidn",
            size_factor=1,
            axis_type="local",
            axis="Y",
            start="head",
            operations=[ParentBoneOperation(time="Pre", bone_name="Teeth.B", parent=["jaw_master"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Teeth.B", rigify_type=rigify.types.basic_super_copy(widget_type="teeth")),
                        CollectionOperation(time="Pre", bone_name="Teeth.B", collection_name="Mouth")
            ]
        ),
        #Tongue
        ConnectBone(
            name="Tongue",
            bone_a="j_f_bero_01",
            bone_b="j_f_bero_02",
            req_bones=["j_f_bero_01", "j_f_bero_02"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Tongue", parent=["jaw_master"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Tongue", rigify_type=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Tongue", collection_name="Mouth")
            ]
        ),
        ConnectBone(
            name="Tongue.001",
            bone_a="j_f_bero_02",
            bone_b="j_f_bero_03",
            req_bones=["j_f_bero_02", "j_f_bero_03"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Tongue.001", parent=["Tongue"], is_connected=True),
                        CollectionOperation(time="Pre", bone_name="Tongue.001", collection_name="Mouth")
            ]
        ),
        ExtensionBone(
            name="Tongue.002",
            bone_a="Tongue.001",
            axis_type="local",
            axis="Y",
            req_bones=["Tongue.001"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Tongue.002", parent=["Tongue.001"], is_connected=True),
                        CollectionOperation(time="Pre", bone_name="Tongue.002", collection_name="Mouth")
            ]
        ),
        #Nose Glue
        ConnectBone(
            name="Nostril.Glue.R",
            bone_a="j_f_hana_r",
            bone_b="j_f_uhana",
            req_bones=["j_f_hana_r", "j_f_uhana"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Nostril.Glue.R", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Nostril.Glue.R", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Nostril.Glue.R", collection_name="MCH")
                        ]
        ),
        ConnectBone(
            name="Nostril.Glue.L",
            bone_a="j_f_hana_l",
            bone_b="j_f_uhana",
            req_bones=["j_f_hana_l", "j_f_uhana"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Nostril.Glue.L", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Nostril.Glue.L", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Nostril.Glue.L", collection_name="MCH")
                        ]
        ),
        ConnectBone(
            name="Nostril.Glue.R.001",
            bone_a="Cheek.T.R.001", 
            bone_b="Nostril.R",
            req_bones=["Cheek.T.R.001", "Nostril.R"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Nostril.Glue.R.001", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Nostril.Glue.R.001", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Nostril.Glue.R.001", collection_name="MCH")
                        ]
        ),
        ConnectBone(
            name="Nostril.Glue.L.001",
            bone_a="Cheek.T.L.001", 
            bone_b="Nostril.L",
            req_bones=["Cheek.T.L.001", "Nostril.L"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Nostril.Glue.L.001", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Nostril.Glue.L.001", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Nostril.Glue.L.001", collection_name="MCH")
            ]
        ),
        #Cheek Glue Bones Right
        ConnectBone(
            name="Cheek.B.R.glue",
            bone_a="j_f_dhoho_r",
            bone_b="j_f_shoho_r",
            req_bones=["j_f_shoho_r", "j_f_dhoho_r"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Cheek.B.R.glue", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Cheek.B.R.glue", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Cheek.B.R.glue", collection_name="MCH")
            ]
        ),
        ConnectBone(
            name="Cheek.T.R.glue",
            bone_a="j_f_dhoho_r",
            bone_b="j_f_hoho_r",
            req_bones=["j_f_hoho_r", "j_f_dhoho_r"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Cheek.T.R.glue", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Cheek.T.R.glue", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Cheek.T.R.glue", collection_name="MCH")
            ]
        ),
        #Cheek Glue Bones Left
        ConnectBone(
            name="Cheek.B.L.glue",
            bone_a="j_f_dhoho_l",
            bone_b="j_f_shoho_l",
            req_bones=["j_f_shoho_l", "j_f_dhoho_l"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Cheek.B.L.glue", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Cheek.B.L.glue", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Cheek.B.L.glue", collection_name="MCH")
            ]
        ),
        ConnectBone(
            name="Cheek.T.L.glue",
            bone_a="j_f_dhoho_l",
            bone_b="j_f_hoho_l",
            req_bones=["j_f_hoho_l", "j_f_dhoho_l"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Cheek.T.L.glue", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Cheek.T.L.glue", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Cheek.T.L.glue", collection_name="MCH")
            ]
        ),
        #Nostril Glue Bones
        ConnectBone(
            name="Nostril.Glue.R",
            bone_a="j_f_hana_r",
            bone_b="j_f_uhana",
            req_bones=["j_f_hana_r", "j_f_uhana"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Nostril.Glue.R", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Nostril.Glue.R", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Nostril.Glue.R", collection_name="MCH")
            ]
        ),
        ConnectBone(
            name="Nostril.Glue.L",
            bone_a="j_f_hana_l",
            bone_b="j_f_uhana",
            req_bones=["j_f_hana_l", "j_f_uhana"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Nostril.Glue.L", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Nostril.Glue.L", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Nostril.Glue.L", collection_name="MCH")
            ]
        ),
        ConnectBone(
            name="Nostril.Glue.R.001",
            bone_a="Cheek.T.R.001", 
            bone_b="Nostril.R",
            req_bones=["Cheek.T.R.001", "Nostril.R"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Nostril.Glue.R.001", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Nostril.Glue.R.001", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Nostril.Glue.R.001", collection_name="MCH")
            ]
        ),
        ConnectBone(
            name="Nostril.Glue.L.001",
            bone_a="Cheek.T.L.001", 
            bone_b="Nostril.L",
            req_bones=["Cheek.T.L.001", "Nostril.L"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Nostril.Glue.L.001", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Nostril.Glue.L.001", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Nostril.Glue.L.001", collection_name="MCH")
            ]
        ),
        #Lip Glue Bones
        ConnectBone(
            name="Lip.T.R.001.glue",
            bone_a="j_f_hana_r",
            bone_b="j_f_ulip_01_r",
            req_bones=["j_f_hana_r", "j_f_ulip_01_r"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Lip.T.R.001.glue", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Lip.T.R.001.glue", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.2, skin_glue_tail_reparent=True)),
                        CollectionOperation(time="Pre", bone_name="Lip.T.R.001.glue", collection_name="MCH")
            ]
        ),
        ConnectBone(
            name="Lip.T.L.001.glue",
            bone_a="j_f_hana_l",
            bone_b="j_f_ulip_01_l",
            req_bones=["j_f_hana_l", "j_f_ulip_01_l"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Lip.T.L.001.glue", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Lip.T.L.001.glue", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.2, skin_glue_tail_reparent=True)),
                        CollectionOperation(time="Pre", bone_name="Lip.T.L.001.glue", collection_name="MCH")
            ]
        ),
        #Mouth Corner Glue Bones
        ConnectBone(
            name="Mouth.Corner.glue.L",
            bone_a="j_f_shoho_l",
            bone_b="Corner.L",
            req_bones=["j_f_shoho_l", "Corner.L"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Mouth.Corner.glue.L", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Mouth.Corner.glue.L", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5, skin_glue_tail_reparent=True)),
                        CollectionOperation(time="Pre", bone_name="Mouth.Corner.glue.L", collection_name="MCH")
            ]
        ),
        ConnectBone(
            name="Mouth.Corner.glue.R",
            bone_a="j_f_shoho_r",
            bone_b="Corner.R",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_shoho_r", "Corner.R"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Mouth.Corner.glue.R", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Mouth.Corner.glue.R", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5, skin_glue_tail_reparent=True)),
                        CollectionOperation(time="Pre", bone_name="Mouth.Corner.glue.R", collection_name="MCH")
            ]
        ),    
    ]
)

BROW = BoneGroup(
    name="Brow",
    transform_link=[
        TransformLink(target="DEF-Brow.R", bone="j_f_mayu_r"),
        TransformLink(target="DEF-Brow.R.001", bone="j_f_mmayu_r"),
        TransformLink(target="DEF-Brow.R.002", bone="j_f_miken_01_r"),
        TransformLink(target="DEF-Brow.R.003", bone="j_f_miken_02_r"),
        TransformLink(target="DEF-Brow.L", bone="j_f_mayu_l"),
        TransformLink(target="DEF-Brow.L.001", bone="j_f_mmayu_l"),
        TransformLink(target="DEF-Brow.L.002", bone="j_f_miken_01_l"),
        TransformLink(target="DEF-Brow.L.003", bone="j_f_miken_02_l")
    ],
    generators=[
        ConnectBone(
            name="Brow.R",
            bone_a="j_f_mayu_r",
            bone_b="j_f_mmayu_r",
            req_bones=["j_f_mayu_r", "j_f_mmayu_r",],
            operations=[ParentBoneOperation(time="Pre", bone_name="Brow.R", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Brow.R", rigify_type=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, skin_control_orientation_bone="Head", skin_chain_falloff_length=True, primary_layer_extra="Face (Primary)")),
                        CollectionOperation(time="Pre", bone_name="Brow.R", collection_name="Face (Secondary)")
            ]
        ),
        ConnectBone(
            name="Brow.R.001",
            bone_a="j_f_mmayu_r",
            bone_b="j_f_miken_01_r",
            req_bones=["j_f_mmayu_r", "j_f_miken_01_r"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Brow.R.001", parent=["Brow.R"], is_connected=True),
                        CollectionOperation(time="Pre", bone_name="Brow.R.001", collection_name="Face (Primary)")
            ]
        ),
        ConnectBone(
            name="Brow.R.002",
            bone_a="j_f_miken_01_r",
            bone_b="j_f_miken_02_r",
            req_bones=["j_f_miken_01_r", "j_f_miken_02_r"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Brow.R.002", parent=["Brow.R.001"], is_connected=True),
                        CollectionOperation(time="Pre", bone_name="Brow.R.002", collection_name="Face (Primary)")
            ]
        ),
        ExtensionBone(
            name="Brow.R.003",
            bone_a="Brow.R.002",
            axis_type="local",
            axis="Y",
            req_bones=["j_f_miken_02_r"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Brow.R.003", parent=["Brow.R.002"], is_connected=True),
                        CollectionOperation(time="Pre", bone_name="Brow.R.003", collection_name="Face (Primary)")
            ]
        ),
        ConnectBone(
            name="Brow.L",
            bone_a="j_f_mayu_l",
            bone_b="j_f_mmayu_l",
            req_bones=["j_f_mayu_l", "j_f_mmayu_l",],
            operations=[ParentBoneOperation(time="Pre", bone_name="Brow.L", parent=["Head"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Brow.L", rigify_type=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, skin_control_orientation_bone="Head", skin_chain_falloff_length=True, primary_layer_extra="Face (Primary)")),
                        CollectionOperation(time="Pre", bone_name="Brow.L", collection_name="Face (Secondary)")
            ]
        ),
        ConnectBone(
            name="Brow.L.001",
            bone_a="j_f_mmayu_l",
            bone_b="j_f_miken_01_l",
            req_bones=["j_f_mmayu_l", "j_f_miken_01_l"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Brow.L.001", parent=["Brow.L"], is_connected=True),
                        CollectionOperation(time="Pre", bone_name="Brow.L.001", collection_name="Face (Primary)")
            ]
        ),
        ConnectBone(
            name="Brow.L.002",
            bone_a="j_f_miken_01_l",
            bone_b="j_f_miken_02_l",
            req_bones=["j_f_miken_01_l", "j_f_miken_02_l"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Brow.L.002", parent=["Brow.L.001"], is_connected=True),
                        CollectionOperation(time="Pre", bone_name="Brow.L.002", collection_name="Face (Primary)")
            ]
        ),
        ExtensionBone(
            name="Brow.L.003",
            bone_a="Brow.L.002",
            axis_type="local",
            axis="Y",
            req_bones=["j_f_miken_02_l"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Brow.L.003", parent=["Brow.L.002"], is_connected=True),
                        CollectionOperation(time="Pre", bone_name="Brow.L.003", collection_name="Face (Primary)")
            ]
        )
    ]
)

LEFT_EYE = BoneGroup(
    name="Eyes",
    transform_link= [
        TransformLink(target="lid.B.L.001", bone="j_f_mabdn_03in_l"),
        TransformLink(target="lid.B.L.002", bone="j_f_mabdn_01_l"),
        TransformLink(target="lid.B.L.003", bone="j_f_mabdn_02out_l"),
        TransformLink(target="lid.T.L.001", bone="j_f_mabup_02out_l"),
        TransformLink(target="lid.T.L.002", bone="j_f_mabup_01_l"),
        TransformLink(target="lid.T.L.003", bone="j_f_mabup_03in_l"),
        TransformLink(target="MCH-Eye.L", bone="j_f_eyepuru_l"),
    ],
    generators=[

        ## Skin Bone, Basicly Corner Bones for the eyes
        SkinBone(
            name="lid.T.L", 
            bone_a="j_f_mabup_02out_l", 
            mesh_restriction="eye_occlusion",
            req_bones=["j_f_mabup_02out_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=2, primary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="Head", skin_chain_falloff_spherical=[False, False, False], skin_chain_falloff=[0.0, 1.0, 0.0], skin_chain_falloff_length=True), 
                b_collection="Face (Secondary)"
                )
        ),
        SkinBone(
            name="lid.T.L.002", 
            bone_a="j_f_mabup_01_l", 
            mesh_restriction="eye_occlusion",
            req_bones=["j_f_mabup_01_l"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
                )
        ),
        SkinBone(
            name="lid.B.L", 
            bone_a="j_f_mabdn_03in_l", 
            mesh_restriction="eye_occlusion", 
            req_bones=["j_f_mabdn_03in_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=2, primary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="Head"), 
                b_collection="Face (Secondary)"
                )
        ),
        SkinBone(
            name="lid.B.L.002", 
            bone_a="j_f_mabdn_01_l", 
            mesh_restriction="eye_occlusion",
            req_bones=["j_f_mabdn_01_l"], 
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
                )
        ),


        CopyBone(
            name="Eye.L",
            source_bone="j_f_eyepuru_l",
            req_bones=["j_f_eyepuru_l"],
            parent="Head",
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.face_skin_eye(),
                b_collection="Face (Primary)"
            )
        ),

        # CenterBone(
        #     name="Eye.L",
        #     ref_bones=["lid.T.L", "lid.T.L.002", "lid.B.L", "lid.B.L.002"],
        #     parent="Head",
        #     axis="Y",
        #     inverted=True,
        #     req_bones=["lid.T.L", "lid.T.L.002", "lid.B.L", "lid.B.L.002"],
        #     pose_operations=PoseOperations(
        #         rigify_settings=rigify.types.face_skin_eye(),
        #         b_collection="Face"
        #     )
        # ),

        BridgeBone(
            name="lid.T.L.001",
            bone_a="lid.T.L",
            bone_b="lid.T.L.002",
            offset_factor=mathutils.Vector((0.0, -0.001, 0.001)),
            is_connected=True,  
            parent="Eye.L",
            req_bones=["lid.T.L", "lid.T.L.002"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
            )
        ), 

        BridgeBone(
            name="lid.T.L.003", 
            bone_a="lid.T.L.002",
            bone_b="lid.B.L",
            offset_factor=mathutils.Vector((0.0, 0.0, 0.003)),
            is_connected=False,
            req_bones=["lid.T.L.002", "lid.B.L"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
            )
        ),
        BridgeBone(
            name="lid.B.L.001",
            bone_a="lid.B.L",
            bone_b="lid.B.L.002",
            offset_factor=mathutils.Vector((-0.002, 0.0, 0.001)),
            is_connected=True,
            parent="Eye.L",
            req_bones=["lid.B.L", "lid.B.L.002"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
            )
        ),

        BridgeBone(
            name="lid.B.L.003",
            bone_a="lid.B.L.002",
            bone_b="lid.T.L",
            offset_factor=mathutils.Vector((0.003, -0.001, -0.003)),
            is_connected=False,
            req_bones=["lid.B.L.002", "lid.T.L"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
            )
        ),


        ConnectBone(
            name="eye_tracker.B.L.001",
            bone_a="j_f_mabdn_03in_l",
            bone_b="lid.B.L.001",
            parent="Eye.L",
            is_connected=False,
            req_bones=["j_f_mabdn_03in_l", "j_f_eye_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),

        ConnectBone(
            name="eye_tracker.B.L.002",
            bone_a="j_f_mabdn_01_l",
            bone_b="lid.B.L.002",
            parent="Eye.L",
            is_connected=False,
            req_bones=["j_f_mabdn_01_l", "j_f_eye_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),

        ConnectBone(
            name="eye_tracker.B.L.003",
            bone_a="j_f_mabdn_02out_l",
            bone_b="lid.B.L.003",
            parent="Eye.L",
            is_connected=False,
            req_bones=["j_f_mabdn_02out_l", "j_f_eye_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),

        ConnectBone(
            name="eye_tracker.T.L.001",
            bone_a="j_f_mabup_02out_l",
            bone_b="lid.T.L.001",
            parent="Eye.L",
            is_connected=False,
            req_bones=["j_f_mabup_02out_l", "j_f_eye_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),

        ConnectBone(
            name="eye_tracker.T.L.002",
            bone_a="j_f_mabup_01_l",
            bone_b="lid.T.L.002",
            parent="Eye.L",
            is_connected=False,
            req_bones=["j_f_mabup_01_l", "j_f_eye_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),

        ConnectBone(
            name="eye_tracker.T.L.003",
            bone_a="j_f_mabup_03in_l",
            bone_b="lid.T.L.003",
            parent="Eye.L",
            is_connected=False,
            req_bones=["j_f_mabup_03in_l", "j_f_eye_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),
        #Glue Bones
        ConnectBone(
            name="Lower.Lid.L.Glue",
            bone_a="lid.B.L.002",
            bone_b="j_f_hoho_l",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hoho_l", "lid.B.L.002"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.1, skin_glue_tail_reparent=True),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Upper.Lid.L.Glue",
            bone_a="lid.T.L.002",
            bone_b="j_f_miken_02_l",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_miken_02_l", "lid.T.L.002"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.1, skin_glue_tail_reparent=True),
                b_collection="MCH"
            )
        ),
    ]
)  

RIGHT_EYE = BoneGroup(
    name="Eyes",
    transform_link= [
        TransformLink(target="lid.B.R.001", bone="j_f_mabdn_03in_r"),
        TransformLink(target="lid.B.R.002", bone="j_f_mabdn_01_r"),
        TransformLink(target="lid.B.R.003", bone="j_f_mabdn_02out_r"),
        TransformLink(target="lid.T.R.001", bone="j_f_mabup_02out_r"),
        TransformLink(target="lid.T.R.002", bone="j_f_mabup_01_r"),
        TransformLink(target="lid.T.R.003", bone="j_f_mabup_03in_r"),
        TransformLink(target="MCH-Eye.R", bone="j_f_eyepuru_r"),
    ],
    generators=[
        ## Skin Bone, Basicly Corner Bones for the eyes
        SkinBone(
            name="lid.T.R", 
            bone_a="j_f_mabup_02out_r", 
            mesh_restriction="eye_occlusion",
            req_bones=["j_f_mabup_02out_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=2, primary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="Head", skin_chain_falloff_spherical=[False, False, False], skin_chain_falloff=[0.0, 1.0, 0.0], skin_chain_falloff_length=True), 
                b_collection="Face (Secondary)"
                )
        ),
        SkinBone(
            name="lid.T.R.002", 
            bone_a="j_f_mabup_01_r", 
            mesh_restriction="eye_occlusion",
            req_bones=["j_f_mabup_01_r"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
                )
        ),
        SkinBone(
            name="lid.B.R", 
            bone_a="j_f_mabdn_03in_r", 
            mesh_restriction="eye_occlusion", 
            req_bones=["j_f_mabdn_03in_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=2, primary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="Head"), 
                b_collection="Face (Secondary)"
                )
        ),
        SkinBone(
            name="lid.B.R.002",
            bone_a="j_f_mabdn_01_r",
            mesh_restriction="eye_occlusion",
            req_bones=["j_f_mabdn_01_r"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
                )
        ),
        CopyBone(
            name="Eye.R",
            source_bone="j_f_eyepuru_r",
            req_bones=["j_f_eyepuru_r"],
            parent="Head",
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.face_skin_eye(),
                b_collection="Face (Primary)"
                )
        ),
        BridgeBone(
            name="lid.T.R.001",
            bone_a="lid.T.R",
            bone_b="lid.T.R.002",
            offset_factor=mathutils.Vector((0.0, -0.001, 0.001)),
            is_connected=True,  
            parent="Eye.R",
            req_bones=["lid.T.R", "lid.T.R.002"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
            )
        ),
        BridgeBone(
            name="lid.T.R.003", 
            bone_a="lid.T.R.002",
            bone_b="lid.B.R",
            offset_factor=mathutils.Vector((0.0, 0.0, 0.003)),
            is_connected=False,
            req_bones=["lid.T.R.002", "lid.B.R"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
            )
        ),
        BridgeBone(
            name="lid.B.R.001",
            bone_a="lid.B.R",
            bone_b="lid.B.R.002",
            offset_factor=mathutils.Vector((-0.002, 0.0, 0.001)),
            is_connected=True,
            parent="Eye.R",
            req_bones=["lid.B.R", "lid.B.R.002"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
            )
        ),
        BridgeBone(
            name="lid.B.R.003",
            bone_a="lid.B.R.002",
            bone_b="lid.T.R",
            offset_factor=mathutils.Vector((-0.003, -0.001, -0.003)),
            is_connected=False,
            req_bones=["lid.B.R.002", "lid.T.R"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
            )
        ),

        ConnectBone(
            name="eye_tracker.B.R.001",
            bone_a="j_f_mabdn_03in_r",
            bone_b="lid.B.R.001",
            parent="Eye.R",
            is_connected=False,
            req_bones=["j_f_mabdn_03in_r", "j_f_eye_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),
        ConnectBone(
            name="eye_tracker.B.R.002",
            bone_a="j_f_mabdn_01_r",
            bone_b="lid.B.R.002",
            parent="Eye.R",
            is_connected=False,
            req_bones=["j_f_mabdn_01_r", "j_f_eye_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),
        ConnectBone(
            name="eye_tracker.B.R.003",
            bone_a="j_f_mabdn_02out_r",
            bone_b="lid.B.R.003",
            parent="Eye.R",
            is_connected=False,
            req_bones=["j_f_mabdn_02out_r", "j_f_eye_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),
        ConnectBone(
            name="eye_tracker.T.R.001",
            bone_a="j_f_mabup_02out_r",
            bone_b="lid.T.R.001",
            parent="Eye.R",
            is_connected=False,
            req_bones=["j_f_mabup_02out_r", "j_f_eye_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),
        ConnectBone(
            name="eye_tracker.T.R.002",
            bone_a="j_f_mabup_01_r",
            bone_b="lid.T.R.002",
            parent="Eye.R",
            is_connected=False,
            req_bones=["j_f_mabup_01_r", "j_f_eye_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),
        ConnectBone(
            name="eye_tracker.T.R.003",
            bone_a="j_f_mabup_03in_r",
            bone_b="lid.T.R.003",
            parent="Eye.R",
            is_connected=False,
            req_bones=["j_f_mabup_03in_r", "j_f_eye_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),
        #Glue Bones
        ConnectBone(
            name="Lower.Lid.R.Glue",
            bone_a="lid.B.R.002",
            bone_b="j_f_hoho_r",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hoho_r", "lid.B.R.002"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.1, skin_glue_tail_reparent=True),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Upper.Lid.R.Glue",
            bone_a="lid.T.R.002",
            bone_b="j_f_miken_02_r",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_miken_02_r", "lid.T.R.002"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.1, skin_glue_tail_reparent=True),
                b_collection="MCH"
            )
        ),
    ]
)

def get_rig_module() -> RigModule:
    return RigModule(
        name="Default",
        type="Generation",
        bone_groups=[HEAD, BROW, LEFT_EYE, RIGHT_EYE],
        ui = UI_Collections([
            BoneCollection(name="Head", ui=True, color_set="Head", row_index=1, title="Head"),
            BoneCollection(name="Face (Primary)", ui=True, color_set="Face_Primary", row_index=2, title="Primary", visible=False),
            BoneCollection(name="Face (Secondary)", ui=True, color_set="Face_Secondary", row_index=2, title="Secondary", visible=False),
            BoneCollection(name="Mouth", ui=True, color_set="Torso", row_index=3, title="Mouth", visible=False),
        ])
    )

