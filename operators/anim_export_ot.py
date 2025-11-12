import bpy
import os
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper  
from ..preferences import get_preferences

class AETHER_OT_AnimExport(Operator, ExportHelper):
    bl_idname = "aether.anim_export"
    bl_label = "Export Animation (GLB)"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Export animation as GLB with all actions"
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    filename_ext = '.glb'
    filter_glob: bpy.props.StringProperty(default='*.glb', options={'HIDDEN'}) # type: ignore

    
    def invoke(self, context, event):
        prefs = get_preferences()  
        blend_filename = bpy.path.basename(bpy.data.filepath) 
        if blend_filename:
            blend_filename = os.path.splitext(blend_filename)[0] + ".glb"  
        else:
            blend_filename = "untitled.glb"  
        
        if prefs.default_anim_export_path:
            self.filepath = os.path.join(prefs.default_anim_export_path, blend_filename)
        else:
            self.filepath = blend_filename
        
        return super().invoke(context, event)


    def execute(self, context):
        if not context.active_object or context.active_object.type != 'ARMATURE':
            self.report({'ERROR'}, "Please select an armature to export animations from.")
            return {'CANCELLED'}
        
        if not bpy.data.actions:
            self.report({'WARNING'}, "No actions found to export.")
            return {'CANCELLED'}
        
        try:
            bpy.ops.export_scene.gltf(
                filepath=self.filepath,
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
            
            action_count = len(bpy.data.actions)
            self.report({'INFO'}, f"GLB exported to {self.filepath} with {action_count} action(s)")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {str(e)}")
            return {'CANCELLED'}
        

def register():
    bpy.utils.register_class(AETHER_OT_AnimExport)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_AnimExport)