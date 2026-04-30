import mathutils

from ......core.rigify.settings import UI_Collections, BoneCollection
from ......core.operations import CollectionOperation, ParentBoneOperation, RigifyTypeOperation
from ......core.generators import ConnectBone, ExtensionBone, CenterBone, CopyBone, SkinBone, BridgeBone
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify

MOUTH_MANUAL = BoneGroup(
    name="Mouth Manual",
    #I genuinely think this is probably the dumbest addition to the rigging system but here we are. Some people just hate nice things. - Oats
    transform_link=[
        TransformLink(target="DEF-Lip.T.R", bone="j_f_ulip_01_r"),
        TransformLink(target="DEF-Lip.T.R.001", bone="j_f_umlip_01_r"),
        TransformLink(target="DEF-Lip.T.R.002", bone="j_f_uslip_r"),
        TransformLink(target="DEF-Lip.B.R", bone="j_f_dlip_01_r"),
        TransformLink(target="DEF-Lip.B.R.001", bone="j_f_dmlip_01_r"),
        TransformLink(target="DEF-Lip.B.R.002", bone="j_f_dslip_r"),
        # TransformLink(target="DEF-Lip.T.L.001", bone="j_f_ulip_01_l"),
        # TransformLink(target="DEF-Lip.T.L.002", bone="j_f_umlip_01_l"),
        # TransformLink(target="DEF-Lip.T.L.003", bone="j_f_uslip_l"),
        # TransformLink(target="DEF-Lip.B.L.001", bone="j_f_dlip_01_l"),
        # TransformLink(target="DEF-Lip.B.L.002", bone="j_f_dmlip_01_l"),
        # TransformLink(target="DEF-Lip.B.L.003", bone="j_f_dslip_l"),
        # TransformLink(target="Lip.T.L.001", bone="j_f_ulip_02_l"),
        # TransformLink(target="Lip.T.L.002", bone="j_f_umlip_02_l"),
        # TransformLink(target="Lip.T.R.001", bone="j_f_ulip_02_r"),
        # TransformLink(target="Lip.T.R.002", bone="j_f_umlip_02_r"),
        # TransformLink(target="Lip.B.L.001", bone="j_f_dlip_02_l"),
        # TransformLink(target="Lip.B.L.002", bone="j_f_dmlip_02_l"),
        # TransformLink(target="Lip.B.R.001", bone="j_f_dlip_02_r"),
        # TransformLink(target="Lip.B.R.002", bone="j_f_dmlip_02_r"),
        # TransformLink(target="DEF-Teeth.T", bone="j_f_hagukiup"),
        # TransformLink(target="DEF-Teeth.B", bone="j_f_hagukidn"),
        # TransformLink(target="DEF-Tongue", bone="j_f_bero_01"),
        # TransformLink(target="DEF-Tongue.001", bone="j_f_bero_02"),
        # TransformLink(target="DEF-Tongue.002", bone="j_f_bero_03"),
    ],
    generators=[
        #Jaw
        CenterBone(
            name="jaw_ref",
            ref_bones=["j_f_dlip_01_r", "j_f_dlip_01_l"],
            axis="Y",
            inverted=False,
            parent="Head",
            req_bones=["j_f_dlip_01_r", "j_f_dlip_01_l"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="jaw_ref", collection_name="MCH")
                        ]
        ),
        ConnectBone(
            name="Jaw",
            bone_a="j_f_ago",
            bone_b="jaw_master_ref",
            parent=["Head", "j_kao"],
            req_bones=["j_f_ago", "jaw_ref"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="jaw_master", rigify_type=rigify.types.basic_super_copy(widget_type="jaw")),
                        CollectionOperation(time="Pre", bone_name="jaw_master", collection_name="Face (Primary)")
            ]
        ),
        #Lips Right
        ExtensionBone(
            name="Lip.T.R",
            bone_a="j_f_ulip_01_r",
            parent=["Head", "j_kao"],
            start="head",
            size_factor=0.5,
            axis="Y",
            axis_type="local",
            req_bones=["j_f_ulip_01_r"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Lip.T.R", rigify_type=rigify.types.basic_super_copy(widget_type="circle")),
                        CollectionOperation(time="Pre", bone_name="Lip.T.R", collection_name="Face (Primary)")
                        ]
        ),
        ExtensionBone(
            name="Lip.T.R.001",
            bone_a="j_f_umlip_01_r",
            parent=["Head", "j_kao"],
            start="head",
            size_factor=0.5,
            axis="Y",
            axis_type="local",
            req_bones=["j_f_umlip_01_r"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Lip.T.R.001", rigify_type=rigify.types.basic_super_copy(widget_type="circle")),
                        CollectionOperation(time="Pre", bone_name="Lip.T.R.001", collection_name="Face (Secondary)")
                        ]
        ),
        ExtensionBone(
            name="Lip.T.R.002",
            bone_a="j_f_uslip_r",
            parent=["Head", "j_kao"],
            start="head",
            size_factor=0.5,
            axis="Y",
            axis_type="local",
            req_bones=["j_f_uslip_r"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Lip.T.R.002", rigify_type=rigify.types.basic_super_copy(widget_type="circle")),
                        CollectionOperation(time="Pre", bone_name="Lip.T.R.002", collection_name="Face (Primary)")
                        ]
        ),
        ExtensionBone(
            name="Lip.B.R",
            bone_a="j_f_dlip_01_r",
            parent=["Head", "j_kao"],
            start="head",
            size_factor=0.5,
            axis="Y",
            axis_type="local",
            req_bones=["j_f_dlip_01_r"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Lip.B.R", rigify_type=rigify.types.basic_super_copy(widget_type="circle")),
                        CollectionOperation(time="Pre", bone_name="Lip.B.R", collection_name="Face (Primary)")
                        ]
        ),
        ExtensionBone(
            name="Lip.B.R.001",
            bone_a="j_f_dmlip_01_r",
            parent=["Head", "j_kao"],
            start="head",
            size_factor=0.5,
            axis="Y",
            axis_type="local",
            req_bones=["j_f_dmlip_01_r"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Lip.B.R.001", rigify_type=rigify.types.basic_super_copy(widget_type="circle")),
                        CollectionOperation(time="Pre", bone_name="Lip.B.R.001", collection_name="Face (Secondary)")
                        ]
        ),
        ExtensionBone(
            name="Lip.B.R.002",
            bone_a="j_f_dslip_r",
            parent=["Head", "j_kao"],
            start="head",
            size_factor=0.5,
            axis="Y",
            axis_type="local",
            req_bones=["j_f_dslip_r"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Lip.B.R.002", rigify_type=rigify.types.basic_super_copy(widget_type="circle")),
                        CollectionOperation(time="Pre", bone_name="Lip.B.R.002", collection_name="Face (Primary)")
                        ]
        ),
    ]
)
def get_rig_module() -> RigModule:
    return RigModule(
        name="Manual",
        type="Generation",
        bone_groups=[MOUTH_MANUAL],
        ui = UI_Collections([
            BoneCollection(name="Face (Primary)", ui=True, color_set="Face_Primary", row_index=0, title="Face (Primary)", visible=True),
            BoneCollection(name="Face (Secondary)", ui=True, color_set="Face_Secondary", row_index=0, title="Face (Secondary)", visible=False),
            BoneCollection(name="Face (Misc)", ui=True, color_set="Face_Secondary", row_index=1, title="Face (Misc)", visible=False),
        ])
    )