import mathutils

from ......core.rigify.settings import UI_Collections, BoneCollection
from ......core.operations import CollectionOperation, ParentBoneOperation, PropOverrideOperation, RigifyTypeOperation, WidgetOperation, BoneRestrictionOperation
from ......core.constraints import CopyLocationConstraint, CopyScaleConstraint, LimitLocationConstraint
from ......core.drivers import TransformChannelVariable, Driver, SinglePropertyVariable
from ......core.bone_generators import ConnectBone, ExtensionBone, CenterBone, CopyBone, SkinBone, BridgeBone, OffsetBone
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify

EYES = BoneGroup(
    name="Head",
    transform_link= [
        TransformLink(target="DEF-Eye.L", bone="J_Adj_L_FaceEye"),
        TransformLink(target="DEF-Eye.R", bone="J_Adj_R_FaceEye"),
    ],
    generators=[
        #Left Eye
        CopyBone(
            name="Eye.L",
            bone_a="J_Adj_L_FaceEye",
            req_bones=["J_Adj_L_FaceEye"],
            parent="Head",
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Eye.L", rigify_type=rigify.types.face_skin_eye()),
                        CollectionOperation(time="Pre", bone_name="Eye.L", collection_name="Face (Primary)")
            ]
        ),


        ## We need to build a fake eye ring here so rigify can generate the eye controls. This is dumb and i dont know why rigify doesnt have a better soltuion
        ## I also checked what VRM to Rigify did and they spawn the rigify bse rig and edit it, they shrimply dont delete the additional eyebones. 
        ## Due to the nature of this, this will look scuffed but idc

        ExtensionBone(
            name="Eye.L.Ring_helper1",
            bone_a="Eye.L",
            parent=["Head"], 
            start="head",
            axis="Z",
            size_factor=0.4,
        ),
        ExtensionBone(
            name="Eye.L.Ring_helper2",
            bone_a="Eye.L",
            parent=["Head"], 
            start="head",
            axis="Z",
            size_factor=-0.4,
        ),
        ExtensionBone(
            name="Eye.L.Ring_helper3",
            bone_a="Eye.L",
            parent=["Head"], 
            start="head",
            axis="X",
            size_factor=0.4,
        ),
        ExtensionBone(
            name="Eye.L.Ring_helper4",
            bone_a="Eye.L",
            parent=["Head"], 
            start="head",
            axis="X",
            size_factor=-0.4,
        ),

        ConnectBone(
            name="lid.T.L",
            bone_a="Eye.L.Ring_helper4",
            bone_b="Eye.L.Ring_helper1",
            start="tail",
            end="tail",
            parent=["Eye.L"],
            req_bones=["Eye.L.Ring_helper1", "Eye.L.Ring_helper2", "Eye.L.Ring_helper3", "Eye.L.Ring_helper4"],
            operations=[
                RigifyTypeOperation(time="Pre", bone_name="lid.T.L", rigify_type=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=2, primary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="Head")),
                CollectionOperation(bone_name="lid.T.L", collection_name="Face (Primary)"),
            ]
        ),
        ConnectBone(
            name="lid.T.L.002",
            bone_a="Eye.L.Ring_helper1",
            bone_b="Eye.L.Ring_helper3",
            start="tail",
            end="tail",
            parent=["lid.T.L"],
            req_bones=["Eye.L.Ring_helper1", "Eye.L.Ring_helper2", "Eye.L.Ring_helper3", "Eye.L.Ring_helper4"],
            operations=[CollectionOperation(time="Pre", bone_name="lid.T.L.002", collection_name="Face (Secondary)")]
        ),
        ConnectBone(
            name="lid.B.L",
            bone_a="Eye.L.Ring_helper3",
            bone_b="Eye.L.Ring_helper2",
            start="tail",
            end="tail",
            parent=["Eye.L"],
            req_bones=["Eye.L.Ring_helper1", "Eye.L.Ring_helper2", "Eye.L.Ring_helper3", "Eye.L.Ring_helper4"],
            operations=[
                RigifyTypeOperation(time="Pre", bone_name="lid.B.L", rigify_type=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=2, primary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="Head")),
                CollectionOperation(bone_name="lid.B.L", collection_name="Face (Primary)"),
            ]
        ),
        ConnectBone(
            name="lid.B.L.002",
            bone_a="Eye.L.Ring_helper2",
            bone_b="Eye.L.Ring_helper4",
            start="tail",
            end="tail",
            parent=["lid.B.L"],
            req_bones=["Eye.L.Ring_helper1", "Eye.L.Ring_helper2", "Eye.L.Ring_helper3", "Eye.L.Ring_helper4"],
            operations=[CollectionOperation(time="Pre", bone_name="lid.B.L.002", collection_name="Face (Secondary)")]
        ),

        BridgeBone(
            name="lid.T.L.001",
            bone_a="lid.T.L",
            bone_b="lid.T.L.002",
            offset_factor=mathutils.Vector((0.0, -0.001, 0.001)),
            is_connected=True,  
            parent="Eye.L",
            req_bones=["lid.T.L", "lid.T.L.002"],
            operations=[CollectionOperation(time="Pre", bone_name="lid.T.L.001", collection_name="Face (Secondary)")
            ]
        ), 

        BridgeBone(
            name="lid.T.L.003", 
            bone_a="lid.T.L.002",
            bone_b="lid.B.L",
            offset_factor=mathutils.Vector((0.0, 0.0, 0.003)),
            is_connected=False,
            req_bones=["lid.T.L.002", "lid.B.L"],
            operations=[CollectionOperation(time="Pre", bone_name="lid.T.L.003", collection_name="Face (Secondary)")]
        ),
        BridgeBone(
            name="lid.B.L.001",
            bone_a="lid.B.L",
            bone_b="lid.B.L.002",
            offset_factor=mathutils.Vector((-0.002, 0.0, 0.001)),
            is_connected=True,
            parent="Eye.L",
            req_bones=["lid.B.L", "lid.B.L.002"],
            operations=[CollectionOperation(time="Pre", bone_name="lid.B.L.001", collection_name="Face (Secondary)")]
        ),

        BridgeBone(
            name="lid.B.L.003",
            bone_a="lid.B.L.002",
            bone_b="lid.T.L",
            offset_factor=mathutils.Vector((0.003, -0.001, -0.003)),
            is_connected=False,
            req_bones=["lid.B.L.002", "lid.T.L"],
            operations=[CollectionOperation(time="Pre", bone_name="lid.B.L.003", collection_name="Face (Secondary)")]
        ),






        #Right Eye 
        CopyBone(
            name="Eye.R",
            bone_a="J_Adj_R_FaceEye",
            req_bones=["J_Adj_R_FaceEye"],
            parent="Head",
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Eye.R", rigify_type=rigify.types.face_skin_eye()),
                        CollectionOperation(time="Pre", bone_name="Eye.R", collection_name="Face (Primary)")
            ]
        ),


        ## We need to build a fake eye ring here so rigify can generate the eye controls. This is dumb and i dont know why rigify doesnt have a better soltuion
        ## I also checked what VRM to Rigify did and they spawn the rigify bse rig and edit it, they shrimply dont delete the additional eyebones. 
        ## Due to the nature of this, this will look scuffed but idc

        ExtensionBone(
            name="Eye.R.Ring_helper1",
            bone_a="Eye.R",
            parent=["Head"], 
            start="head",
            axis="Z",
            size_factor=0.4,
        ),
        ExtensionBone(
            name="Eye.R.Ring_helper2",
            bone_a="Eye.R",
            parent=["Head"], 
            start="head",
            axis="Z",
            size_factor=-0.4,
        ),
        ExtensionBone(
            name="Eye.R.Ring_helper3",
            bone_a="Eye.R",
            parent=["Head"], 
            start="head",
            axis="X",
            size_factor=0.4,
        ),
        ExtensionBone(
            name="Eye.R.Ring_helper4",
            bone_a="Eye.R",
            parent=["Head"], 
            start="head",
            axis="X",
            size_factor=-0.4,
        ),

        ConnectBone(
            name="lid.T.R",
            bone_a="Eye.R.Ring_helper4",
            bone_b="Eye.R.Ring_helper1",
            start="tail",
            end="tail",
            parent=["Eye.R"],
            req_bones=["Eye.R.Ring_helper1", "Eye.R.Ring_helper2", "Eye.R.Ring_helper3", "Eye.R.Ring_helper4"],
            operations=[
                RigifyTypeOperation(time="Pre", bone_name="lid.T.R", rigify_type=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=2, primary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="Head")),
                CollectionOperation(bone_name="lid.T.R", collection_name="Face (Primary)"),
            ]
        ),
        ConnectBone(
            name="lid.T.R.002",
            bone_a="Eye.R.Ring_helper1",
            bone_b="Eye.R.Ring_helper3",
            start="tail",
            end="tail",
            parent=["lid.T.R"],
            req_bones=["Eye.R.Ring_helper1", "Eye.R.Ring_helper2", "Eye.R.Ring_helper3", "Eye.R.Ring_helper4"],
            operations=[CollectionOperation(time="Pre", bone_name="lid.T.R.002", collection_name="Face (Secondary)")]
        ),
        ConnectBone(
            name="lid.B.R",
            bone_a="Eye.R.Ring_helper3",
            bone_b="Eye.R.Ring_helper2",
            start="tail",
            end="tail",
            parent=["Eye.R"],
            req_bones=["Eye.R.Ring_helper1", "Eye.R.Ring_helper2", "Eye.R.Ring_helper3", "Eye.R.Ring_helper4"],
            operations=[
                RigifyTypeOperation(time="Pre", bone_name="lid.B.R", rigify_type=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=2, primary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="Head")),
                CollectionOperation(bone_name="lid.B.R", collection_name="Face (Primary)"),
            ]
        ),
        ConnectBone(
            name="lid.B.R.002",
            bone_a="Eye.R.Ring_helper2",
            bone_b="Eye.R.Ring_helper4",
            start="tail",
            end="tail",
            parent=["lid.B.R"],
            req_bones=["Eye.R.Ring_helper1", "Eye.R.Ring_helper2", "Eye.R.Ring_helper3", "Eye.R.Ring_helper4"],
            operations=[CollectionOperation(time="Pre", bone_name="lid.B.R.002", collection_name="Face (Secondary)")]
        ),

        BridgeBone(
            name="lid.T.R.001",
            bone_a="lid.T.R",
            bone_b="lid.T.R.002",
            offset_factor=mathutils.Vector((0.0, -0.001, 0.001)),
            is_connected=True,  
            parent="Eye.R",
            req_bones=["lid.T.R", "lid.T.R.002"],
            operations=[CollectionOperation(time="Pre", bone_name="lid.T.R.001", collection_name="Face (Secondary)")
            ]
        ), 

        BridgeBone(
            name="lid.T.R.003", 
            bone_a="lid.T.R.002",
            bone_b="lid.B.R",
            offset_factor=mathutils.Vector((0.0, 0.0, 0.003)),
            is_connected=False,
            req_bones=["lid.T.R.002", "lid.B.R"],
            operations=[CollectionOperation(time="Pre", bone_name="lid.T.R.003", collection_name="Face (Secondary)")]
        ),
        BridgeBone(
            name="lid.B.R.001",
            bone_a="lid.B.R",
            bone_b="lid.B.R.002",
            offset_factor=mathutils.Vector((-0.002, 0.0, 0.001)),
            is_connected=True,
            parent="Eye.R",
            req_bones=["lid.B.R", "lid.B.R.002"],
            operations=[CollectionOperation(time="Pre", bone_name="lid.B.R.001", collection_name="Face (Secondary)")]
        ),

        BridgeBone(
            name="lid.B.R.003",
            bone_a="lid.B.R.002",
            bone_b="lid.T.R",
            offset_factor=mathutils.Vector((0.003, -0.001, -0.003)),
            is_connected=False,
            req_bones=["lid.B.R.002", "lid.T.R"],
            operations=[CollectionOperation(time="Pre", bone_name="lid.B.R.003", collection_name="Face (Secondary)")]
        ),
    ]
        
)

