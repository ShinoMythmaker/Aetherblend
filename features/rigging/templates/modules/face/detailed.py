import mathutils

from ......core.rigify.settings import UI_Collections, BoneCollection

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
            parent=["Spine.004", "j_sebo_c"],
            is_connected=False,
            req_bones=["j_kubi", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.spines_super_head(),
                b_collection="Head"
            )
        ),
        ExtensionBone(
            name="Head",
            bone_a="j_kao",
            parent="Neck",
            is_connected=True,
            axis_type="armature",
            axis="Z",
            size_factor=20.0,
            req_bones=["j_kao"],
            pose_operations=PoseOperations(
                b_collection="Head"
            )
        ),
        #Cheek Right
        ConnectBone(
            name="Cheek.B.R",
            bone_a="j_f_shoho_r",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_shoho_r", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Primary)"
            )
        ),
        ConnectBone(
            name="Cheek.B.R.001",
            bone_a="j_f_dhoho_r",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_dhoho_r", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Secondary)"
            )
        ),
        ConnectBone(
            name="Cheek.T.R",
            bone_a="j_f_hoho_r",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hoho_r", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Primary)"
            )
        ),
        ConnectBone(
            name="Cheek.T.R.001",
            bone_a="j_f_dmemoto_r",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_dmemoto_r", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Secondary)"
            )
        ),
        #Cheek Left
        ConnectBone(
            name="Cheek.B.L",
            bone_a="j_f_shoho_l",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_shoho_l", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Primary)"
            )
        ),
        ConnectBone(
            name="Cheek.B.L.001",
            bone_a="j_f_dhoho_l",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_dhoho_l", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Secondary)"
            )
        ),
        ConnectBone(
            name="Cheek.T.L",
            bone_a="j_f_hoho_l",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hoho_l", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Primary)"
            )
        ),
        ConnectBone(
            name="Cheek.T.L.001",
            bone_a="j_f_dmemoto_l",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_dmemoto_l", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Secondary)"
            )
        ),
        #Nose Centre
        ConnectBone(
            name="Nose",
            bone_a="j_f_uhana",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_uhana", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Secondary)"
            )
        ),
        #Nose Right
        ConnectBone(
            name="Nose.R",
            bone_a="j_f_dmiken_r",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_dmiken_r", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Secondary)"
            )
        ),
        ConnectBone(
            name="Nostril.R",
            bone_a="j_f_hana_r",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hana_r", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Secondary)"
            )
        ),
        #Nose Left
        ConnectBone(
            name="Nose.L",
            bone_a="j_f_dmiken_l",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_dmiken_l", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Secondary)"
            )
        ),
        ConnectBone(
            name="Nostril.L",
            bone_a="j_f_hana_l",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hana_l", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Secondary)"
            )
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
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_anchor(skin_anchor_hide=True),
                b_collection="Face"
            )
        ),
        #Jaw
        CenterBone(
            name="jaw_master_ref",
            ref_bones=["j_f_dlip_01_r", "j_f_dlip_01_l"],
            parent="Head",
            axis="Y",
            inverted=False,
            req_bones=["j_f_dlip_01_r", "j_f_dlip_01_l"],
            pose_operations=PoseOperations(
                b_collection="MCH",
            ),
        ),
        ConnectBone(
            name="jaw_master",
            bone_a="j_f_ago",
            bone_b="jaw_master_ref",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_ago", "jaw_master_ref"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.face_skin_jaw(jaw_mouth_influence=1.0),
                b_collection="Face (Primary)"
            )
        ),
        #Mouth Center Reference
        CenterBone(
            name="Mouth.Center",
            ref_bones=["j_f_ulip_01_r", "j_f_ulip_01_l"],
            parent="Head",
            axis="Y",
            inverted=False,
            req_bones=["j_f_ulip_01_r", "j_f_ulip_01_l"],
            pose_operations=PoseOperations(
                b_collection="MCH",
            ),
        ),
        #Mouth Right
        ConnectBone(
            name="Lip.T.R",
            bone_a="Mouth.Center",
            bone_b="j_f_ulip_01_r",
            parent="jaw_master",
            is_connected=False,
            req_bones=["j_f_ulip_01_r", "Mouth.Center"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Head", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 0.0, -1.0], primary_layer_extra="Face (Primary)"),
                b_collection="Face (Secondary)"
            )
        ),
        ConnectBone(
            name="Lip.T.R.001",
            bone_a="j_f_ulip_01_r",
            bone_b="j_f_umlip_01_r",
            parent="Lip.T.R",
            is_connected=True,
            req_bones=["j_f_umlip_01_r", "j_f_ulip_01_r"],
            pose_operations=PoseOperations(
                b_collection="Face"
            )
        ),
        ConnectBone(
            name="Lip.B.R",
            bone_a="jaw_master_ref",
            bone_b="j_f_dlip_01_r",
            parent="jaw_master",
            is_connected=False,
            req_bones=["j_f_dlip_01_r", "jaw_master_ref"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Head", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 0.0, -1.0], primary_layer_extra="Face (Primary)"),
                b_collection="Face (Secondary)"
            )
        ),
        ConnectBone(
            name="Lip.B.R.001",
            bone_a="j_f_dlip_01_r",
            bone_b="j_f_dmlip_01_r",
            parent="Lip.B.R",
            is_connected=True,
            req_bones=["j_f_dmlip_01_r", "j_f_dlip_01_r"],
            pose_operations=PoseOperations(
                b_collection="Face"
            )
        ),
        
        #This is a reference point for the last bone in the chain
        CenterBone(
            name="Corner.R",
            ref_bones=["j_f_uslip_r", "j_f_dslip_r", "Cheek.B.R"],
            parent="Head",
            axis="Y",
            inverted=False,
            req_bones=["j_f_uslip_r", "j_f_dslip_r", "Cheek.B.R"],
            pose_operations=PoseOperations(
                b_collection="MCH",
            ),
        ),
        ConnectBone(
            name="Lip.T.R.002",
            bone_a="j_f_umlip_01_r",
            bone_b="j_f_uslip_r",
            parent="Lip.T.R.001",
            is_connected=True,
            req_bones=["j_f_uslip_r", "j_f_umlip_01_r"],
            pose_operations=PoseOperations(
                 b_collection="Face"
            )
        ),
        ConnectBone(
            name="Lip.T.R.003",
            bone_a="j_f_uslip_r",
            bone_b="Corner.R",
            parent="Lip.T.R.002",
            is_connected=True,
            req_bones=["j_f_uslip_r", "Corner.R"],
            pose_operations=PoseOperations(
                    b_collection="Face"
            )
        ),
        ConnectBone(
            name="Lip.B.R.002",
            bone_a="j_f_dmlip_01_r",
            bone_b="j_f_dslip_r",
            parent="Lip.B.R.001",
            is_connected=True,
            req_bones=["j_f_dmlip_01_r", "j_f_dslip_r"],
            pose_operations=PoseOperations(
                 b_collection="Face"
            )
        ),
        ConnectBone(
            name="Lip.B.R.003",
            bone_a="j_f_dslip_r",
            bone_b="Corner.R",
            parent="Lip.B.R.002",
            is_connected=True,
            req_bones=["j_f_dslip_r", "Corner.R"],
            pose_operations=PoseOperations(
                    b_collection="Face"
            )
        ),

        #Left Mouth
        ConnectBone(
            name="Lip.T.L",
            bone_a="Mouth.Center",
            bone_b="j_f_ulip_01_l",
            parent="jaw_master",
            is_connected=False,
            req_bones=["j_f_ulip_01_l", "Mouth.Center"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Head", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 0.0, -1.0], primary_layer_extra="Face (Primary)"),
                b_collection="Face (Secondary)"
            )
        ),
        ConnectBone(
            name="Lip.T.L.001",
            bone_a="j_f_ulip_01_l",
            bone_b="j_f_umlip_01_l",
            parent="Lip.T.L",
            is_connected=True,
            req_bones=["j_f_umlip_01_l", "j_f_ulip_01_l"],
            pose_operations=PoseOperations(
                b_collection="Face"
            )
        ),
        ConnectBone(
            name="Lip.B.L",
            bone_a="jaw_master_ref",
            bone_b="j_f_dlip_01_l",
            parent="jaw_master",
            is_connected=False,
            req_bones=["j_f_dlip_01_l", "jaw_master_ref"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Head", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 0.0, -1.0], primary_layer_extra="Face (Primary)"),
                b_collection="Face (Secondary)"
            )
        ),
        ConnectBone(
            name="Lip.B.L.001",
            bone_a="j_f_dlip_01_l",
            bone_b="j_f_dmlip_01_l",
            parent="Lip.B.L",
            is_connected=True,
            req_bones=["j_f_dmlip_01_l", "j_f_dlip_01_l"],
            pose_operations=PoseOperations(
                b_collection="Face"
            )
        ),
        #This is a reference point for the last bone in the chain
        CenterBone(
            name="Corner.L",
            ref_bones=["j_f_uslip_l", "j_f_dslip_l", "Cheek.B.L"],
            parent="Head",
            axis="Y",
            inverted=False,
            req_bones=["j_f_uslip_l", "j_f_dslip_l", "Cheek.B.L"],
             pose_operations=PoseOperations(
                b_collection="MCH"
             ),
        ),
        ConnectBone(
           name = "Lip.T.L.002",
           bone_a = "j_f_umlip_01_l",
           bone_b = "j_f_uslip_l",
           parent = "Lip.T.L.001",
           is_connected = True,
           req_bones = ["j_f_umlip_01_l", "j_f_uslip_l"],
           pose_operations = PoseOperations(
               b_collection = "Face"
           )
       ),
        ConnectBone(
           name = "Lip.T.L.003",
           bone_a = "j_f_uslip_l",
           bone_b = "Corner.L",
           parent = "Lip.T.L.002",
           is_connected = True,
           req_bones = ["j_f_uslip_l", "Corner.L"],
           pose_operations = PoseOperations(
               b_collection = "Face"
          )
       ),
        ConnectBone(
           name = "Lip.B.L.002",
           bone_a = "j_f_dmlip_01_l",
           bone_b = "j_f_dslip_l",
           parent = "Lip.B.L.001",
           is_connected = True,
           req_bones = ["j_f_dmlip_01_l", "j_f_dslip_l"],
           pose_operations = PoseOperations(
               b_collection = "Face"
          )
       ),
        ConnectBone(
           name = "Lip.B.L.003",
           bone_a = "j_f_dslip_l",
           bone_b = "Corner.L",
           parent = "Lip.B.L.002",
           is_connected = True,
           req_bones = ["Corner.L", "j_f_dslip_l"],
           pose_operations = PoseOperations(
               b_collection = "Face"
          )
       ),
        #Teeth
        ExtensionBone(
            name="Teeth.T",
            bone_a="j_f_hagukiup",
            size_factor=1,
            axis_type="local",
            axis="Y",
            parent="Head",
            start="head",
            is_connected=False,
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.basic_super_copy(widget_type="teeth"),
                b_collection="Mouth"
            )
        ),
        ExtensionBone(
            name="Teeth.B",
            bone_a="j_f_hagukidn",
            size_factor=1,
            axis_type="local",
            axis="Y",
            parent="jaw_master",
            start="head",
            is_connected=False,
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.basic_super_copy(widget_type="teeth"),
                b_collection="Mouth"
            )
        ),
        #Tongue
        ConnectBone(
            name="Tongue",
            bone_a="j_f_bero_01",
            bone_b="j_f_bero_02",
            parent="jaw_master",
            is_connected=False,
            req_bones=["j_f_bero_01", "j_f_bero_02"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Head"),
                b_collection="Mouth"
            )
        ),
        ConnectBone(
            name="Tongue.001",
            bone_a="j_f_bero_02",
            bone_b="j_f_bero_03",
            parent="Tongue",
            is_connected=True,
            req_bones=["j_f_bero_02", "j_f_bero_03"],
            pose_operations=PoseOperations(
                b_collection="Mouth"
            )
        ),
        ExtensionBone(
            name="Tongue.002",
            bone_a="Tongue.001",
            parent="Tongue.001",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["Tongue.001"],
            pose_operations=PoseOperations(
                b_collection="Mouth"
            )
        ),
        #Nose Glue
        ConnectBone(
            name="Nostril.Glue.R",
            bone_a="j_f_hana_r",
            bone_b="j_f_uhana",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hana_r", "j_f_uhana"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Nostril.Glue.L",
            bone_a="j_f_hana_l",
            bone_b="j_f_uhana",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hana_l", "j_f_uhana"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Nostril.Glue.R.001",
            bone_a="Cheek.T.R.001", 
            bone_b="Nostril.R",
            parent="Head",
            is_connected=False,
            req_bones=["Cheek.T.R.001", "Nostril.R"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            ),
        ),
        ConnectBone(
            name="Nostril.Glue.L.001",
            bone_a="Cheek.T.L.001", 
            bone_b="Nostril.L",
            parent="Head",
            is_connected=False,
            req_bones=["Cheek.T.L.001", "Nostril.L"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            ),
        ),
        #Cheek Glue Bones Right
        ConnectBone(
            name="Cheek.B.R.glue",
            bone_a="j_f_dhoho_r",
            bone_b="j_f_shoho_r",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_shoho_r", "j_f_dhoho_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Cheek.T.R.glue",
            bone_a="j_f_dhoho_r",
            bone_b="j_f_hoho_r",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hoho_r", "j_f_dhoho_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            )
        ),
        #Cheek Glue Bones Left
        ConnectBone(
            name="Cheek.B.L.glue",
            bone_a="j_f_dhoho_l",
            bone_b="j_f_shoho_l",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_shoho_l", "j_f_dhoho_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Cheek.T.L.glue",
            bone_a="j_f_dhoho_l",
            bone_b="j_f_hoho_l",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hoho_l", "j_f_dhoho_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            )
        ),
        #Nostril Glue Bones
        ConnectBone(
            name="Nostril.Glue.R",
            bone_a="j_f_hana_r",
            bone_b="j_f_uhana",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hana_r", "j_f_uhana"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Nostril.Glue.L",
            bone_a="j_f_hana_l",
            bone_b="j_f_uhana",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hana_l", "j_f_uhana"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Nostril.Glue.R.001",
            bone_a="Cheek.T.R.001", 
            bone_b="Nostril.R",
            parent="Head",
            is_connected=False,
            req_bones=["Cheek.T.R.001", "Nostril.R"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            ),
        ),
        ConnectBone(
            name="Nostril.Glue.L.001",
            bone_a="Cheek.T.L.001", 
            bone_b="Nostril.L",
            parent="Head",
            is_connected=False,
            req_bones=["Cheek.T.L.001", "Nostril.L"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            ),
        ),
        #Lip Glue Bones
        ConnectBone(
            name="Lip.T.R.001.glue",
            bone_a="j_f_hana_r",
            bone_b="j_f_ulip_01_r",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hana_r", "j_f_ulip_01_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.2, skin_glue_tail_reparent=True),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Lip.T.L.001.glue",
            bone_a="j_f_hana_l",
            bone_b="j_f_ulip_01_l",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hana_l", "j_f_ulip_01_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.2, skin_glue_tail_reparent=True),
                b_collection="MCH"
            )
        ),
        #Mouth Corner Glue Bones
        ConnectBone(
            name="Mouth.Corner.glue.L",
            bone_a="j_f_shoho_l",
            bone_b="Corner.L",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_shoho_l", "Corner.L"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5, skin_glue_tail_reparent=True),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Mouth.Corner.glue.R",
            bone_a="j_f_shoho_r",
            bone_b="Corner.R",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_shoho_r", "Corner.R"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5, skin_glue_tail_reparent=True),
                b_collection="MCH"
            )
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
            is_connected=False,
            req_bones=["j_f_mayu_r", "j_f_mmayu_r",],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, skin_control_orientation_bone="Head", skin_chain_falloff_length=True, primary_layer_extra="Face (Primary)"),
                b_collection="Face (Secondary)",
            )
        ),
        ConnectBone(
            name="Brow.R.001",
            bone_a="j_f_mmayu_r",
            bone_b="j_f_miken_01_r",
            parent="Brow.R",
            is_connected=True,
            req_bones=["j_f_mmayu_r", "j_f_miken_01_r"],
            pose_operations=PoseOperations(
                b_collection="Face (Primary)",
            )
        ),
        ConnectBone(
            name="Brow.R.002",
            bone_a="j_f_miken_01_r",
            bone_b="j_f_miken_02_r",
            parent="Brow.R.001",
            is_connected=True,
            req_bones=["j_f_miken_01_r", "j_f_miken_02_r"],
            pose_operations=PoseOperations(
                b_collection="Face (Primary)",
            )
        ),
        ExtensionBone(
            name="Brow.R.003",
            bone_a="Brow.R.002",
            parent="Brow.R.002",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["j_f_miken_02_r"],
            pose_operations=PoseOperations(
                b_collection="Face (Primary)"
            )
        ),
        ConnectBone(
            name="Brow.L",
            bone_a="j_f_mayu_l",
            bone_b="j_f_mmayu_l",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_mayu_l", "j_f_mmayu_l",],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, skin_control_orientation_bone="Head", skin_chain_falloff_length=True, primary_layer_extra="Face (Primary)"),
                b_collection="Face (Secondary)",
            )
        ),
        ConnectBone(
            name="Brow.L.001",
            bone_a="j_f_mmayu_l",
            bone_b="j_f_miken_01_l",
            parent="Brow.L",
            is_connected=True,
            req_bones=["j_f_mmayu_l", "j_f_miken_01_l"],
            pose_operations=PoseOperations(
                b_collection="Face (Primary)",
            )
        ),
        ConnectBone(
            name="Brow.L.002",
            bone_a="j_f_miken_01_l",
            bone_b="j_f_miken_02_l",
            parent="Brow.L.001",
            is_connected=True,
            req_bones=["j_f_miken_01_l", "j_f_miken_02_l"],
            pose_operations=PoseOperations(
                b_collection="Face (Primary)",
            )
        ),
        ExtensionBone(
            name="Brow.L.003",
            bone_a="Brow.L.002",
            parent="Brow.L.002",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["j_f_miken_02_l"],
            pose_operations=PoseOperations(
                b_collection="Face (Primary)"
            )
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

