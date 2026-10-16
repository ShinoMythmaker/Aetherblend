import bpy

from ...ui.tabs import get_active_tab
from ...ui.visibility import visible_in_current_area
from ...utils import addon_dependencies


class AETHER_PT_RigCreation(bpy.types.Panel):
    bl_label = "Create Rig"
    bl_idname = "AETHER_PT_rig_creation_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 4

    @classmethod
    def poll(cls, context):
        if not visible_in_current_area(context):
            return False
        if get_active_tab(context) != 'GENERATE':
            return False

        armature = context.active_object
        return (
            armature is not None
            and armature.visible_get()
            and armature.type == 'ARMATURE'
            and getattr(armature, 'aether_rig', None)
        )

    def draw(self, context):
        addon_enabled = addon_dependencies.is_addon_enabled(module_name="rigify")
        if not addon_enabled:
            layout = self.layout
            box = layout.box()
            box.label(text="Rigify addon is not enabled", icon='ERROR')
            return None

        layout = self.layout
        armature = context.active_object
        aether_rig = getattr(armature, 'aether_rig', None)
        if not aether_rig:
            return

        col = layout.column(align=True)

        full_rig_button = col.row(align=True)
        full_rig_button.scale_y = 1.3
        if aether_rig.rigified:
            full_rig_button.operator("aether.rig_generator_generate_full", text="Regenerate", icon="FILE_REFRESH")
        else:
            full_rig_button.operator("aether.rig_generator_generate_full", text="Generate Rig", icon="PLAY")

        unlink = full_rig_button.column(align=False)
        unlink.scale_x = 1.3
        unlink.operator("aether.rig_generator_clean_up", text="", icon="UNLINKED")


        reset = full_rig_button.column(align=False)
        reset.scale_x = 1.3
        reset.operator("aether.rig_generator_reset", text="", icon="RESTRICT_INSTANCED_ON")

        meta_rig_button = col.row(align=True)
        meta_rig_button.scale_y = 0.95
        meta_rig_button.operator("aether.rig_generator_generate_meta", text="Generate Meta Rig", icon="ARMATURE_DATA")

        row = layout.row(align=True)
        row.label(text="Template", icon='PRESET')
        row.prop(aether_rig, "template", text="")

        row = layout.row(align=True)
        row.label(text="Colorset", icon='COLOR')
        row.prop(aether_rig, "selected_colorset", text="")


def register():
    bpy.utils.register_class(AETHER_PT_RigCreation)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_RigCreation)