def get_rig_module() -> RigModule:
    return RigModule(
        name="VRM-Default",
        type="Generation",
        bone_groups=[EYES],
        ui_collections = UI_Collections([
            BoneCollection(name="Face (Primary)", ui=True, color_set="Face_Primary", row_index=1, title="Face (Primary)", visible=True),
        ]),
        operations =[
            BoneRestrictionOperation(time="Post", bone_name="Eye_master.L", hide_select=True, hide=True,),
            BoneRestrictionOperation(time="Post", bone_name="Eye_master.R", hide_select=True, hide=True,),

            BoneRestrictionOperation(time="Post", bone_name="lid.T.L", hide_select=True, hide=True,),
            BoneRestrictionOperation(time="Post", bone_name="lid.T.L.001", hide_select=True, hide=True,),
            BoneRestrictionOperation(time="Post", bone_name="lid.T.L.002", hide_select=True, hide=True,),
            BoneRestrictionOperation(time="Post", bone_name="lid.T.L.003", hide_select=True, hide=True,),
            BoneRestrictionOperation(time="Post", bone_name="lid.B.L", hide_select=True, hide=True,),
            BoneRestrictionOperation(time="Post", bone_name="lid.B.L.001", hide_select=True, hide=True,),
            BoneRestrictionOperation(time="Post", bone_name="lid.B.L.002", hide_select=True, hide=True,),
            BoneRestrictionOperation(time="Post", bone_name="lid.B.L.003", hide_select=True, hide=True,),

            BoneRestrictionOperation(time="Post", bone_name="lid.T.R", hide_select=True, hide=True,),
            BoneRestrictionOperation(time="Post", bone_name="lid.T.R.001", hide_select=True, hide=True,),
            BoneRestrictionOperation(time="Post", bone_name="lid.T.R.002", hide_select=True, hide=True,),
            BoneRestrictionOperation(time="Post", bone_name="lid.T.R.003", hide_select=True, hide=True,),
            BoneRestrictionOperation(time="Post", bone_name="lid.B.R", hide_select=True, hide=True,),
            BoneRestrictionOperation(time="Post", bone_name="lid.B.R.001", hide_select=True, hide=True,),
            BoneRestrictionOperation(time="Post", bone_name="lid.B.R.002", hide_select=True, hide=True,),
            BoneRestrictionOperation(time="Post", bone_name="lid.B.R.003", hide_select=True, hide=True,),
        ]
    )