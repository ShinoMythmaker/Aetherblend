
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

    s_import_collection: BoolProperty(name="Import-Collection", description="Stores all import in a seperatre Collection", default=True)  # type: ignore
    s_cleanup_colliders: BoolProperty(name="Cleanup Colliders", description="Removes colliders from the imported model", default=True)  # type: ignore
    s_hide_toon_shaders: BoolProperty(name="Hide Toon Shaders", description="Hides toon shaders from the imported model", default=True)  # type: ignore
    
    
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

        # Import Options Section
        box = layout.box()
        row = box.row()
        row.label(text="VRM Import", icon="IMPORT")

        col = box.column(align=True)

        split = col.split(factor=indent)  
        split.label(text=" ")
        split.prop(self, "s_import_collection")

        split = col.split(factor=indent)
        split.label(text=" ")
        split.prop(self, "s_cleanup_colliders")

        split = col.split(factor=indent)
        split.label(text=" ")
        split.prop(self, "s_hide_toon_shaders")
 
    def execute(self, context):  
        bpy.context.window.cursor_set('WAIT')   
        
        if not self.filepath or not self.filepath.lower().endswith(".vrm"): 
            self.report({'ERROR'}, "[AetherBlend] Invalid file format. Please select a .vrm file.")
            return {'CANCELLED'}   

        # Import the model
        imported_objects = utils.import_export.import_vrm(filepath=self.filepath)

        # Process the imported objects with settings in mind
        if self.s_import_collection:
            import_collection = utils.collection.create_collection("Model_Import")
            import_collection.color_tag = "COLOR_05"
            utils.collection.link_to_collection(imported_objects, import_collection)

        if self.s_cleanup_colliders:
            _remove_colliders(imported_objects)

        if self.s_hide_toon_shaders:
            _hide_toon_shaders(imported_objects)

        bpy.ops.object.select_all(action='DESELECT')

        armature = utils.armature.find_armature_in_objects(imported_objects)
        if armature:
            utils.object.select_only(armature)

            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.armature.select_all(action='SELECT')
            bpy.ops.armature.assign_to_collection(new_collection_name="Original")
            bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, "[AetherBlend] Model imported and processed successfully.")
        
        if get_preferences().auto_navigate_tabs == 'ON':
            set_active_tab(context, 'GENERATE')
        
        bpy.context.window.cursor_set('DEFAULT')
        return {'FINISHED'}
    

def _hide_toon_shaders(objects):
    """Hides toon shaders in the imported objects."""
    ## check each object for modfiers with the string "MToon Outline" in there name and disbale there visibility in the viewport
    for obj in objects:
        for mod in obj.modifiers:
            if "MToon Outline" in mod.name:
                mod.show_viewport = False

def _remove_colliders(objects):
    """Removes colliders from the imported objects."""
    ## Delete all objects with the word "collider" in their name (case-insensitive)
    colliders = [obj for obj in objects if re.search(r'collider', obj.name, re.IGNORECASE)]
    bpy.ops.object.select_all(action='DESELECT')
    for collider in colliders:
        collider.select_set(True)
    bpy.ops.object.delete()


def register():
    bpy.utils.register_class(AETHER_OT_VRM_Import)


def unregister():
    bpy.utils.unregister_class(AETHER_OT_VRM_Import)
