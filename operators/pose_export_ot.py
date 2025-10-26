import bpy
import json
import os
import re
from bpy.types import Operator
from bpy.props import BoolProperty
from bpy_extras.io_utils import ExportHelper  


class AETHER_OT_PoseExport(Operator, ExportHelper):
    """Exports armature pose into a .pose file."""
    bl_idname = "aether.pose_export"
    bl_label = "Export to Pose File"
    bl_options = {'REGISTER'}
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    filename_ext = '.pose'
    filter_glob: bpy.props.StringProperty(default='*.pose', options={'HIDDEN'}) # type: ignore
    
    
    def invoke(self, context, event):
        blend_filename = bpy.path.basename(bpy.data.filepath) 
        if blend_filename:
            blend_filename = os.path.splitext(blend_filename)[0] + ".pose" 
        else:
            blend_filename = "untitled.pose" 
        
        self.filepath = blend_filename

        return super().invoke(context, event)
    
    
    def execute(self, context):
        armature = context.object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "No armature selected")
            return {'CANCELLED'}
        
        root_bone = armature.pose.bones.get("n_throw")
        if not root_bone:
            self.report({'ERROR'}, "Origin bone 'n_throw' not found")
            return {'CANCELLED'}
        
        root_matrix_world = armature.matrix_world @ root_bone.matrix
        skeleton_data = {
            "FileExtension": ".pose",
            "TypeName": "Aetherblend Pose",
            "FileVersion": 2,
            "Bones": {}
        }
        
        ffxiv_col = armature.data.collections.get('FFXIV')
        selected_bones = [bone.name for bone in ffxiv_col.bones]
        for bone_name in selected_bones:
            clean_bone_name = re.sub(r"\.\d+$", "", bone_name)
            bone = armature.pose.bones.get(bone_name)
            if bone:
                bone_matrix_world = armature.matrix_world @ bone.matrix
                relative_matrix = root_matrix_world.inverted() @ bone_matrix_world
                
                bone_data = {}
                bone_data["Position"] = f"{relative_matrix.translation.x:.6f}, {relative_matrix.translation.y:.6f}, {relative_matrix.translation.z:.6f}"
                bone_data["Rotation"] = f"{relative_matrix.to_quaternion().x:.6f}, {relative_matrix.to_quaternion().y:.6f}, {relative_matrix.to_quaternion().z:.6f}, {relative_matrix.to_quaternion().w:.6f}"
                bone_data["Scale"] = f"{relative_matrix.to_scale().x:.8f}, {relative_matrix.to_scale().y:.8f}, {relative_matrix.to_scale().z:.8f}"
                
                skeleton_data["Bones"][clean_bone_name] = bone_data
        
        with open(self.filepath, 'w') as f:
            json.dump(skeleton_data, f, indent=4)
        
        self.report({'INFO'}, "Pose exported successfully!")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(AETHER_OT_PoseExport)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_PoseExport)