import bpy

from ...properties.tab_prop import get_active_tab
from ...utils import addon_dependencies
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

        has_meddle = addon_dependencies.is_addon_enabled(module_name="meddle", display_name="Meddle Tools")
        has_ffgear = addon_dependencies.is_addon_enabled(module_name="ffgear", display_name="FFGear")

        def draw_action_row(label: str, operator_id: str, *, enabled: bool):
            row = layout.row(align=True)
            split = row.split(factor=0.88, align=True)

            left = split.row(align=True)
            left.label(text=label, icon='ERROR' if not enabled else 'BLANK1')

            right = split.row(align=True)
            right.alignment = 'RIGHT'
            right.enabled = enabled
            right.operator(operator_id, text="", icon='NODETREE')

        draw_action_row("Meddle Shader", "aether.shader_meddle", enabled=has_meddle)
        draw_action_row("FFGear Shader", "aether.shader_ffgear", enabled=has_ffgear)

        # AB Iris/Limbal rely on Meddle-import shader context.
        draw_action_row("AB Iris Shader", "aether.shader_iris", enabled=has_meddle)
        draw_action_row("AB Limbal Shader", "aether.shader_limbal", enabled=has_meddle)
        
        


def register():
    bpy.utils.register_class(AETHER_PT_shaders)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_shaders)
        