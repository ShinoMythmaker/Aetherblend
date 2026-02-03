import bpy
import os
import math
import tempfile
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper, axis_conversion
from mathutils import Matrix, Euler
from ...preferences import get_preferences

class AETHER_OT_AnimExport(Operator, ExportHelper):
    bl_idname = "aether.anim_export"
    bl_label = "Export Animation"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Export animation with axis conversion options"
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    filename_ext = '.fbx'
    filter_glob: bpy.props.StringProperty(default='*.glb;*.fbx', options={'HIDDEN'}) # type: ignore
    
    # Export format choice
    export_format: bpy.props.EnumProperty(
        name="Format",
        description="Choose export format",
        items=(
            ('GLB', "GLB", "Export as GLB with axis conversion via FBX intermediate"),
            ('FBX', "FBX", "Export directly as FBX with axis conversion"),
        ),
        default='FBX',
    ) # type: ignore
    
    def get_actions(self, context):
        """Get list of available actions for the active armature."""
        items = []
        if context.active_object and context.active_object.type == 'ARMATURE':
            for action in bpy.data.actions:
                items.append((action.name, action.name, ""))
        
        if not items:
            items.append(('NONE', "No Actions", ""))
        return items
    
    # Action selection
    selected_action: bpy.props.EnumProperty(
        name="Action",
        description="Select which action to export",
        items=get_actions,
    ) # type: ignore
    
    # Axis conversion properties
    use_pose_axis_conversion: bpy.props.BoolProperty(
        name="Use Axis Conversion",
        description="Apply pose axis conversion to match character import settings",
        default=True
    ) # type: ignore
    
    pose_primary_axis: bpy.props.EnumProperty(
        name="Primary Axis",
        description="Primary axis for animation export orientation. For FFXIV characters from Meddle, use -Z",
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
        description="Secondary axis for animation export orientation. For FFXIV characters from Meddle, use Y",
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

    
    def invoke(self, context, event):
        prefs = get_preferences()
        
        # Set the selected action to the currently active one
        if context.active_object and context.active_object.type == 'ARMATURE':
            if context.active_object.animation_data and context.active_object.animation_data.action:
                self.selected_action = context.active_object.animation_data.action.name
        
        blend_filename = bpy.path.basename(bpy.data.filepath) 
        if blend_filename:
            # Set extension based on export format
            ext = '.fbx' if self.export_format == 'FBX' else '.glb'
            blend_filename = os.path.splitext(blend_filename)[0] + ext
        else:
            blend_filename = "untitled.glb"  
        
        if prefs.default_anim_export_path:
            self.filepath = os.path.join(prefs.default_anim_export_path, blend_filename)
        else:
            self.filepath = blend_filename
        
        return super().invoke(context, event)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "export_format", expand=True)
        layout.separator()
        layout.prop(self, "selected_action")
        layout.separator()
        layout.prop(self, "use_pose_axis_conversion")
        
        if self.use_pose_axis_conversion:
            col = layout.column(align=True)
            col.prop(self, "pose_primary_axis")
            col.prop(self, "pose_secondary_axis")


    def execute(self, context):
        if not context.active_object or context.active_object.type != 'ARMATURE':
            self.report({'ERROR'}, "Please select an armature to export animations from.")
            return {'CANCELLED'}
        
        original_armature = context.active_object
        
        # Get the selected action
        if self.selected_action == 'NONE' or self.selected_action not in bpy.data.actions:
            self.report({'ERROR'}, "No valid action selected.")
            return {'CANCELLED'}
        
        selected_action = bpy.data.actions[self.selected_action]
        action_name = selected_action.name
        
        # Temporarily set this as the active action
        original_action = original_armature.animation_data.action if original_armature.animation_data else None
        if not original_armature.animation_data:
            original_armature.animation_data_create()
        original_armature.animation_data.action = selected_action
        
        # Set wait cursor
        context.window_manager.progress_begin(0, 100)
        context.window.cursor_set('WAIT')
        
        original_selection = context.selected_objects.copy()
        original_active = context.view_layer.objects.active
        imported_armature = None
        imported_action = None
        
        try:
            # If FBX format, export directly
            if self.export_format == 'FBX':
                # Update file extension if needed
                filepath = self.filepath
                if not filepath.lower().endswith('.fbx'):
                    filepath = os.path.splitext(filepath)[0] + '.fbx'
                
                if self.use_pose_axis_conversion:
                    bpy.ops.export_scene.fbx(
                        filepath=filepath,
                        use_selection=True,
                        bake_anim=True,
                        add_leaf_bones=False,
                        primary_bone_axis=self.pose_primary_axis,
                        secondary_bone_axis=self.pose_secondary_axis,
                        use_armature_deform_only=False,
                        bake_anim_use_all_actions=False,
                        bake_anim_use_nla_strips=False,
                        bake_anim_use_all_bones=True,
                        bake_anim_force_startend_keying=True,
                    )
                else:
                    bpy.ops.export_scene.fbx(
                        filepath=filepath,
                        use_selection=True,
                        bake_anim=True,
                        add_leaf_bones=False,
                        use_armature_deform_only=False,
                        bake_anim_use_all_actions=False,
                        bake_anim_use_nla_strips=False,
                        bake_anim_use_all_bones=True,
                        bake_anim_force_startend_keying=True,
                    )
                
                self.report({'INFO'}, f"FBX exported to {filepath} with action '{action_name}'")
                
                # Show completion popup
                def draw_popup(self, context):
                    self.layout.label(text=f"Action: {action_name}")
                    self.layout.label(text=f"File: {os.path.basename(filepath)}")
                
                context.window_manager.popup_menu(draw_popup, title="Export Successful", icon='CHECKMARK')
                
                return {'FINISHED'}
            
            # GLB format with axis conversion via FBX intermediate
            # Update file extension if needed
            filepath = self.filepath
            if not filepath.lower().endswith('.glb'):
                filepath = os.path.splitext(filepath)[0] + '.glb'
            
            # If axis conversion is enabled, use FBX intermediate workflow
            if self.use_pose_axis_conversion:
                # Check for FFXIV collection
                ffxiv_col = original_armature.data.collections.get('FFXIV')
                if not ffxiv_col:
                    self.report({'ERROR'}, "FFXIV bone collection not found")
                    return {'CANCELLED'}
                
                ffxiv_bone_names = set(bone.name for bone in ffxiv_col.bones)
                
                # Create temp FBX file
                temp_fbx = tempfile.NamedTemporaryFile(delete=False, suffix='.fbx')
                temp_fbx_path = temp_fbx.name
                temp_fbx.close()
                
                # Export to FBX with axis conversion
                bpy.ops.export_scene.fbx(
                    filepath=temp_fbx_path,
                    use_selection=True,
                    bake_anim=True,
                    add_leaf_bones=False,
                    primary_bone_axis=self.pose_primary_axis,
                    secondary_bone_axis=self.pose_secondary_axis,
                    use_armature_deform_only=False,
                    bake_anim_use_all_actions=False,
                    bake_anim_use_nla_strips=False,
                    bake_anim_use_all_bones=True,
                    bake_anim_force_startend_keying=True,
                )
                
                # Import FBX back
                bpy.ops.import_scene.fbx(filepath=temp_fbx_path)
                
                # Find the imported armature and action
                imported_armature = None
                imported_action = None
                for obj in context.selected_objects:
                    if obj.type == 'ARMATURE' and obj != original_armature:
                        imported_armature = obj
                        if obj.animation_data and obj.animation_data.action:
                            imported_action = obj.animation_data.action
                        break
                
                if not imported_armature:
                    raise Exception("Failed to find imported armature")
                
                # Rename the imported action
                if imported_action:
                    new_action_name = f"Export-{action_name}"
                    imported_action.name = new_action_name
                    
                    # Ensure only this action is active
                    if imported_armature.animation_data:
                        imported_armature.animation_data.action = imported_action
                
                # Enter edit mode and remove non-FFXIV bones
                bpy.ops.object.select_all(action='DESELECT')
                imported_armature.select_set(True)
                context.view_layer.objects.active = imported_armature
                bpy.ops.object.mode_set(mode='EDIT')
                
                bones_to_remove = [bone for bone in imported_armature.data.edit_bones 
                                   if bone.name not in ffxiv_bone_names]
                for bone in bones_to_remove:
                    imported_armature.data.edit_bones.remove(bone)
                
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Make absolutely sure only the imported armature is selected
                bpy.ops.object.select_all(action='DESELECT')
                imported_armature.select_set(True)
                context.view_layer.objects.active = imported_armature
                
                # Export cleaned armature to GLB with ONLY the active action
                bpy.ops.export_scene.gltf(
                    filepath=filepath,
                    export_format='GLB',
                    use_selection=True,
                    use_visible=False,
                    use_active_collection=False,
                    export_yup=True,
                    export_apply=True,
                    export_animations=True,
                    export_frame_range=False,
                    export_anim_slide_to_zero=True,
                    export_animation_mode='ACTIVE_ACTIONS',
                    export_optimize_animation_size=False,
                    export_optimize_animation_keep_anim_armature=True,
                    export_optimize_animation_keep_anim_object=True,
                    export_materials='NONE'
                )
                
                # Clean up imported armature and action
                bpy.data.objects.remove(imported_armature, do_unlink=True)
                if imported_action:
                    bpy.data.actions.remove(imported_action)
                
                # Clean up temp file
                try:
                    os.unlink(temp_fbx_path)
                except:
                    pass
                    
            else:
                # No conversion, direct GLB export
                bpy.ops.export_scene.gltf(
                    filepath=filepath,
                    export_format='GLB',
                    use_selection=True,
                    export_yup=True,
                    export_apply=True,
                    export_animations=True,
                    export_frame_range=False,
                    export_anim_slide_to_zero=True,
                    export_animation_mode='ACTIONS',
                    export_optimize_animation_size=False,
                    export_optimize_animation_keep_anim_armature=True,
                    export_optimize_animation_keep_anim_object=True,
                    export_materials='NONE'
                )
            
            # Show completion popup
            def draw_popup(self, context):
                self.layout.label(text=f"Action: {action_name}")
                self.layout.label(text=f"File: {os.path.basename(filepath)}")
            
            context.window_manager.popup_menu(draw_popup, title="Export Successful", icon='CHECKMARK')
            
            self.report({'INFO'}, f"GLB exported to {filepath} with action '{action_name}'")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {str(e)}")
            return {'CANCELLED'}
            
        finally:
            # Restore cursor and progress
            context.window.cursor_set('DEFAULT')
            context.window_manager.progress_end()
            
            # Restore original action
            if original_armature and original_armature.name in bpy.data.objects:
                if original_armature.animation_data:
                    original_armature.animation_data.action = original_action
            
            # Restore original selection
            bpy.ops.object.select_all(action='DESELECT')
            for obj in original_selection:
                if obj.name in bpy.data.objects:
                    obj.select_set(True)
            if original_active and original_active.name in bpy.data.objects:
                context.view_layer.objects.active = original_active
        

def register():
    bpy.utils.register_class(AETHER_OT_AnimExport)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_AnimExport)