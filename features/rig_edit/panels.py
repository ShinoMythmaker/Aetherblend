"""Panel for editing a generated rig."""
import bpy

from ...ui.tabs import get_active_tab
from ...ui.visibility import visible_in_current_area


class AETHER_PT_RigManipulation(bpy.types.Panel):
    bl_label = "Rig Manipulation"
    bl_idname = "AETHER_PT_rig_manipulation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 5

    @classmethod
    def poll(cls, context):
        if not visible_in_current_area(context):
            return False
        if get_active_tab(context) != 'GENERATE':
            return False

        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return False

        aether_rig = getattr(armature, 'aether_rig', None)
        return aether_rig and aether_rig.rigified

    def draw(self, context):
        layout = self.layout
        armature = context.active_object
        aether_rig = getattr(armature, 'aether_rig', None)


        row = layout.row(align=True)
        row.label(text="Blenderfy", icon='BLENDER')
        row.label(
            text="Converted" if aether_rig.converted else "Not Converted",
            icon='CHECKMARK' if aether_rig.converted else 'CANCEL'
        )

        row = layout.row(align=True)
        row.operator(
            "aether.rig_edit_remove_game_support",
            text="Convert",
            icon="SHADERFX",
        )

        layout.separator()

        link_collection = armature.data.collections.get('LINK')
        if not link_collection:
            layout.label(text="LINK collection not found", icon='ERROR')
            return

        row = layout.row(align=True)
        row.label(text="Inherit Scale", icon='ORIENTATION_PARENT')

        current_text = "Full"
        if aether_rig:
            scale_labels = {
                'FULL': 'Full',
                'FIX_SHEAR': 'Aligned',
                'AVERAGE': 'Average',
                'NONE': 'None',
                'NONE_LEGACY': 'None (Legacy)'
            }
            current_text = scale_labels.get(aether_rig.link_inherit_scale, 'Full')

        row.operator_menu_enum("aether.rig_edit_set_inherit_scale", "inherit_scale", text=current_text)

        layout.separator()

        row = layout.row(align=True)

        row.label(text="NoAnim Bones", icon='BONE_DATA')
        row.operator(
            "aether.rig_edit_delete_no_anim",
            text="Delete",
            icon="TRASH",
            )

def register():
    bpy.utils.register_class(AETHER_PT_RigManipulation)


def unregister():
    bpy.utils.unregister_class(AETHER_PT_RigManipulation)
