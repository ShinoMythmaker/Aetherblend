"""Animation import and retargeting for FFXIV animations to AetherBlend rigs."""

import bpy
from bpy.props import StringProperty, EnumProperty
from bpy.types import Operator
import tempfile
from bpy_extras.io_utils import ImportHelper
from ...utils.axis_conversion import AXIS_ITEMS
from ...core.drivers import TransformChannelVariable, Driver
from ...core.operations import DriverOperation, ParentBoneOperation

# FFXIV bone names to AetherBlend FK control mapping
# TODO: Implement retargeting logic

#there has gotta be a better way to do this lmao
#It's just that these bones are so incredibly case-by-case with their axis and invert requirements that I don't see a way to automate it without some sort of manual mapping like this. At least this way it's all in one place and easy to edit if needed. -Oats
RETARGET_MAP = {
    # Arms
    "j_ude_a_l": {"target": "upper_arm_fk.L", "invert_x": False, "invert_y": False, "invert_z": True, "invert_w": False, "invert_loc_x": True, "invert_loc_y": False, "invert_loc_z": False},
    "j_ude_b_l": {"target": "forearm_fk.L", "invert_x": False, "invert_y": False, "invert_z": True, "invert_w": False, "invert_loc_x": True, "invert_loc_y": False, "invert_loc_z": False},
    "j_ude_a_r": {"target": "upper_arm_fk.R", "invert_x": False, "invert_y": False, "invert_z": True, "invert_w": False, "invert_loc_x": True, "invert_loc_y": False, "invert_loc_z": False}, 
    "j_ude_b_r": {"target": "forearm_fk.R", "invert_x": False, "invert_y": False, "invert_z": True, "invert_w": False, "invert_loc_x": True, "invert_loc_y": False, "invert_loc_z": False},
    "j_sako_l": {"target": "clavicle.L", "invert_x": True, "invert_y": False, "invert_z": False, "invert_w": False, "invert_loc_z": True},
    "j_sako_r": {"target": "clavicle.R", "invert_x": True, "invert_y": False, "invert_z": False, "invert_w": False, "invert_loc_z": True},

    # Fingers
    "j_oya_a_l": {"target": "thumb.L", "invert_z": True},
    "j_hito_a_l": {"target": "index.L", "invert_z": True},
    "j_naka_a_l": {"target": "middle.L", "invert_z": True},
    "j_kusu_a_l": {"target": "ring.L", "invert_z": True},
    "j_ko_a_l": {"target": "pinky.L", "invert_z": True},

    "j_oya_a_r": {"target": "thumb.R", "invert_z": True},
    "j_hito_a_r": {"target": "index.R", "invert_z": True},
    "j_naka_a_r": {"target": "middle.R", "invert_z": True},
    "j_kusu_a_r": {"target": "ring.R", "invert_z": True},
    "j_ko_a_r": {"target": "pinky.R", "invert_z": True},


    # Legs
    "j_asi_a_l": {"target": "thigh_fk.L", "invert_x": True, "invert_y": False, "invert_z": False, "invert_w": False, "invert_loc_x": False, "invert_loc_y": False, "invert_loc_z": True},
    "j_asi_b_l": {"target": "knee.L", "invert_x": True, "invert_y": False, "invert_z": False, "invert_w": False, "invert_loc_x": False, "invert_loc_y": False, "invert_loc_z": True},
    "j_asi_c_l": {"target": "shin_fk.L", "invert_x": True, "invert_y": False, "invert_z": False, "invert_w": False, "invert_loc_x": False, "invert_loc_y": False, "invert_loc_z": True}, 
    "j_asi_d_l": {"target": "foot_fk.L", "invert_x": True, "invert_y": False, "invert_z": False, "invert_w": False, "invert_loc_x": False, "invert_loc_y": False, "invert_loc_z": True},
    "j_asi_a_r": {"target": "thigh_fk.R", "invert_x": True, "invert_y": False, "invert_z": False, "invert_w": False, "invert_loc_x": False, "invert_loc_y": False, "invert_loc_z": True},
    "j_asi_b_r": {"target": "knee.R", "invert_x": True, "invert_y": False, "invert_z": False, "invert_w": False, "invert_loc_x": False, "invert_loc_y": False, "invert_loc_z": True},
    "j_asi_c_r": {"target": "shin_fk.R", "invert_x": True, "invert_y": False, "invert_z": False, "invert_w": False, "invert_loc_x": False, "invert_loc_y": False, "invert_loc_z": True},
    "j_asi_d_r": {"target": "foot_fk.R", "invert_x": True, "invert_y": False, "invert_z": False, "invert_w": False, "invert_loc_x": False, "invert_loc_y": False, "invert_loc_z": True},

    # Spine
    "j_kosi": {"target": "Spine_fk.001", "invert_x": True, "invert_y": True, "invert_z": True, "invert_w": False, "invert_loc_x": True, "invert_loc_y": True, "invert_loc_z": True},
    "j_sebo_a": {"target": "Spine_fk.002", "invert_x": True, "invert_y": False, "invert_z": False, "invert_w": False, "invert_loc_x": False, "invert_loc_y": False, "invert_loc_z": True},
    "j_sebo_b": {"target": "Spine_fk.003", "invert_x": True, "invert_y": False, "invert_z": False, "invert_w": False, "invert_loc_x": False, "invert_loc_y": False, "invert_loc_z": True},
    "j_sebo_c": {"target": "Spine_fk.004", "invert_x": True, "invert_y": False, "invert_z": False, "invert_w": False, "invert_loc_x": False, "invert_loc_y": False, "invert_loc_z": True},
    "j_kubi": {"target": "neck", "invert_x": True, "invert_y": False, "invert_z": False, "invert_w": False, "invert_loc_x": False, "invert_loc_y": False, "invert_loc_z": True},

    "n_hara": {"target": "n_hara_retarget", "invert_loc_x": False, "invert_loc_y": False, "invert_loc_z": True, "invert_z": False, "invert_x": True},

    # Tail
    "n_sippo_a": {"target": "Tail", "invert_z": False, "invert_x": True},
    "n_sippo_b": {"target": "Tail.001", "invert_z": False, "invert_x": True},
    "n_sippo_c": {"target": "Tail.002", "invert_z": False, "invert_x": True},
    "n_sippo_d": {"target": "Tail.003", "invert_z": False, "invert_x": True},
    "n_sippo_e": {"target": "Tail.004", "invert_z": False, "invert_x": True},
}



