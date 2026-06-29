
"""VRM Import Operator for AetherBlend Addon."""

import re

import bpy
from bpy.props import BoolProperty, StringProperty, EnumProperty

from ... import utils
from ...utils import addon_dependencies
from ...utils.axis_conversion import AXIS_ITEMS
from ...preferences import get_preferences
from ...properties.tab_prop import set_active_tab
from ..rigging import template_manager


class AETHER_OT_VRM_Import(bpy.types.Operator):
    """Import a VRM model into Blender with various options."""
    bl_idname = "aether.vrm_import"
    bl_label = "Import VRM Model"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: StringProperty(subtype="FILE_PATH")  # type: ignore
    filter_glob: StringProperty(default='*.vrm', options={'HIDDEN'})  # type: ignore
    
    
    def invoke(self, context, event):
        prefs = get_preferences()
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def draw(self, context):
        indent = 0.3
        indent_nested = 0.3
        layout = self.layout

        # Import Settings Title
        layout.label(text="Import Settings", icon="PREFERENCES")
 
    def execute(self, context):  
        bpy.context.window.cursor_set('WAIT')   
        
        if not self.filepath or not self.filepath.lower().endswith(".vrm"): 
            self.report({'ERROR'}, "[AetherBlend] Invalid file format. Please select a .vrm file.")
            return {'CANCELLED'}   

        # Import the model
        bpy.ops.import_scene.vrm(filepath=self.filepath)

        self.report({'INFO'}, "[AetherBlend] Model imported and processed successfully.")
        
        if get_preferences().auto_navigate_tabs == 'ON':
            set_active_tab(context, 'GENERATE')
        
        bpy.context.window.cursor_set('DEFAULT')
        return {'FINISHED'}


def register():
    bpy.utils.register_class(AETHER_OT_VRM_Import)


def unregister():
    bpy.utils.unregister_class(AETHER_OT_VRM_Import)
