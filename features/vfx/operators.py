import bpy
import os
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper  
from ...preferences import get_preferences

class AETHER_OT_VFXExport(Operator, ExportHelper):
    bl_idname = "aether.vfx_export"
    bl_label = "Export VFX Model (GLB)"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Export VFX model as GLB with modifiers applied"
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    filename_ext = '.glb'
    filter_glob: bpy.props.StringProperty(default='*.glb', options={'HIDDEN'}) # type: ignore

    
    def invoke(self, context, event):
        prefs = get_preferences()  
        blend_filename = bpy.path.basename(bpy.data.filepath) 
        if blend_filename:
            blend_filename = os.path.splitext(blend_filename)[0] + "_vfx.glb"  
        else:
            blend_filename = "untitled_vfx.glb"  
        
        if prefs.default_vfx_export_path:
            self.filepath = os.path.join(prefs.default_vfx_export_path, blend_filename)
        else:
            self.filepath = blend_filename
        
        return super().invoke(context, event)


    def execute(self, context):
        if not context.selected_objects:
            self.report({'ERROR'}, "Please select objects to export.")
            return {'CANCELLED'}
        
        try:
            bpy.ops.export_scene.gltf(
                filepath=self.filepath,
                export_format='GLB',
                use_selection=True,
                export_yup=True,  # Y up enabled for VFX
                export_apply=True,
                export_animations=False,
                export_normals=True,
                export_tangents=True,  # Keep tangents
                export_attributes=True,
                export_materials='EXPORT',
                export_image_format='AUTO'
            )
            
            self.report({'INFO'}, f"VFX model exported to {self.filepath}")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {str(e)}")
            return {'CANCELLED'}
        

def register():
    bpy.utils.register_class(AETHER_OT_VFXExport)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_VFXExport)
