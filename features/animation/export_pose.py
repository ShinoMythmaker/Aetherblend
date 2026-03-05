import bpy
import json
import os
import re
import math
import base64
import tempfile
from bpy.types import Operator
from bpy.props import BoolProperty
from bpy_extras.io_utils import ExportHelper, axis_conversion
from mathutils import Matrix, Euler
from ...preferences import get_preferences


def pose_export_image_items(_self, _context):
    items = [('__NONE__', "None", "Do not embed an image")]
    for image in bpy.data.images:
        items.append((image.name, image.name, ""))
    return items


class AETHER_OT_PoseExport(Operator, ExportHelper):
    """Exports armature pose into a .pose file."""
    bl_idname = "aether.pose_export"
    bl_label = "Export to Pose File"
    bl_options = {'REGISTER'}
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    filename_ext = '.pose'
    filter_glob: bpy.props.StringProperty(default='*.pose', options={'HIDDEN'}) # type: ignore
    
    # Axis conversion properties
    use_pose_axis_conversion: BoolProperty(
        name="Use Axis Conversion",
        description="Apply pose axis conversion to match character import settings",
        default=True
    ) # type: ignore
    
    pose_primary_axis: bpy.props.EnumProperty(
        name="Primary Axis",
        description="Primary axis for pose export orientation. For FFXIV characters from Meddle, use -Z",
        items=(
            ('X', "X Axis", ""),
            ('Y', "Y Axis", ""),
            ('Z', "Z Axis", ""),
            ('-X', "-X Axis", ""),
            ('-Y', "-Y Axis", ""),
            ('-Z', "-Z Axis", ""),
        ),
        default='X',
    ) # type: ignore
    
    pose_secondary_axis: bpy.props.EnumProperty(
        name="Secondary Axis",
        description="Secondary axis for pose export orientation. For FFXIV characters from Meddle, use Y",
        items=(
            ('X', "X Axis", ""),
            ('Y', "Y Axis", ""),
            ('Z', "Z Axis", ""),
            ('-X', "-X Axis", ""),
            ('-Y', "-Y Axis", ""),
            ('-Z', "-Z Axis", ""),
        ),
        default='Y',
    ) # type: ignore

    pose_author: bpy.props.StringProperty(
        name="Author",
        description="Author name written to the pose file",
        default="",
    ) # type: ignore

    pose_description: bpy.props.StringProperty(
        name="Description",
        description="Description written to the pose file",
        default="",
    ) # type: ignore

    pose_version: bpy.props.StringProperty(
        name="Pose Version",
        description="Pose version string written to the pose file (example: 1.0.0)",
        default="1.0.0",
    ) # type: ignore

    pose_tags: bpy.props.StringProperty(
        name="Tags",
        description="Comma-separated tags written to the pose file",
        default="",
    ) # type: ignore

    include_preview_image: BoolProperty(
        name="Include Preview Image",
        description="Embed a selected Blender image as Base64Image in the pose file",
        default=True,
    ) # type: ignore

    preview_image_name: bpy.props.EnumProperty(
        name="Preview Image",
        description="Image datablock to embed into the pose file",
        items=pose_export_image_items,
    ) # type: ignore
    
    
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

        # Default to Blender's latest render result when available.
        render_result = bpy.data.images.get("Render Result")
        self.preview_image_name = render_result.name if render_result else '__NONE__'
        
        return super().invoke(context, event)

    def _encode_image_to_base64(self, context, image):
        if not image:
            return None

        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                temp_path = temp_file.name

            if image.type == 'RENDER_RESULT':
                image.save_render(temp_path, scene=context.scene)
            else:
                # save_render works for most image datablocks and avoids mutating image settings.
                image.save_render(temp_path, scene=context.scene)

            with open(temp_path, 'rb') as f:
                return base64.b64encode(f.read()).decode('ascii')
        except Exception as ex:
            self.report({'WARNING'}, f"Could not embed preview image: {ex}")
            return None
        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass
    
    
    def execute(self, context):
        armature = context.object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "No armature selected")
            return {'CANCELLED'}
        
        # Build axis conversion
        pose_correction_matrix = Matrix.Identity(4)
        if self.use_pose_axis_conversion:
            pose_correction_matrix = axis_conversion(
                from_up=self.pose_primary_axis,         # Primary
                from_forward=self.pose_secondary_axis,  # Secondary
                to_up='Y',                              # Target Primary
                to_forward='X',                         # Target Secondary
            ).to_4x4()
        
        x_rotation = Matrix.Rotation(math.radians(-90), 4, 'X')

        tags = [tag.strip() for tag in self.pose_tags.split(',') if tag.strip()]
        
        skeleton_data = {
            "Author": self.pose_author,
            "Description": self.pose_description,
            "Version": self.pose_version,
            "Tags": tags,
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
                # Get bone matrix in world space
                bone_matrix_world = armature.matrix_world @ bone.matrix
                
                # Apply axis conversion
                if self.use_pose_axis_conversion:
                    bone_matrix_world = bone_matrix_world @ pose_correction_matrix
                
                # Flip for FFXIV
                bone_matrix_world = x_rotation @ bone_matrix_world
                
                bone_data = {}
                bone_data["Position"] = f"{bone_matrix_world.translation.x:.6f}, {bone_matrix_world.translation.y:.6f}, {bone_matrix_world.translation.z:.6f}"
                bone_data["Rotation"] = f"{bone_matrix_world.to_quaternion().x:.6f}, {bone_matrix_world.to_quaternion().y:.6f}, {bone_matrix_world.to_quaternion().z:.6f}, {bone_matrix_world.to_quaternion().w:.6f}"
                bone_data["Scale"] = f"{bone_matrix_world.to_scale().x:.8f}, {bone_matrix_world.to_scale().y:.8f}, {bone_matrix_world.to_scale().z:.8f}"
                
                skeleton_data["Bones"][clean_bone_name] = bone_data

        preview_image = None
        if self.preview_image_name and self.preview_image_name != '__NONE__':
            preview_image = bpy.data.images.get(self.preview_image_name)
        if not preview_image:
            preview_image = bpy.data.images.get("Render Result")
        if self.include_preview_image and preview_image:
            encoded_image = self._encode_image_to_base64(context, preview_image)
            if encoded_image:
                skeleton_data["Base64Image"] = encoded_image
        
        with open(self.filepath, 'w') as f:
            json.dump(skeleton_data, f, indent=4)
        
        self.report({'INFO'}, "Pose exported successfully!")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(AETHER_OT_PoseExport)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_PoseExport)