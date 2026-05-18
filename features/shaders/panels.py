import bpy

from ...properties.tab_prop import get_active_tab
from ...utils.ui_visibility import visible_in_current_area



class AETHER_PT_shaders(bpy.types.Panel):
    bl_label = "Shaders"
    bl_idname = "AETHER_PT_shaders"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 6

    @classmethod
    def poll(cls, context):
        if not visible_in_current_area(context):
            return False
        if get_active_tab(context) != 'GENERATE':
            return False

        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return False
        
        return True

    def draw(self, context):
        layout = self.layout

        # create button for setting up iris node group
        row = layout.row()
        row.operator("aether.shader_iris", text="AB Iris Shader", icon='NODETREE')
        row = layout.row()
        row.operator("aether.shader_limbal", text="AB Limbal Shader", icon='NODETREE')


def register():
    bpy.utils.register_class(AETHER_PT_shaders)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_shaders)
        