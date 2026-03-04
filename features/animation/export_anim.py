import bpy
import os
import tempfile
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from ...preferences import get_preferences

class AETHER_OT_AnimExport(Operator, ExportHelper):
    bl_idname = "aether.anim_export"
    bl_label = "Export Animation"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Export animation with axis conversion"
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    filename_ext = '.fbx'
    filter_glob: bpy.props.StringProperty(default='*.glb;*.fbx', options={'HIDDEN'}) # type: ignore
    
    export_format: bpy.props.EnumProperty(
        name="Format",
        items=[('FBX', "FBX", ""), ('GLB', "GLB", "")],
        default='FBX',
    ) # type: ignore
    
    def get_actions(self, context):
        if context.active_object and context.active_object.type == 'ARMATURE':
            return [(a.name, a.name, "") for a in bpy.data.actions]
        return [('NONE', "No Actions", "")]
    
    selected_action: bpy.props.EnumProperty(name="Action", items=get_actions) # type: ignore
    
    pose_primary_axis: bpy.props.EnumProperty(
        name="Primary Axis",
        items=[('X', "X", ""), ('Y', "Y", ""), ('Z', "Z", ""), 
               ('-X', "-X", ""), ('-Y', "-Y", ""), ('-Z', "-Z", "")],
        default='-Z',
    ) # type: ignore
    
    pose_secondary_axis: bpy.props.EnumProperty(
        name="Secondary Axis",
        items=[('X', "X", ""), ('Y', "Y", ""), ('Z', "Z", ""),
               ('-X', "-X", ""), ('-Y', "-Y", ""), ('-Z', "-Z", "")],
        default='Y',
    ) # type: ignore

    def invoke(self, context, event):
        if context.active_object and context.active_object.type == 'ARMATURE':
            anim_data = context.active_object.animation_data
            if anim_data and anim_data.action:
                self.selected_action = anim_data.action.name
        
        prefs = get_preferences()
        base_name = os.path.splitext(bpy.path.basename(bpy.data.filepath))[0] or "untitled"
        ext = '.fbx' if self.export_format == 'FBX' else '.glb'
        filename = base_name + ext
        
        self.filepath = os.path.join(prefs.default_anim_export_path, filename) if prefs.default_anim_export_path else filename
        return super().invoke(context, event)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "export_format", expand=True)
        layout.separator()
        layout.prop(self, "selected_action")
        layout.separator()
        layout.prop(self, "pose_primary_axis")
        layout.prop(self, "pose_secondary_axis")

    def export_fbx(self, filepath):
        bpy.ops.export_scene.fbx(
            filepath=filepath,
            use_selection=True,
            bake_anim=True,
            add_leaf_bones=False,
            primary_bone_axis=self.pose_primary_axis,
            secondary_bone_axis=self.pose_secondary_axis,
            use_armature_deform_only=True,
            bake_anim_use_all_actions=False,
            bake_anim_use_nla_strips=False,
            bake_anim_use_all_bones=True,
            bake_anim_force_startend_keying=True,
            bake_anim_simplify_factor=0.0
        )

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}
        
        if self.selected_action not in bpy.data.actions:
            self.report({'ERROR'}, "No valid action selected")
            return {'CANCELLED'}
        
        action = bpy.data.actions[self.selected_action]
        original_action = armature.animation_data.action if armature.animation_data else None
        
        if not armature.animation_data:
            armature.animation_data_create()
        armature.animation_data.action = action
        
        bpy.ops.object.mode_set(mode='OBJECT')
        original_selection = context.selected_objects.copy()
        original_active = context.view_layer.objects.active
        
        context.window.cursor_set('WAIT')
        try:
            ext = '.fbx' if self.export_format == 'FBX' else '.glb'
            filepath = os.path.splitext(self.filepath)[0] + ext
            
            if self.export_format == 'FBX':
                self.export_fbx(filepath)
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.fbx') as temp:
                    temp_path = temp.name
                
                try:
                    self.export_fbx(temp_path)
                    bpy.ops.import_scene.fbx(filepath=temp_path)
                    
                    imported = next((o for o in context.selected_objects if o.type == 'ARMATURE' and o != armature), None)
                    if not imported:
                        raise Exception("Import failed")
                    
                    if imported.animation_data and imported.animation_data.action:
                        imported.animation_data.action.name = f"Export-{action.name}"
                    
                    bpy.ops.object.select_all(action='DESELECT')
                    imported.select_set(True)
                    context.view_layer.objects.active = imported
                    
                    bpy.ops.export_scene.gltf(
                        filepath=filepath,
                        export_format='GLB',
                        use_selection=True,
                        export_yup=True,
                        export_apply=True,
                        export_animations=True,
                        export_anim_slide_to_zero=True,
                        export_animation_mode='ACTIVE_ACTIONS',
                        export_materials='NONE',
                        export_def_bones=True
                    )
                    
                    bpy.data.objects.remove(imported, do_unlink=True)
                finally:
                    try:
                        os.unlink(temp_path)
                    except:
                        pass
            
            def popup(self, context):
                self.layout.label(text=f"Action: {action.name}")
                self.layout.label(text=f"File: {os.path.basename(filepath)}")
            
            context.window_manager.popup_menu(popup, title="Export Successful", icon='CHECKMARK')
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {str(e)}")
            return {'CANCELLED'}
        finally:
            context.window.cursor_set('DEFAULT')
            
            if armature.name in bpy.data.objects and armature.animation_data:
                armature.animation_data.action = original_action
            
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