class AETHER_OT_AnimImport(bpy.types.Operator, ImportHelper):   
    bl_idname = "aether.anim_import"
    bl_label = "Import Animation"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Import and retarget in-game animation to AetherBlend rig (FBX only)"
    
    filepath: StringProperty(subtype="FILE_PATH")  # type: ignore
    filename_ext = ''
    filter_glob: StringProperty(default='*.glb;*.gltf;*.fbx', options={'HIDDEN'})  # type: ignore

    def get_actions(self, context):
        if context.active_object and context.active_object.type == 'ARMATURE':
            return [(a.name, a.name, "") for a in bpy.data.actions]
        return [('NONE', "No Actions", "")]
    
    selected_action: bpy.props.EnumProperty(name="Action", items=get_actions) # type: ignore

    export_format: bpy.props.EnumProperty(
        name="Format",
        items=[('FBX', "FBX", ""), ('GLB', "GLB", "")],
        default='FBX',
    ) # type: ignore

    # Bone Axis Orientation (FBX import)
    primary_bone_axis: EnumProperty(
        name="Primary Bone Axis",
        description="Primary axis for bone orientation",
        items=AXIS_ITEMS,
        default='X',
    )  # type: ignore
    
    secondary_bone_axis: EnumProperty(
        name="Secondary Bone Axis",
        description="Secondary axis for bone orientation",
        items=AXIS_ITEMS,
        default='Y',
    )  # type: ignore
    
    def export_fbx(self, filepath):
        bpy.ops.export_scene.fbx(
            filepath=filepath,
            use_selection=True,
            bake_anim=True,
            add_leaf_bones=False,
            primary_bone_axis='Y',
            secondary_bone_axis='X',
            use_armature_deform_only=True,
            bake_anim_use_all_actions=False,
            bake_anim_use_nla_strips=False,
            bake_anim_use_all_bones=True,
            bake_anim_force_startend_keying=True,
            bake_anim_simplify_factor=0.0
        )

    #Good God I need to refactor this -Oats

    def retarget_bone_animation(self, source_bone_name, target_bone_name, invert_x, invert_y, invert_z, invert_w, invert_loc_x, invert_loc_y, invert_loc_z, source_armature, target_armature): #these arguments are getting out of hand, now there are 11 of them! -Oats

        target = bpy.data.objects.get(target_armature.name)
        source = bpy.data.objects.get(source_armature.name)

        if not target or target.type != 'ARMATURE':
            self.report({'ERROR'}, "No armature found in the scene for retargeting")
            return
        
        source_bone = source_bone_name
        target_bone = target_bone_name

        transform_type_X = "LOC_Z"
        transform_type_Y = "LOC_Y"
        transform_type_Z = "LOC_X"

        transform_type_X_rot = "ROT_Z"
        transform_type_Y_rot = "ROT_Y"
        transform_type_Z_rot = "ROT_X"

        # if source_bone == "n_hara":
        #     transform_type_X = "LOC_Y"
        #     transform_type_Y = "LOC_Z"
        #     transform_type_X_rot = "ROT_Y"
        #     transform_type_Y_rot = "ROT_Z"

        if not source_bone:
            self.report({'WARNING'}, f"Source bone '{source_bone_name}' not found")
            return
        if not target_bone:
            self.report({'WARNING'}, f"Target bone '{target_bone_name}' not found")
            return
        
        try:
            # Build expressions with optional inversion
            rot_z_expr = f"{'-' if invert_x else ''}{source_bone}_rot_z"
            rot_x_expr = f"{'-' if invert_z else ''}{source_bone}_rot_x"
            rot_y_expr = f"{'-' if invert_y else ''}{source_bone}_rot_y"
            rot_w_expr = f"{'-' if invert_w else ''}{source_bone}_rot_w"

            loc_x_expr = f"{'-' if invert_loc_x else ''}{source_bone}_loc_x"
            loc_y_expr = f"{'-' if invert_loc_y else ''}{source_bone}_loc_y"
            loc_z_expr = f"{'-' if invert_loc_z else ''}{source_bone}_loc_z"
            
            driver_X = DriverOperation(
                driver_name=f"{target_bone}_anim_driver_X",
                bone_name=target_bone,
                property=["rotation_quaternion", 1],  # Targeting the X component of the quat
                driver=Driver(
                    expression=rot_z_expr,
                    type='SCRIPTED',
                    variables=[
                        TransformChannelVariable(
                            name=f"{source_bone}_rot_z",
                            target_bone=source_bone,
                            target_object=source,
                            transform_type=transform_type_X_rot,
                            transform_space="LOCAL_SPACE",
                            rotation_mode="QUATERNION",
                        ),
                    ],
                )
            )
            
            driver_Z = DriverOperation(
                driver_name=f"{target_bone}_anim_driver_Z",
                bone_name=target_bone,
                property=["rotation_quaternion", 3],  # Targeting the Z component of the quat
                driver=Driver(
                    expression=rot_x_expr,
                    type='SCRIPTED',
                    variables=[
                        TransformChannelVariable(
                            name=f"{source_bone}_rot_x",
                            target_bone=source_bone,
                            target_object=source,
                            transform_type="ROT_X",
                            transform_space="LOCAL_SPACE",
                            rotation_mode="QUATERNION",
                        ),
                    ],
                )
            )

            driver_Y = DriverOperation(
                driver_name=f"{target_bone}_anim_driver_Y",
                bone_name=target_bone,
                property=["rotation_quaternion", 2],  # Targeting the Y component of the quat
                driver=Driver(
                    expression=rot_y_expr,
                    type='SCRIPTED',
                    variables=[
                        TransformChannelVariable(
                            name=f"{source_bone}_rot_y",
                            target_bone=source_bone,
                            target_object=source,
                            transform_type=transform_type_Y_rot,
                            transform_space="LOCAL_SPACE",
                            rotation_mode="QUATERNION",
                        ),
                    ],
                )
            )

            driver_W = DriverOperation(
                driver_name=f"{target_bone}_anim_driver_W",
                bone_name=target_bone,
                property=["rotation_quaternion", 0],  # Targeting the W component of the quat
                driver=Driver(
                    expression=rot_w_expr,
                    type='SCRIPTED',
                    variables=[
                        TransformChannelVariable(
                            name=f"{source_bone}_rot_w",
                            target_bone=source_bone,
                            target_object=source,
                            transform_type="ROT_W",
                            transform_space="LOCAL_SPACE",
                            rotation_mode="QUATERNION",
                        ),
                    ],
                )
            )

            driver_loc_X= DriverOperation(
                driver_name=f"{target_bone}_anim_driver_loc_X",
                bone_name=target_bone,
                property=["location", 0],  # Targeting the X component of the location
                driver=Driver(
                    expression=loc_z_expr,
                    type='SCRIPTED',
                    variables=[
                        TransformChannelVariable(
                            name=f"{source_bone}_loc_z",
                            target_bone=source_bone,
                            target_object=source,
                            transform_type=transform_type_X,
                            transform_space="LOCAL_SPACE",
                        ),
                    ],
                )
            )

            driver_loc_Y= DriverOperation(
                driver_name=f"{target_bone}_anim_driver_loc_Y",
                bone_name=target_bone,
                property=["location", 1],  # Targeting the Y component of the location
                driver=Driver(
                    expression=loc_y_expr,
                    type='SCRIPTED',
                    variables=[
                        TransformChannelVariable(
                            name=f"{source_bone}_loc_y",
                            target_bone=source_bone,
                            target_object=source,
                            transform_type=transform_type_Y,
                            transform_space="LOCAL_SPACE",
                        ),
                    ],
                )
            )

            driver_loc_Z= DriverOperation(
                driver_name=f"{target_bone}_anim_driver_loc_Z",
                bone_name=target_bone,
                property=["location", 2],  # Targeting the Z component of the location
                driver=Driver(
                    expression=loc_x_expr,
                    type='SCRIPTED',
                    variables=[
                        TransformChannelVariable(
                            name=f"{source_bone}_loc_x",
                            target_bone=source_bone,
                            target_object=source,
                            transform_type=transform_type_Z,
                            transform_space="LOCAL_SPACE",
                        ),
                    ],
                )
            )

            driver_Y.apply(target_armature)
            driver_Z.apply(target_armature)
            driver_X.apply(target_armature)
            driver_W.apply(target_armature)
            driver_loc_X.apply(target_armature)
            driver_loc_Y.apply(target_armature)
            driver_loc_Z.apply(target_armature)

        except Exception as e:
            self.report({'ERROR'}, f"Failed to retarget '{source_bone_name}' to '{target_bone_name}': {str(e)}")

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "primary_bone_axis")
        layout.prop(self, "secondary_bone_axis")

    def execute(self, context):  
        bpy.context.window.cursor_set('WAIT')   
        
        if not self.filepath:
            self.report({'ERROR'}, "[AetherBlend] Please select an animation file (.fbx, .gltf, or .glb)")
            bpy.context.window.cursor_set('DEFAULT')
            return {'CANCELLED'}
        
        filepath_lower = self.filepath.lower()
        is_gltf = filepath_lower.endswith(('.gltf', '.glb'))
        is_fbx = filepath_lower.endswith('.fbx')

        if not is_gltf and not is_fbx:
            self.report({'ERROR'}, "[AetherBlend] Please select a valid animation file (.fbx, .gltf, or .glb)")
            bpy.context.window.cursor_set('DEFAULT')
            return {'CANCELLED'}

        try:
             # Store target rig BEFORE import
            target_armature = context.active_object

            if not target_armature or target_armature.type != 'ARMATURE':
                self.report({'ERROR'}, "Select target AetherBlend armature first")
                bpy.context.window.cursor_set('DEFAULT')
                return {'CANCELLED'}
            
            # Import with FBX axis conversion (native)

            if is_fbx:
                bpy.ops.import_scene.fbx(
                    filepath=self.filepath,
                    ignore_leaf_bones=True,
                    primary_bone_axis=self.primary_bone_axis,
                    secondary_bone_axis=self.secondary_bone_axis,
                )
            else:
                bpy.ops.import_scene.gltf(
                    filepath=self.filepath,
                    disable_bone_shape=True,
                )
                # Get the imported glTF armature
                gltf_armature = context.active_object
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.fbx') as temp:
                    temp_path = temp.name
                    self.export_fbx(filepath=temp_path)
                    
                    # Delete the glTF armature before re-importing FBX
                    bpy.data.objects.remove(gltf_armature, do_unlink=True)
                    
                    bpy.ops.import_scene.fbx(
                        filepath=temp_path,
                        ignore_leaf_bones=True,
                        primary_bone_axis=self.primary_bone_axis,
                        secondary_bone_axis=self.secondary_bone_axis,
                        anim_offset=0
                    )
            
            source_armature = context.active_object
            if not source_armature or source_armature.type != 'ARMATURE':
                self.report({'ERROR'}, "Failed to import armature")
                bpy.context.window.cursor_set('DEFAULT')
                return {'CANCELLED'}

            parent_op_bones_hara=["Spine_fk.001", "Spine_fk.002"]

            parent_op_bones_leg={"knee.L" : "thigh_fk.L",
                                 "shin_fk.L" : "knee.L",
                                 "knee.R" : "thigh_fk.R",
                                 "shin_fk.R" : "knee.R",
                                 }

            # Set target_armature as active so mode switching works correctly
            bpy.context.view_layer.objects.active = target_armature
            target_armature.select_set(True)

            for bone_name in parent_op_bones_hara:
                ParentOP=ParentBoneOperation(bone_name=bone_name, parent=["n_hara_retarget"])
                ParentOP.apply(armature=target_armature)

            for bone_name, parent_target in parent_op_bones_leg.items():
                ParentOP=ParentBoneOperation(bone_name=bone_name, parent=(parent_target,))
                ParentOP.apply(armature=target_armature)

            for ffbone, mapping in RETARGET_MAP.items():
                self.retarget_bone_animation(ffbone, mapping["target"], mapping.get("invert_x", False), mapping.get("invert_y", False), mapping.get("invert_z", False), mapping.get("invert_w", False), mapping.get("invert_loc_x", False), mapping.get("invert_loc_y", False), mapping.get("invert_loc_z", False), source_armature, target_armature)

            self.report({'INFO'}, "Animation imported successfully")
            bpy.context.window.cursor_set('DEFAULT')
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Import failed: {str(e)}")
            bpy.context.window.cursor_set('DEFAULT')
            return {'CANCELLED'}

def register():
    bpy.utils.register_class(AETHER_OT_AnimImport)


def unregister():
    bpy.utils.unregister_class(AETHER_OT_AnimImport)