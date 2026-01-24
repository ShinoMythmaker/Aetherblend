import bpy
import json
import os
import re
from bpy.types import Operator
from bpy.props import BoolProperty
from bpy_extras.io_utils import ExportHelper, axis_conversion
from mathutils import Matrix
from ...preferences import get_preferences


class AETHER_OT_PoseExport(Operator, ExportHelper):
    """Exports armature pose into a .pose file."""
    bl_idname = "aether.pose_export"
    bl_label = "Export to Pose File"
    bl_options = {'REGISTER'}
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    filename_ext = '.pose'
    filter_glob: bpy.props.StringProperty(default='*.pose', options={'HIDDEN'}) # type: ignore
    
    
    def invoke(self, context, event):
        prefs = get_preferences()  
        blend_filename = bpy.path.basename(bpy.data.filepath) 
        if blend_filename:
            blend_filename = os.path.splitext(blend_filename)[0] + ".pose"  
        else:
            blend_filename = "untitled.pose"  
        
        if prefs.default_pose_export_path:
            self.filepath = os.path.join(prefs.default_pose_export_path, blend_filename)
        else:
            self.filepath = blend_filename
        
        return super().invoke(context, event)
    
    
    def execute(self, context):
        armature = context.object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "No armature selected")
            return {'CANCELLED'}
        
        # Get pose export properties
        export_props = context.scene.aether_animation_export
        
        # Build axis conversion matrix if enabled
        pose_correction_matrix = Matrix.Identity(4)
        if export_props.use_pose_axis_conversion:
            pose_correction_matrix = axis_conversion(
                from_up=export_props.pose_primary_axis,         ## Primary
                from_forward=export_props.pose_secondary_axis,  ## Secondary
                to_up='Y',                                      ## Target Primary
                to_forward='X',                                 ## Target Secondary
            ).to_4x4()
        
        skeleton_data = {
            "FileExtension": ".pose",
            "TypeName": "Aetherblend Pose",
            "FileVersion": 2,
            "Bones": {}
        }
        
        ffxiv_col = armature.data.collections.get('FFXIV')
        if not ffxiv_col:
            self.report({'ERROR'}, "FFXIV bone collection not found")
            return {'CANCELLED'}
            
        selected_bones = [bone.name for bone in ffxiv_col.bones]
        for bone_name in selected_bones:
            clean_bone_name = re.sub(r"\.\d+$", "", bone_name)
            bone = armature.pose.bones.get(bone_name)
            if bone:
                # Get bone matrix in world space (relative to scene origin)
                bone_matrix_world = armature.matrix_world @ bone.matrix
                
                # Apply axis conversion if enabled
                if export_props.use_pose_axis_conversion:
                    bone_matrix_world = bone_matrix_world @ pose_correction_matrix
                
                bone_data = {}
                bone_data["Position"] = f"{bone_matrix_world.translation.x:.6f}, {bone_matrix_world.translation.y:.6f}, {bone_matrix_world.translation.z:.6f}"
                bone_data["Rotation"] = f"{bone_matrix_world.to_quaternion().x:.6f}, {bone_matrix_world.to_quaternion().y:.6f}, {bone_matrix_world.to_quaternion().z:.6f}, {bone_matrix_world.to_quaternion().w:.6f}"
                bone_data["Scale"] = f"{bone_matrix_world.to_scale().x:.8f}, {bone_matrix_world.to_scale().y:.8f}, {bone_matrix_world.to_scale().z:.8f}"
                
                skeleton_data["Bones"][clean_bone_name] = bone_data
        
        with open(self.filepath, 'w') as f:
            json.dump(skeleton_data, f, indent=4)
        
        self.report({'INFO'}, "Pose exported successfully!")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(AETHER_OT_PoseExport)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_PoseExport)