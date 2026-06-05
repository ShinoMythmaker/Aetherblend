import mathutils

from ......core.rigify.settings import UI_Collections, BoneCollection
from ......core.operations import CollectionOperation, ParentBoneOperation, PropOverrideOperation, RigifyTypeOperation, WidgetOperation, BoneRestrictionOperation, ConstraintOperation, DriverOperation, PoseBoneOperation
from ......core.constraints import CopyLocationConstraint, CopyScaleConstraint, LimitLocationConstraint
from ......core.drivers import TransformChannelVariable, Driver, SinglePropertyVariable
from ......core.bone_generators import ConnectBone, ExtensionBone, CenterBone, CopyBone, SkinBone, BridgeBone, OffsetBone
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify

HEAD = BoneGroup(
    name="Head",
    transform_link= [
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
    ],
    generators=[
        #Cheek Right
        ConnectBone(
            name="Cheek.B.R",
            bone_a="j_f_shoho_r",
            bone_b="j_kao",
            parent="Head",
            req_bones=["j_f_shoho_r", "j_kao"],
            operations=[ RigifyTypeOperation(time="Pre", bone_name="Cheek.B.R", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Cheek.B.R", collection_name="Face (Primary)")
            ]
         ),
        ConnectBone(
            name="Cheek.B.R.001",
            bone_a="j_f_dhoho_r",
            bone_b="j_kao",
            parent="Head",
            req_bones=["j_f_dhoho_r", "j_kao"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Cheek.B.R.001", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Cheek.B.R.001", collection_name="Face (Secondary)")
            ]   
        ),
        ConnectBone(
            name="Cheek.T.R",
            bone_a="j_f_hoho_r",
            bone_b="j_kao",
            parent="Head",
            req_bones=["j_f_hoho_r", "j_kao"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Cheek.T.R", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Cheek.T.R", collection_name="Face (Primary)")
            ]         
        ),
        ConnectBone(
            name="Cheek.T.R.001",
            bone_a="j_f_dmemoto_r",
            bone_b="j_kao",
            parent="Head",
            req_bones=["j_f_dmemoto_r", "j_kao"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Cheek.T.R.001", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Cheek.T.R.001", collection_name="Face (Secondary)")
            ]  
        ),
        #Cheek Left
        ConnectBone(
            name="Cheek.B.L",
            bone_a="j_f_shoho_l",
            bone_b="j_kao",
            parent="Head",
            req_bones=["j_f_shoho_l", "j_kao"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Cheek.B.L", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Cheek.B.L", collection_name="Face (Primary)")
            ]
        ),
        ConnectBone(
            name="Cheek.B.L.001",
            bone_a="j_f_dhoho_l",
            bone_b="j_kao",
            parent="Head",
            req_bones=["j_f_dhoho_l", "j_kao"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Cheek.B.L.001", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Cheek.B.L.001", collection_name="Face (Secondary)")
            ]            
        ),
        ConnectBone(
            name="Cheek.T.L",
            bone_a="j_f_hoho_l",
            bone_b="j_kao",
            parent="Head",
            req_bones=["j_f_hoho_l", "j_kao"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Cheek.T.L", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Cheek.T.L", collection_name="Face (Primary)")
            ]       
        ),
        ConnectBone(
            name="Cheek.T.L.001",
            bone_a="j_f_dmemoto_l",
            bone_b="j_kao",
            parent="Head",
            req_bones=["j_f_dmemoto_l", "j_kao"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Cheek.T.L.001", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Cheek.T.L.001", collection_name="Face (Secondary)")
                        ]
        ),
        #Nose Centre
        ConnectBone(
            name="Nose",
            bone_a="j_f_uhana",
            bone_b="j_kao",
            parent="Head",
            req_bones=["j_f_uhana", "j_kao"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Nose", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Nose", collection_name="Face (Primary)")
            ]     
        ),
        #Nose Right
        ConnectBone(
            name="Nose.R",
            bone_a="j_f_dmiken_r",
            bone_b="j_kao",
            parent="Head",
            req_bones=["j_f_dmiken_r", "j_kao"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Nose.R", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Nose.R", collection_name="Face (Primary)")
            ] 
        ),
        ConnectBone(
            name="Nostril.R",
            bone_a="j_f_hana_r",
            bone_b="j_kao",
            parent="Head",
            req_bones=["j_f_hana_r", "j_kao"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Nostril.R", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Nostril.R", collection_name="Face (Primary)")
            ]    
        ),
        #Nose Left
        ConnectBone(
            name="Nose.L",
            bone_a="j_f_dmiken_l",
            bone_b="j_kao",
            parent="Head",
            req_bones=["j_f_dmiken_l", "j_kao"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Nose.L", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Nose.L", collection_name="Face (Primary)")
            ]
        ),
        ConnectBone(
            name="Nostril.L",
            bone_a="j_f_hana_l",
            bone_b="j_kao",
            parent="Head",
            req_bones=["j_f_hana_l", "j_kao"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Nostril.L", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head")),
                        CollectionOperation(time="Pre", bone_name="Nostril.L", collection_name="Face (Primary)")
            ]  
        ),
        
        #Anchor
        ExtensionBone(
            name="Face.Suppressor",
            bone_a="j_kao",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            size_factor=1.0,
            parent="Head",
            req_bones=["j_kao"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Face.Suppressor", rigify_type=rigify.types.skin_anchor(skin_anchor_hide=True)),
                        CollectionOperation(time="Pre", bone_name="Face.Suppressor", collection_name="MCH")
                        ]
        ),
        #Nose Glue
        ConnectBone(
            name="Nostril.Glue.R",
            bone_a="j_f_hana_r",
            bone_b="j_f_uhana",
            parent="Head",
            req_bones=["j_f_hana_r", "j_f_uhana"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Nostril.Glue.R", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Nostril.Glue.R", collection_name="MCH")
                        ]
        ),
        ConnectBone(
            name="Nostril.Glue.L",
            bone_a="j_f_hana_l",
            bone_b="j_f_uhana",
            parent="Head",
            req_bones=["j_f_hana_l", "j_f_uhana"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Nostril.Glue.L", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Nostril.Glue.L", collection_name="MCH")
                        ]
        ),
        ConnectBone(
            name="Nostril.Glue.R.001",
            bone_a="Cheek.T.R.001", 
            bone_b="Nostril.R",
            parent="Head",
            req_bones=["Cheek.T.R.001", "Nostril.R"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Nostril.Glue.R.001", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Nostril.Glue.R.001", collection_name="MCH")
                        ]
        ),
        ConnectBone(
            name="Nostril.Glue.L.001",
            bone_a="Cheek.T.L.001", 
            bone_b="Nostril.L",
            parent="Head",
            req_bones=["Cheek.T.L.001", "Nostril.L"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Nostril.Glue.L.001", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Nostril.Glue.L.001", collection_name="MCH")
            ]
        ),
        #Cheek Glue Bones Right
        ConnectBone(
            name="Cheek.B.R.glue",
            bone_a="j_f_dhoho_r",
            bone_b="j_f_shoho_r",
            parent="Head",
            req_bones=["j_f_shoho_r", "j_f_dhoho_r"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Cheek.B.R.glue", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Cheek.B.R.glue", collection_name="MCH")
            ]
        ),
        ConnectBone(
            name="Cheek.T.R.glue",
            bone_a="j_f_dhoho_r",
            bone_b="j_f_hoho_r",
            parent="Head",
            req_bones=["j_f_hoho_r", "j_f_dhoho_r"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Cheek.T.R.glue", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Cheek.T.R.glue", collection_name="MCH")
            ]
        ),
        #Cheek Glue Bones Left
        ConnectBone(
            name="Cheek.B.L.glue",
            bone_a="j_f_dhoho_l",
            bone_b="j_f_shoho_l",
            parent="Head",
            req_bones=["j_f_shoho_l", "j_f_dhoho_l"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Cheek.B.L.glue", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Cheek.B.L.glue", collection_name="MCH")
            ]
        ),
        ConnectBone(
            name="Cheek.T.L.glue",
            bone_a="j_f_dhoho_l",
            bone_b="j_f_hoho_l",
            parent="Head",
            req_bones=["j_f_hoho_l", "j_f_dhoho_l"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Cheek.T.L.glue", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Cheek.T.L.glue", collection_name="MCH")
            ]
        ),
        #Nostril Glue Bones
        ConnectBone(
            name="Nostril.Glue.R",
            bone_a="j_f_hana_r",
            bone_b="j_f_uhana",
            parent="Head",
            req_bones=["j_f_hana_r", "j_f_uhana"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Nostril.Glue.R", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Nostril.Glue.R", collection_name="MCH")
            ]
        ),
        ConnectBone(
            name="Nostril.Glue.L",
            bone_a="j_f_hana_l",
            bone_b="j_f_uhana",
            parent="Head",
            req_bones=["j_f_hana_l", "j_f_uhana"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Nostril.Glue.L", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Nostril.Glue.L", collection_name="MCH")
            ]
        ),
        ConnectBone(
            name="Nostril.Glue.R.001",
            bone_a="Cheek.T.R.001", 
            bone_b="Nostril.R",
            parent="Head",
            req_bones=["Cheek.T.R.001", "Nostril.R"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Nostril.Glue.R.001", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Nostril.Glue.R.001", collection_name="MCH")
            ]
        ),
        ConnectBone(
            name="Nostril.Glue.L.001",
            bone_a="Cheek.T.L.001", 
            bone_b="Nostril.L",
            parent="Head",
            req_bones=["Cheek.T.L.001", "Nostril.L"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Nostril.Glue.L.001", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5)),
                        CollectionOperation(time="Pre", bone_name="Nostril.Glue.L.001", collection_name="MCH")
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
            parent="Head",
            req_bones=["j_f_mayu_r", "j_f_mmayu_r",],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Brow.R", rigify_type=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, skin_control_orientation_bone="Head", skin_chain_falloff_length=True, primary_layer_extra="Face (Primary)")),
                        CollectionOperation(time="Pre", bone_name="Brow.R", collection_name="Face (Secondary)")
            ]
        ),
        ConnectBone(
            name="Brow.R.001",
            bone_a="j_f_mmayu_r",
            bone_b="j_f_miken_01_r",
            parent="Brow.R",
            is_connected=True,
            req_bones=["j_f_mmayu_r", "j_f_miken_01_r"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="Brow.R.001", collection_name="Face (Primary)")
            ]
        ),
        ConnectBone(
            name="Brow.R.002",
            bone_a="j_f_miken_01_r",
            bone_b="j_f_miken_02_r",
            parent="Brow.R.001",
            is_connected=True,
            req_bones=["j_f_miken_01_r", "j_f_miken_02_r"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="Brow.R.002", collection_name="Face (Primary)")
            ]
        ),
        ExtensionBone(
            name="Brow.R.003",
            bone_a="Brow.R.002",
            axis_type="local",
            axis="Y",
            parent="Brow.R.002",
            is_connected=True,
            req_bones=["j_f_miken_02_r"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="Brow.R.003", collection_name="Face (Primary)")
            ]
        ),
        ConnectBone(
            name="Brow.L",
            bone_a="j_f_mayu_l",
            bone_b="j_f_mmayu_l",
            parent="Head",
            req_bones=["j_f_mayu_l", "j_f_mmayu_l",],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Brow.L", rigify_type=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, skin_control_orientation_bone="Head", skin_chain_falloff_length=True, primary_layer_extra="Face (Primary)")),
                        CollectionOperation(time="Pre", bone_name="Brow.L", collection_name="Face (Secondary)")
            ]
        ),
        ConnectBone(
            name="Brow.L.001",
            bone_a="j_f_mmayu_l",
            bone_b="j_f_miken_01_l",
            parent="Brow.L",
            is_connected=True,
            req_bones=["j_f_mmayu_l", "j_f_miken_01_l"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="Brow.L.001", collection_name="Face (Primary)")
            ]
        ),
        ConnectBone(
            name="Brow.L.002",
            bone_a="j_f_miken_01_l",
            bone_b="j_f_miken_02_l",
            parent="Brow.L.001",
            is_connected=True,
            req_bones=["j_f_miken_01_l", "j_f_miken_02_l"],
            operations=[
                        CollectionOperation(time="Pre", bone_name="Brow.L.002", collection_name="Face (Primary)")
            ]
        ),
        ExtensionBone(
            name="Brow.L.003",
            bone_a="Brow.L.002",
            axis_type="local",
            axis="Y",
            parent="Brow.L.002",
            is_connected=True,
            req_bones=["j_f_miken_02_l"],
            operations=[
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
            data_key="eye_occlusion",
            req_bones=["j_f_mabup_02out_l"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="lid.T.L", rigify_type=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=2, primary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="Head", skin_chain_falloff_spherical=[False, False, False], skin_chain_falloff=[0.0, 1.0, 0.0], skin_chain_falloff_length=True)),
                         CollectionOperation(time="Pre", bone_name="lid.T.L", collection_name="Face (Secondary)")
            ]
        ),
        SkinBone(
            name="lid.T.L.002", 
            bone_a="j_f_mabup_01_l", 
            data_key="eye_occlusion",
            req_bones=["j_f_mabup_01_l"],
            operations=[CollectionOperation(time="Pre", bone_name="lid.T.L.002", collection_name="Face (Secondary)")]
        ),
        SkinBone(
            name="lid.B.L", 
            bone_a="j_f_mabdn_03in_l", 
            data_key="eye_occlusion", 
            req_bones=["j_f_mabdn_03in_l"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="lid.B.L", rigify_type=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=2, primary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="Head")),
                         CollectionOperation(time="Pre", bone_name="lid.B.L", collection_name="Face (Secondary)")
            ]
        ),
        SkinBone(
            name="lid.B.L.002", 
            bone_a="j_f_mabdn_01_l", 
            data_key="eye_occlusion",
            req_bones=["j_f_mabdn_01_l"], 
            operations=[CollectionOperation(time="Pre", bone_name="lid.B.L.002", collection_name="Face (Secondary)")]
            
        ),
        CopyBone(
            name="Eye.L",
            source_bone="j_f_eyepuru_l",
            req_bones=["j_f_eyepuru_l"],
            parent="Head",
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Eye.L", rigify_type=rigify.types.face_skin_eye()),
                        CollectionOperation(time="Pre", bone_name="Eye.L", collection_name="Face (Primary)")
            ]
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
        ConnectBone(
            name="eye_tracker.B.L.001",
            bone_a="j_f_mabdn_03in_l",
            bone_b="lid.B.L.001",
            parent="Eye.L",
            is_connected=False,
            req_bones=["j_f_mabdn_03in_l", "j_f_eye_l"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="eye_tracker.B.L.001", rigify_type=rigify.types.skin_basic_chain()),
                        CollectionOperation(time="Pre", bone_name="eye_tracker.B.L.001", collection_name="Face")]
        ),

        ConnectBone(
            name="eye_tracker.B.L.002",
            bone_a="j_f_mabdn_01_l",
            bone_b="lid.B.L.002",
            parent="Eye.L",
            is_connected=False,
            req_bones=["j_f_mabdn_01_l", "j_f_eye_l"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="eye_tracker.B.L.002", rigify_type=rigify.types.skin_basic_chain()),
                        CollectionOperation(time="Pre", bone_name="eye_tracker.B.L.002", collection_name="Face")
            ]
        ),

        ConnectBone(
            name="eye_tracker.B.L.003",
            bone_a="j_f_mabdn_02out_l",
            bone_b="lid.B.L.003",
            parent="Eye.L",
            is_connected=False,
            req_bones=["j_f_mabdn_02out_l", "j_f_eye_l"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="eye_tracker.B.L.003", rigify_type=rigify.types.skin_basic_chain()),
                        CollectionOperation(time="Pre", bone_name="eye_tracker.B.L.003", collection_name="Face")
            ]
        ),

        ConnectBone(
            name="eye_tracker.T.L.001",
            bone_a="j_f_mabup_02out_l",
            bone_b="lid.T.L.001",
            parent="Eye.L",
            is_connected=False,
            req_bones=["j_f_mabup_02out_l", "j_f_eye_l"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="eye_tracker.T.L.001", rigify_type=rigify.types.skin_basic_chain()),
                        CollectionOperation(time="Pre", bone_name="eye_tracker.T.L.001", collection_name="Face")
            ]
        ),

        ConnectBone(
            name="eye_tracker.T.L.002",
            bone_a="j_f_mabup_01_l",
            bone_b="lid.T.L.002",
            parent="Eye.L",
            is_connected=False,
            req_bones=["j_f_mabup_01_l", "j_f_eye_l"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="eye_tracker.T.L.002", rigify_type=rigify.types.skin_basic_chain()),
                        CollectionOperation(time="Pre", bone_name="eye_tracker.T.L.002", collection_name="Face")
            ]
        ),

        ConnectBone(
            name="eye_tracker.T.L.003",
            bone_a="j_f_mabup_03in_l",
            bone_b="lid.T.L.003",
            parent="Eye.L",
            is_connected=False,
            req_bones=["j_f_mabup_03in_l", "j_f_eye_l"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="eye_tracker.T.L.003", rigify_type=rigify.types.skin_basic_chain()),
                        CollectionOperation(time="Pre", bone_name="eye_tracker.T.L.003", collection_name="Face")
            ]
        ),
        #Glue Bones
        ConnectBone(
            name="Lower.Lid.L.Glue",
            bone_a="lid.B.L.002",
            bone_b="j_f_hoho_l",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hoho_l", "lid.B.L.002"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Lower.Lid.L.Glue", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.1, skin_glue_tail_reparent=True)),
                        CollectionOperation(time="Pre", bone_name="Lower.Lid.L.Glue", collection_name="MCH")
            ]    
        ),
        ConnectBone(
            name="Upper.Lid.L.Glue",
            bone_a="lid.T.L.002",
            bone_b="j_f_miken_02_l",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_miken_02_l", "lid.T.L.002"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Upper.Lid.L.Glue", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.1, skin_glue_tail_reparent=True)),
                        CollectionOperation(time="Pre", bone_name="Upper.Lid.L.Glue", collection_name="MCH")
            ]
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
        ## Skin Bone, Basically Corner Bones for the eyes
        SkinBone(
            name="lid.T.R", 
            bone_a="j_f_mabup_02out_r", 
            data_key="eye_occlusion",
            req_bones=["j_f_mabup_02out_r"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="lid.T.R", rigify_type=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=2, primary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="Head", skin_chain_falloff_spherical=[False, False, False], skin_chain_falloff=[0.0, 1.0, 0.0], skin_chain_falloff_length=True)), 
                        CollectionOperation(time="Pre", bone_name="lid.T.R", collection_name="Face (Secondary)")
            ]
        ),
        SkinBone(
            name="lid.T.R.002", 
            bone_a="j_f_mabup_01_r", 
            data_key="eye_occlusion",
            req_bones=["j_f_mabup_01_r"],
            operations=[CollectionOperation(time="Pre", bone_name="lid.T.R.002", collection_name="Face (Secondary)")]
        ),
        SkinBone(
            name="lid.B.R", 
            bone_a="j_f_mabdn_03in_r", 
            data_key="eye_occlusion", 
            req_bones=["j_f_mabdn_03in_r"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="lid.B.R", rigify_type=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=2, primary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="Head")), 
                        CollectionOperation(time="Pre", bone_name="lid.B.R", collection_name="Face (Secondary)")]
        ),
        SkinBone(
            name="lid.B.R.002",
            bone_a="j_f_mabdn_01_r",
            data_key="eye_occlusion",
            req_bones=["j_f_mabdn_01_r"],
            operations=[CollectionOperation(time="Pre", bone_name="lid.B.R.002", collection_name="Face (Secondary)")]
        ),
        CopyBone(
            name="Eye.R",
            source_bone="j_f_eyepuru_r",
            req_bones=["j_f_eyepuru_r"],
            parent="Head",
            operations=[RigifyTypeOperation(time="Pre", bone_name="Eye.R", rigify_type=rigify.types.face_skin_eye()), 
                        CollectionOperation(time="Pre", bone_name="Eye.R", collection_name="Face (Primary)")
            ]
        ),
        BridgeBone(
            name="lid.T.R.001",
            bone_a="lid.T.R",
            bone_b="lid.T.R.002",
            offset_factor=mathutils.Vector((0.0, -0.001, 0.001)),
            is_connected=True,  
            parent="Eye.R",
            req_bones=["lid.T.R", "lid.T.R.002"],
            operations=[CollectionOperation(time="Pre", bone_name="lid.T.R.001", collection_name="Face (Secondary)")]
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
            offset_factor=mathutils.Vector((0.002, 0.0, 0.001)),
            is_connected=True,
            parent="Eye.R",
            req_bones=["lid.B.R", "lid.B.R.002"],
            operations=[CollectionOperation(time="Pre", bone_name="lid.B.R.001", collection_name="Face (Secondary)")]
        ),
        BridgeBone(
            name="lid.B.R.003",
            bone_a="lid.B.R.002",
            bone_b="lid.T.R",
            offset_factor=mathutils.Vector((-0.003, -0.001, -0.003)),
            is_connected=False,
            req_bones=["lid.B.R.002", "lid.T.R"],
            operations=[CollectionOperation(time="Pre", bone_name="lid.B.R.003", collection_name="Face (Secondary)")]
        ),
        ConnectBone(
            name="eye_tracker.B.R.001",
            bone_a="j_f_mabdn_03in_r",
            bone_b="lid.B.R.001",
            parent="Eye.R",
            is_connected=False,
            req_bones=["j_f_mabdn_03in_r", "j_f_eye_r"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="eye_tracker.B.R.001", rigify_type=rigify.types.skin_basic_chain()),
                        CollectionOperation(time="Pre", bone_name="eye_tracker.B.R.001", collection_name="Face")
            ]
        ),
        ConnectBone(
            name="eye_tracker.B.R.002",
            bone_a="j_f_mabdn_01_r",
            bone_b="lid.B.R.002",
            parent="Eye.R",
            is_connected=False,
            req_bones=["j_f_mabdn_01_r", "j_f_eye_r"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="eye_tracker.B.R.002", rigify_type=rigify.types.skin_basic_chain()),
                        CollectionOperation(time="Pre", bone_name="eye_tracker.B.R.002", collection_name="Face")
            ]
        ),
        ConnectBone(
            name="eye_tracker.B.R.003",
            bone_a="j_f_mabdn_02out_r",
            bone_b="lid.B.R.003",
            parent="Eye.R",
            is_connected=False,
            req_bones=["j_f_mabdn_02out_r", "j_f_eye_r"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="eye_tracker.B.R.003", rigify_type=rigify.types.skin_basic_chain()),
                        CollectionOperation(time="Pre", bone_name="eye_tracker.B.R.003", collection_name="Face")
            ]
        ),
        ConnectBone(
            name="eye_tracker.T.R.001",
            bone_a="j_f_mabup_02out_r",
            bone_b="lid.T.R.001",
            parent="Eye.R",
            is_connected=False,
            req_bones=["j_f_mabup_02out_r", "j_f_eye_r"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="eye_tracker.T.R.001", rigify_type=rigify.types.skin_basic_chain()),
                        CollectionOperation(time="Pre", bone_name="eye_tracker.T.R.001", collection_name="Face")
            ]
        ),
        ConnectBone(
            name="eye_tracker.T.R.002",
            bone_a="j_f_mabup_01_r",
            bone_b="lid.T.R.002",
            parent="Eye.R",
            is_connected=False,
            req_bones=["j_f_mabup_01_r", "j_f_eye_r"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="eye_tracker.T.R.002", rigify_type=rigify.types.skin_basic_chain()),
                        CollectionOperation(time="Pre", bone_name="eye_tracker.T.R.002", collection_name="Face")
            ]
        ),
        ConnectBone(
            name="eye_tracker.T.R.003",
            bone_a="j_f_mabup_03in_r",
            bone_b="lid.T.R.003",
            parent="Eye.R",
            is_connected=False,
            req_bones=["j_f_mabup_03in_r", "j_f_eye_r"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="eye_tracker.T.R.003", rigify_type=rigify.types.skin_basic_chain()),
                        CollectionOperation(time="Pre", bone_name="eye_tracker.T.R.003", collection_name="Face")
            ]
        ),
        #Glue Bones
        ConnectBone(
            name="Lower.Lid.R.Glue",
            bone_a="lid.B.R.002",
            bone_b="j_f_hoho_r",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hoho_r", "lid.B.R.002"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Lower.Lid.R.Glue", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.1, skin_glue_tail_reparent=True)),
                        CollectionOperation(time="Pre", bone_name="Lower.Lid.R.Glue", collection_name="MCH")]
        ),
        ConnectBone(
            name="Upper.Lid.R.Glue",
            bone_a="lid.T.R.002",
            bone_b="j_f_miken_02_r",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_miken_02_r", "lid.T.R.002"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="Upper.Lid.R.Glue", rigify_type=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.1, skin_glue_tail_reparent=True)),
                        CollectionOperation(time="Pre", bone_name="Upper.Lid.R.Glue", collection_name="MCH")]
        ),
    ]
)


