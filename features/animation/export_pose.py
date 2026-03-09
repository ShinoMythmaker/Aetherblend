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

    preview_source: bpy.props.EnumProperty(
        name="Preview Source",
        description="Source used for Base64Image",
        items=(
            ('AUTO_VIEWPORT', "Auto Viewport", "Generate from current viewport"),
            ('RENDER_RESULT', "Render Result", "Use Blender Render Result image"),
            ('BLENDER_IMAGE', "Blend Image", "Choose an image datablock"),
            ('EXTERNAL_FILE', "External File", "Load image from disk"),
        ),
        default='AUTO_VIEWPORT',
    ) # type: ignore

    preview_image_name: bpy.props.EnumProperty(
        name="Preview Image",
        description="Image datablock to embed into the pose file",
        items=pose_export_image_items,
    ) # type: ignore

    preview_external_path: bpy.props.StringProperty(
        name="External Image Path",
        description="Path to an external image file",
        default="",
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

    def draw(self, _context):
        layout = self.layout
        axis_box = layout.box()
        axis_box.label(text="Axis")
        axis_box.prop(self, "use_pose_axis_conversion")
        axis_box.prop(self, "pose_primary_axis")
        axis_box.prop(self, "pose_secondary_axis")

        pose_box = layout.box()
        pose_box.label(text="Pose File Data")
        pose_box.prop(self, "pose_author")
        pose_box.prop(self, "pose_description")
        pose_box.prop(self, "pose_version")
        pose_box.prop(self, "pose_tags")
        pose_box.prop(self, "include_preview_image")
        if self.include_preview_image:
            pose_box.prop(self, "preview_source")
            if self.preview_source == 'BLENDER_IMAGE':
                pose_box.prop(self, "preview_image_name")
            elif self.preview_source == 'EXTERNAL_FILE':
                pose_box.prop(self, "preview_external_path")

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

    def _encode_file_to_base64(self, file_path):
        try:
            path = bpy.path.abspath(file_path)
            if not path or not os.path.isfile(path):
                return None
            with open(path, 'rb') as f:
                return base64.b64encode(f.read()).decode('ascii')
        except Exception as ex:
            self.report({'WARNING'}, f"Could not embed external image: {ex}")
            return None

    def _encode_viewport_to_base64(self, context):
        try:
            override = None
            viewport_space = None
            for window in context.window_manager.windows:
                screen = window.screen
                for area in screen.areas:
                    if area.type != 'VIEW_3D':
                        continue
                    if not area.spaces:
                        continue
                    space = area.spaces[0]
                    for region in area.regions:
                        if region.type == 'WINDOW':
                            override = {
                                "window": window,
                                "screen": screen,
                                "area": area,
                                "region": region,
                                "scene": context.scene,
                            }
                            viewport_space = space
                            break
                    if override:
                        break
                if override:
                    break

            if not override:
                return None

            old_armature_visibility = None
            if viewport_space and hasattr(viewport_space, "show_object_viewport_armature"):
                old_armature_visibility = viewport_space.show_object_viewport_armature
                viewport_space.show_object_viewport_armature = False

            try:
                with context.temp_override(**override):
                    bpy.ops.render.opengl(write_still=False, view_context=True)
            finally:
                if old_armature_visibility is not None and viewport_space and hasattr(viewport_space, "show_object_viewport_armature"):
                    viewport_space.show_object_viewport_armature = old_armature_visibility

            render_result = bpy.data.images.get("Render Result")
            if not render_result:
                return None
            return self._encode_image_to_base64(context, render_result)
        except Exception as ex:
            self.report({'WARNING'}, f"Could not generate viewport preview: {ex}")
            return None

    def _get_preview_base64(self, context):
        if self.preview_source == 'AUTO_VIEWPORT':
            encoded = self._encode_viewport_to_base64(context)
            if encoded:
                return encoded
            render_result = bpy.data.images.get("Render Result")
            return self._encode_image_to_base64(context, render_result) if render_result else None

        if self.preview_source == 'RENDER_RESULT':
            render_result = bpy.data.images.get("Render Result")
            return self._encode_image_to_base64(context, render_result) if render_result else None

        if self.preview_source == 'BLENDER_IMAGE':
            image = None
            if self.preview_image_name and self.preview_image_name != '__NONE__':
                image = bpy.data.images.get(self.preview_image_name)
            return self._encode_image_to_base64(context, image) if image else None

        if self.preview_source == 'EXTERNAL_FILE':
            return self._encode_file_to_base64(self.preview_external_path)

        return None
    
    
    def execute(self, context):
        armature = context.object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "No armature selected")
            return {'CANCELLED'}
        
        pose_correction_matrix = Matrix.Identity(4)
        if self.use_pose_axis_conversion:
            pose_correction_matrix = axis_conversion(
                from_up=self.pose_primary_axis,
                from_forward=self.pose_secondary_axis,
                to_up='Y',
                to_forward='X',
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
                bone_matrix_world = armature.matrix_world @ bone.matrix
                if self.use_pose_axis_conversion:
                    bone_matrix_world = bone_matrix_world @ pose_correction_matrix
                bone_matrix_world = x_rotation @ bone_matrix_world
                
                bone_data = {}
                bone_data["Position"] = f"{bone_matrix_world.translation.x:.6f}, {bone_matrix_world.translation.y:.6f}, {bone_matrix_world.translation.z:.6f}"
                bone_data["Rotation"] = f"{bone_matrix_world.to_quaternion().x:.6f}, {bone_matrix_world.to_quaternion().y:.6f}, {bone_matrix_world.to_quaternion().z:.6f}, {bone_matrix_world.to_quaternion().w:.6f}"
                bone_data["Scale"] = f"{bone_matrix_world.to_scale().x:.8f}, {bone_matrix_world.to_scale().y:.8f}, {bone_matrix_world.to_scale().z:.8f}"
                
                skeleton_data["Bones"][clean_bone_name] = bone_data

        if self.include_preview_image:
            encoded_image = self._get_preview_base64(context)
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