_IrisMinOut = 0.7
_IrisMaxOut = 1.5
_PupilMinOut = 0.5
_PupilMaxOut = 2.3

EYES_CONTROLS = BoneGroup(
    name="Eyes Controls",
    generators=[
        #####
        # Iris Sliders
        #####
        OffsetBone(
            name="Iris.Ctrl.Master",
            bone_a="Eye.L",
            offset=(0.0025, 0.015, 0.051),
            parent="Eye.L",
            operations=[RigifyTypeOperation(time="Pre", bone_name="Iris.Ctrl.Master", rigify_type=rigify.types.basic_raw_copy()),
                        CollectionOperation(time="Pre", bone_name="Iris.Ctrl.Master", collection_name="Eyes (Macro)"),
                        WidgetOperation(time="Post", bone_name="Iris.Ctrl.Master", custom_object="IrisSliderFrame", rotation=(90.0,-90.0,180.0), wire_width=1.2, scale_to_bone_length=False, 
                                        color_set="CUSTOM", custom_color_normal=(0.443137, 0.541176, 1.0), custom_color_select=(0.443137, 0.541176, 1.0), custom_color_active=(0.443137, 0.541176, 1.0)),
                        ParentBoneOperation(time="Post", bone_name="Iris.Ctrl.Master", parent=["head"]),
                        PoseBoneOperation(time="Post", bone_name="Iris.Ctrl.Master",scale=(0.007, 0.007, 0.007)),
                        BoneRestrictionOperation(time="Post", bone_name="Iris.Ctrl.Master", lock_location=True, lock_rotation=True, lock_scale=True, hide_select=True),
            ]
        ),
        OffsetBone(
            name="Iris.Ctrl",
            bone_a="Eye.L",
            offset=(0.0025, 0.015, 0.051),
            parent="Eye.L",
            operations=[RigifyTypeOperation(time="Pre", bone_name="Iris.Ctrl", rigify_type=rigify.types.basic_raw_copy()),
                        CollectionOperation(time="Pre", bone_name="Iris.Ctrl", collection_name="Eyes (Macro)"),
                        WidgetOperation(time="Post", bone_name="Iris.Ctrl", custom_object="Slider", rotation=(90.0,-90.0, 180.0), wire_width=1.3, scale_to_bone_length=False),
                        BoneRestrictionOperation(time="Post", bone_name="Iris.Ctrl", lock_location=(True, True, False), lock_rotation=True, lock_scale=True),
                        ParentBoneOperation(time="Post", bone_name="Iris.Ctrl", parent=["Iris.Ctrl.Master"]),
                        ConstraintOperation(
                            bone_name="Iris.Ctrl",
                            time="Post",
                            constraint=LimitLocationConstraint(use_min_z=True, min_z=-1, use_max_z=True, max_z=1, use_transform_limit=True)),

            ]
        ),
        #####
        # Pupil Sliders
        #####
        OffsetBone(
            name="Pupil.Ctrl.Master",
            bone_a="Eye.L",
            offset=(0.0025, 0.015, 0.058),
            parent="Eye.L",
            operations=[RigifyTypeOperation(time="Pre", bone_name="Pupil.Ctrl.Master", rigify_type=rigify.types.basic_raw_copy()),
                        CollectionOperation(time="Pre", bone_name="Pupil.Ctrl.Master", collection_name="Eyes (Macro)"),
                        WidgetOperation(time="Post", bone_name="Pupil.Ctrl.Master", custom_object="PupilSliderFrame", rotation=(90.0,-90.0,180.0), wire_width=1.2, scale_to_bone_length=False, 
                                        color_set="CUSTOM", custom_color_normal=(0.443137, 0.541176, 1.0), custom_color_select=(0.443137, 0.541176, 1.0), custom_color_active=(0.443137, 0.541176, 1.0)),
                        ParentBoneOperation(time="Post", bone_name="Pupil.Ctrl.Master", parent=["head"]),
                        PoseBoneOperation(time="Post", bone_name="Pupil.Ctrl.Master",scale=(0.007, 0.007, 0.007)),
                        BoneRestrictionOperation(time="Post", bone_name="Pupil.Ctrl.Master", lock_location=True, lock_rotation=True, lock_scale=True, hide_select=True),
            ]
        ),
        OffsetBone(
            name="Pupil.Ctrl",
            bone_a="Eye.L",
            offset=(0.0025, 0.015, 0.058),
            parent="Eye.L",
            operations=[RigifyTypeOperation(time="Pre", bone_name="Pupil.Ctrl", rigify_type=rigify.types.basic_raw_copy()),
                        CollectionOperation(time="Pre", bone_name="Pupil.Ctrl", collection_name="Eyes (Macro)"),
                        WidgetOperation(time="Post", bone_name="Pupil.Ctrl", custom_object="Slider", rotation=(90.0,-90.0, 180.0), wire_width=1.3, scale_to_bone_length=False),
                        BoneRestrictionOperation(time="Post", bone_name="Pupil.Ctrl", lock_location=(True, True, False), lock_rotation=True, lock_scale=True),
                        ParentBoneOperation(time="Post", bone_name="Pupil.Ctrl", parent=["Pupil.Ctrl.Master"]),
                        ConstraintOperation(
                            bone_name="Pupil.Ctrl",
                            time="Post",
                            constraint=LimitLocationConstraint(use_min_z=True, min_z=-1, use_max_z=True, max_z=1, use_transform_limit=True)),

            ]
        ),

        #####
        # Anchor bones for EyeLid Control
        #####
        # - Left Eye
        ExtensionBone(
            name="lid.anchor.B.L.002",
            bone_a="lid.B.L.002",
            axis_type="global",
            axis="Z",
            start="head",
            parent="lid.B.L.002",
            operations=[CollectionOperation(time="Pre", bone_name="lid.anchor.B.L.002", collection_name="Eyes_Anchors"),
                        RigifyTypeOperation(time="Pre", bone_name="lid.anchor.B.L.002", rigify_type=rigify.types.basic_raw_copy()),
                        WidgetOperation(time="Post", bone_name="lid.anchor.B.L.002", color_set="THEME01", custom_object="Pointer", wire_width=2.0),
                        BoneRestrictionOperation(time="Post", bone_name="lid.anchor.B.L.002", lock_rotation=True, lock_scale=True, inherit_rotation=False, inherit_scale="NONE")
            ]
        ),
        ExtensionBone(
            name="lid.anchor.B.L.001",
            bone_a="lid.B.L.001",
            axis_type="global",
            axis="Z",
            start="head",
            parent="lid.B.L.001",
            operations=[CollectionOperation(time="Pre", bone_name="lid.anchor.B.L.001", collection_name="Eyes_Anchors"),
                        RigifyTypeOperation(time="Pre", bone_name="lid.anchor.B.L.001", rigify_type=rigify.types.basic_raw_copy()),
                        WidgetOperation(time="Post", bone_name="lid.anchor.B.L.001", color_set="THEME01", custom_object="Pointer", wire_width=2.0),
                        BoneRestrictionOperation(time="Post", bone_name="lid.anchor.B.L.001", lock_rotation=True, lock_scale=True, inherit_rotation=False, inherit_scale="NONE")
            ]
        ),
        ExtensionBone(
            name="lid.anchor.B.L.003",
            bone_a="lid.B.L.003",
            axis_type="global",
            axis="Z",
            start="head",
            parent="lid.B.L.003",
            operations=[CollectionOperation(time="Pre", bone_name="lid.anchor.B.L.003", collection_name="Eyes_Anchors"),
                        RigifyTypeOperation(time="Pre", bone_name="lid.anchor.B.L.003", rigify_type=rigify.types.basic_raw_copy()),
                        WidgetOperation(time="Post", bone_name="lid.anchor.B.L.003", color_set="THEME01", custom_object="Pointer", wire_width=2.0),
                        BoneRestrictionOperation(time="Post", bone_name="lid.anchor.B.L.003", lock_rotation=True, lock_scale=True, inherit_rotation=False, inherit_scale="NONE")
            ]
        ),
        # - Right Eye 
        ExtensionBone(
            name="lid.anchor.B.R.002",
            bone_a="lid.B.R.002",
            axis_type="global",
            axis="Z",
            start="head",
            parent="lid.B.R.002",
            operations=[CollectionOperation(time="Pre", bone_name="lid.anchor.B.R.002", collection_name="Eyes_Anchors"),
                        RigifyTypeOperation(time="Pre", bone_name="lid.anchor.B.R.002", rigify_type=rigify.types.basic_raw_copy()),
                        WidgetOperation(time="Post", bone_name="lid.anchor.B.R.002", color_set="THEME01", custom_object="Pointer", wire_width=2.0),
                        BoneRestrictionOperation(time="Post", bone_name="lid.anchor.B.R.002", lock_rotation=True, lock_scale=True, inherit_rotation=False, inherit_scale="NONE")
            ]
        ),
        ExtensionBone(
            name="lid.anchor.B.R.001",
            bone_a="lid.B.R.001",
            axis_type="global",
            axis="Z",
            start="head",
            parent="lid.B.R.001",
            operations=[CollectionOperation(time="Pre", bone_name="lid.anchor.B.R.001", collection_name="Eyes_Anchors"),
                        RigifyTypeOperation(time="Pre", bone_name="lid.anchor.B.R.001", rigify_type=rigify.types.basic_raw_copy()),
                        WidgetOperation(time="Post", bone_name="lid.anchor.B.R.001", color_set="THEME01", custom_object="Pointer", wire_width=2.0),
                        BoneRestrictionOperation(time="Post", bone_name="lid.anchor.B.R.001", lock_rotation=True, lock_scale=True, inherit_rotation=False, inherit_scale="NONE")
            ]
        ),
        ExtensionBone(
            name="lid.anchor.B.R.003",
            bone_a="lid.B.R.003",
            axis_type="global",
            axis="Z",
            start="head",
            parent="lid.B.R.003",
            operations=[CollectionOperation(time="Pre", bone_name="lid.anchor.B.R.003", collection_name="Eyes_Anchors"),
                        RigifyTypeOperation(time="Pre", bone_name="lid.anchor.B.R.003", rigify_type=rigify.types.basic_raw_copy()),
                        WidgetOperation(time="Post", bone_name="lid.anchor.B.R.003", color_set="THEME01", custom_object="Pointer", wire_width=2.0),
                        BoneRestrictionOperation(time="Post", bone_name="lid.anchor.B.R.003", lock_rotation=True, lock_scale=True, inherit_rotation=False, inherit_scale="NONE")
            ]
        ),
    
        #####
        # EyeLid Controllers
        #####
        OffsetBone(
            name="Lid.Ctrl.Master",
            bone_a="Eye.L",
            offset=(0.01, 0.015, 0.035),
            parent="Eye.L",
            operations=[RigifyTypeOperation(time="Pre", bone_name="Lid.Ctrl.Master", rigify_type=rigify.types.basic_raw_copy()),
                        CollectionOperation(time="Pre", bone_name="Lid.Ctrl.Master", collection_name="Eyes (Macro)"),
                        WidgetOperation(time="Post", bone_name="Lid.Ctrl.Master", custom_object="EyeTriangle", rotation=(90.0,0.0,0.0), wire_width=1.2, scale_to_bone_length=False, 
                                        color_set="CUSTOM", custom_color_normal=(1.0, 0.435294, 0.733333), custom_color_select=(1.0, 0.435294, 0.733333), custom_color_active=(1.0, 0.435294, 0.733333)),
                        ParentBoneOperation(time="Post", bone_name="Lid.Ctrl.Master", parent=["head"]),
                        PoseBoneOperation(time="Post", bone_name="Lid.Ctrl.Master",scale=(0.015, 0.015, 0.015)),
                        BoneRestrictionOperation(time="Post", bone_name="Lid.Ctrl.Master", lock_location=True, lock_rotation=True, lock_scale=True, hide_select=True),
            ]
        ),
        OffsetBone(
            name="Lid.Ctrl",
            bone_a="Eye.L",
            offset=(0.01, 0.015, 0.035),
            parent="Eye.L",
            operations=[RigifyTypeOperation(time="Pre", bone_name="Lid.Ctrl", rigify_type=rigify.types.basic_raw_copy()),
                        CollectionOperation(time="Pre", bone_name="Lid.Ctrl", collection_name="Eyes (Macro)"),
                        WidgetOperation(time="Post", bone_name="Lid.Ctrl", custom_object="Circle", rotation=(180.0,90.0,90.0), scale=(0.08,0.08,0.08), wire_width=1.3, scale_to_bone_length=False),
                        BoneRestrictionOperation(time="Post", bone_name="Lid.Ctrl", lock_location=(False, True, False), lock_rotation=True, lock_scale=True),
                        ParentBoneOperation(time="Post", bone_name="Lid.Ctrl", parent=["Lid.Ctrl.Master"]),
                        ConstraintOperation(
                            bone_name="Lid.Ctrl",
                            time="Post",
                            constraint=LimitLocationConstraint(use_min_z=True, min_z=-1, use_max_z=True, max_z=0,use_min_x=True, min_x=-0.667, use_max_x=True, max_x=0.667, use_transform_limit=True)),
            ]
        ),
    ],
    operations=[
        #####
        # Constraints for Eyelid Control
        #####
        # - Left Eye
        ConstraintOperation(
            bone_name="lid.T.L.003",
            constraint= CopyLocationConstraint(target_bone="lid.anchor.B.L.001", influence=0.0, name="AB_EyeLidControl"),
            time="Post"
        ),
        ConstraintOperation(
            bone_name="lid.T.L.002",
            constraint= CopyLocationConstraint(target_bone="lid.anchor.B.L.002", influence=0.0, name="AB_EyeLidControl"),
            time="Post"
        ),
        ConstraintOperation(
            bone_name="lid.T.L.001",
            constraint= CopyLocationConstraint(target_bone="lid.anchor.B.L.003", influence=0.0, name="AB_EyeLidControl"),
            time="Post"
        ),
        # - Right Eye
        ConstraintOperation(
            bone_name="lid.T.R.003",
            constraint= CopyLocationConstraint(target_bone="lid.anchor.B.R.001", influence=0.0, name="AB_EyeLidControl"),
            time="Post"
        ),
        ConstraintOperation(
            bone_name="lid.T.R.002",
            constraint= CopyLocationConstraint(target_bone="lid.anchor.B.R.002", influence=0.0, name="AB_EyeLidControl"),
            time="Post"
        ),
        ConstraintOperation(
            bone_name="lid.T.R.001",
            constraint= CopyLocationConstraint(target_bone="lid.anchor.B.R.003", influence=0.0, name="AB_EyeLidControl"),
            time="Post"
        ),

        #####
        # Drivers for Eyelid Control
        #####
        # - Left Eye
        DriverOperation(
            driver_name="EyeLidControl_lid.T.L.003",
            time="Post",
            bone_name="lid.T.L.003",
            constraint_name="AB_EyeLidControl",
            property="influence",
            driver=Driver(
                type="SCRIPTED",
                expression="min(1, max(0, (-y / 1) - max(0, x / 0.667)))",
                variables=[
                    TransformChannelVariable(
                        name="x",
                        target_bone="Lid.Ctrl",
                        transform_type="LOC_X",
                        transform_space="LOCAL_SPACE"
                    ),
                    TransformChannelVariable(
                        name="y",
                        target_bone="Lid.Ctrl",
                        transform_type="LOC_Z",
                        transform_space="LOCAL_SPACE"
                    )
                ]
            )
        ),
        DriverOperation(
            driver_name="EyeLidControl_lid.T.L.002",
            time="Post",
            bone_name="lid.T.L.002",
            constraint_name="AB_EyeLidControl",
            property="influence",
            driver=Driver(
                type="SCRIPTED",
                expression="min(1, max(0, (-y / 1) - max(0, x / 0.667)))",
                variables=[
                    TransformChannelVariable(
                        name="x",
                        target_bone="Lid.Ctrl",
                        transform_type="LOC_X",
                        transform_space="LOCAL_SPACE"
                    ),
                    TransformChannelVariable(
                        name="y",
                        target_bone="Lid.Ctrl",
                        transform_type="LOC_Z",
                        transform_space="LOCAL_SPACE"
                    )
                ]
            )
        ),
        DriverOperation(
            driver_name="EyeLidControl_lid.T.L.001",
            time="Post",
            bone_name="lid.T.L.001",
            constraint_name="AB_EyeLidControl",
            property="influence",
            driver=Driver(
                type="SCRIPTED",
                expression="min(1, max(0, (-y / 1) - max(0, x / 0.667)))",
                variables=[
                    TransformChannelVariable(
                        name="x",
                        target_bone="Lid.Ctrl",
                        transform_type="LOC_X",
                        transform_space="LOCAL_SPACE"
                    ),
                    TransformChannelVariable(
                        name="y",
                        target_bone="Lid.Ctrl",
                        transform_type="LOC_Z",
                        transform_space="LOCAL_SPACE"
                    )
                ]
            )
        ),
        # - Right Eye
        DriverOperation(
            driver_name="EyeLidControl_lid.T.R.003",
            time="Post",
            bone_name="lid.T.R.003",
            constraint_name="AB_EyeLidControl",
            property="influence",
            driver=Driver(
                type="SCRIPTED",
                expression="min(1, max(0, (-y / 1) - max(0, -x / 0.667)))",
                variables=[
                    TransformChannelVariable(
                        name="x",
                        target_bone="Lid.Ctrl",
                        transform_type="LOC_X",
                        transform_space="LOCAL_SPACE"
                    ),
                    TransformChannelVariable(
                        name="y",
                        target_bone="Lid.Ctrl",
                        transform_type="LOC_Z",
                        transform_space="LOCAL_SPACE"
                    )
                ]
            )
        ),
        DriverOperation(
            driver_name="EyeLidControl_lid.T.R.002",
            time="Post",
            bone_name="lid.T.R.002",
            constraint_name="AB_EyeLidControl",
            property="influence",
            driver=Driver(
                type="SCRIPTED",
                expression="min(1, max(0, (-y / 1) - max(0, -x / 0.667)))",
                variables=[
                    TransformChannelVariable(
                        name="x",
                        target_bone="Lid.Ctrl",
                        transform_type="LOC_X",
                        transform_space="LOCAL_SPACE"
                    ),
                    TransformChannelVariable(
                        name="y",
                        target_bone="Lid.Ctrl",
                        transform_type="LOC_Z",
                        transform_space="LOCAL_SPACE"
                    )
                ]
            )
        ),
        DriverOperation(
            driver_name="EyeLidControl_lid.T.R.001",
            time="Post",
            bone_name="lid.T.R.001",
            constraint_name="AB_EyeLidControl",
            property="influence",
            driver=Driver(
                type="SCRIPTED",
                expression="min(1, max(0, (-y / 1) - max(0, -x / 0.667)))",
                variables=[
                    TransformChannelVariable(
                        name="x",
                        target_bone="Lid.Ctrl",
                        transform_type="LOC_X",
                        transform_space="LOCAL_SPACE"
                    ),
                    TransformChannelVariable(
                        name="y",
                        target_bone="Lid.Ctrl",
                        transform_type="LOC_Z",
                        transform_space="LOCAL_SPACE"
                    )
                ]
            )
        ),
    
        #####
        # Iris and Pupil Drivers
        #####
        # - Driver for the Object property to drive the Shader
        DriverOperation(
            driver_name="Iris Scale X",
            data="iris",
            property='["Eye Scale X"]',
            driver=Driver(
                type="SCRIPTED",
                expression="1/iris_x",
                variables=[
                    TransformChannelVariable(name="iris_x", target_bone="j_f_irisprm_l", transform_type="SCALE_X", transform_space="LOCAL_SPACE"),
                ]
            ),
            time="Post",
        ),
        DriverOperation(
            driver_name="Iris Scale Y",
            data="iris",
            property='["Eye Scale Y"]',
            driver=Driver(
                type="SCRIPTED",
                expression="1/iris_y",
                variables=[
                    TransformChannelVariable(name="iris_y", target_bone="j_f_irisprm_l", transform_type="SCALE_Z", transform_space="LOCAL_SPACE"),
                    #Don't mind that it's taking the Z scale, it works
                ]
            ),
            time="Post",
        ),
        DriverOperation(
            driver_name="Iris Scale Z",
            data="iris",
            property='["Pupil Scale"]',
            driver=Driver(
                type="SCRIPTED",
                expression="iris_z-1",
                variables=[
                    TransformChannelVariable(name="iris_z", target_bone="j_f_irisprm_l", transform_type="SCALE_Y", transform_space="LOCAL_SPACE"),
                    #Don't mind that it's taking the Y scale, it works
                    #Admittedly this could be hella confusing on the user end if you haven't seen the code but I'll just write it in the wiki and call people stupid if they haven't read that -Oats
                    #Yes - Shino
                ]
            ),
            time="Post",
        ),

        # - Driver on the FFXIV Iris Control Bones to map from our Sliders (This is is based on a trust me bro basis and i will not explain it thx, explained it anyway)
        ## Quick math for expressions example 1 + (0.3 * var if var < 0 else 0.5 * var)
        ## 1 - 0.3 is our min outpuut 
        ## 1 + 0.5 is our max output
        ## Your welcome -Shino
        ## Also look ive made helper Variables so you dont have to edit all expressions the whole time.
        # - Left Side
        DriverOperation(
            driver_name="Iris.Ctrl Scale X L",
            time="Post",
            bone_name="j_f_irisprm_l",
            property=("scale", 0),
            driver=Driver(
                type="SCRIPTED",
                expression=f"1 + ({1-_IrisMinOut} * var if var < 0 else {_IrisMaxOut-1} * var)",
                variables=[
                    TransformChannelVariable(name="var", target_bone="Iris.Ctrl", transform_type="LOC_Z", transform_space="LOCAL_SPACE"),
                ]
            )
        ),
        DriverOperation(
            driver_name="Iris.Ctrl Scale Z L",
            time="Post",
            bone_name="j_f_irisprm_l",
            property=("scale", 2),
            driver=Driver(
                type="SCRIPTED",
                expression=f"1 + ({1-_IrisMinOut} * var if var < 0 else {_IrisMaxOut-1} * var)",
                variables=[
                    TransformChannelVariable(name="var", target_bone="Iris.Ctrl", transform_type="LOC_Z", transform_space="LOCAL_SPACE"),
                ]
            )
        ),
        DriverOperation(
            driver_name="Pupil.Ctrl Scale Y L",
            time="Post",
            bone_name="j_f_irisprm_l",
            property=("scale", 1),
            driver=Driver(
                type="SCRIPTED",
                expression=f"1 + ({1-_PupilMinOut} * var if var < 0 else {_PupilMaxOut-1} * var)",
                variables=[
                    TransformChannelVariable(name="var", target_bone="Pupil.Ctrl", transform_type="LOC_Z", transform_space="LOCAL_SPACE"),
                ]
            )
        ),
        # - Right Side
        DriverOperation(
            driver_name="Iris.Ctrl Scale X R",
            time="Post",
            bone_name="j_f_irisprm_r",
            property=("scale", 0),
            driver=Driver(
                type="SCRIPTED",
                expression=f"1 + ({1-_IrisMinOut} * var if var < 0 else {_IrisMaxOut-1} * var)",
                variables=[
                    TransformChannelVariable(name="var", target_bone="Iris.Ctrl", transform_type="LOC_Z", transform_space="LOCAL_SPACE"),
                ]
            )
        ),
        DriverOperation(
            driver_name="Iris.Ctrl Scale Z R",
            time="Post",
            bone_name="j_f_irisprm_r",
            property=("scale", 2),
            driver=Driver(
                type="SCRIPTED",
                expression=f"1 + ({1-_IrisMinOut} * var if var < 0 else {_IrisMaxOut-1} * var)",
                variables=[
                    TransformChannelVariable(name="var", target_bone="Iris.Ctrl", transform_type="LOC_Z", transform_space="LOCAL_SPACE"),
                ]
            )
        ),   
        DriverOperation(
            driver_name="Pupil.Ctrl Scale Y R",
            time="Post",
            bone_name="j_f_irisprm_r",
            property=("scale", 1),
            driver=Driver(
                type="SCRIPTED",
                expression=f"1 + ({1-_PupilMinOut} * var if var < 0 else {_PupilMaxOut-1} * var)",
                variables=[
                    TransformChannelVariable(name="var", target_bone="Pupil.Ctrl", transform_type="LOC_Z", transform_space="LOCAL_SPACE"),
                ]
            )
        ),
    ]
)

def get_rig_module() -> RigModule:
    return RigModule(
        name="Default",
        type="Generation",
        bone_groups=[HEAD, BROW, LEFT_EYE, RIGHT_EYE, EYES_CONTROLS],
        ui_collections = UI_Collections([
            BoneCollection(name="Head", ui=True, color_set="Head", row_index=1, title="Head"),
            BoneCollection(name="Face (Primary)", ui=True, color_set="Face_Primary", row_index=2, title="Face (Primary)", visible=True),
            BoneCollection(name="Face (Secondary)", ui=True, color_set="Face_Secondary", row_index=2, title="Face (Secondary)", visible=False),
            BoneCollection(name="Eyes (Macro)", ui=True, color_set="Face_Primary", row_index=3, title="Eyes (Macro)", visible=True),
        ]),
        operations=[
            #Head 
            PropOverrideOperation(bone_name="head", property_name="head_follow", value=1),

            #Left Face
            WidgetOperation(bone_name="Cheek.T.L",scale_factor=0.3,),
            WidgetOperation(bone_name="Cheek.T.L.001",scale_factor=0.3,),
            WidgetOperation(bone_name="Cheek.B.L.001",scale_factor=0.3,),
            WidgetOperation(bone_name="Cheek.B.L",scale_factor=0.3,),
            WidgetOperation(bone_name="Nose.L",scale_factor=0.3,),
            WidgetOperation(bone_name="Nostril.L",scale_factor=0.2,),    
            WidgetOperation(bone_name="Nose",scale_factor=0.2,),
            #Right Face
            WidgetOperation(bone_name="Cheek.T.R",scale_factor=0.3,),
            WidgetOperation(bone_name="Cheek.T.R.001",scale_factor=0.3,),
            WidgetOperation(bone_name="Cheek.B.R.001",scale_factor=0.3,),
            WidgetOperation(bone_name="Cheek.B.R",scale_factor=0.3,),
            WidgetOperation(bone_name="Nose.R",scale_factor=0.3,),
            WidgetOperation(bone_name="Nostril.R",scale_factor=0.2,),   
        ],
        ui_flags = ["Eye Lid Edit Mode"],
    )

