"""Panels for using a generated rig: bone collection layers, rig UI and bake settings."""
import collections

import bpy

from ...ui.tabs import get_active_tab
from ...ui.visibility import visible_in_current_area
from ..rig_generator import library


def _flatten_children(iterable):
    """Enumerate the iterator items as well as their children in the tree order."""
    for item in iterable:
        yield item
        yield from _flatten_children(item.children)


class AETHER_PT_RigLayersPanel(bpy.types.Panel):
    bl_label = "Rig Layers"
    bl_idname = "AETHER_PT_rig_layers"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 6

    @classmethod
    def poll(cls, context):
        if not visible_in_current_area(context):
            return False
        if get_active_tab(context) != 'RIG_LAYERS':
            return False

        try:
            return (context.active_object.data.get("rig_id") is not None)
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return

        if not armature.data.get("rig_id"):
            return

        layout = self.layout
        any_soloed = any(collection.is_solo for collection in armature.data.collections)

        ## AB Additions
        if context.mode == 'POSE':
            row = layout.row(align=True)
            row.operator(
                "aether.rig_ui_solo_collections",
                text="Unsolo All" if any_soloed else "Solo Selected",
                icon='SOLO_ON' if any_soloed else 'SOLO_OFF',
                depress=any_soloed,
            )
            layout.separator()

        ## Rigify UI
        layout = self.layout
        row_table = collections.defaultdict(list)
        for coll in _flatten_children(context.active_object.data.collections):
            row_id = coll.rigify_ui_row
            if row_id > 0:
                row_table[row_id].append(coll)
        col = layout.column()
        for row_id in range(min(row_table.keys()), 1 + max(row_table.keys())):
            row = col.row()
            row_buttons = row_table[row_id]
            if row_buttons:
                midpoint = len(row_buttons) / 2
                for index, coll in enumerate(row_buttons):
                    title = coll.rigify_ui_title or coll.name
                    row2 = row.row(align=True)

                    place_solo_left = index < midpoint
                    if len(row_buttons) == 1:
                        place_solo_left = False

                    if place_solo_left:
                        solo = row2.row(align=True)
                        visibility = row2.row(align=True)
                    else:
                        visibility = row2.row(align=True)
                        solo = row2.row(align=True)

                    visibility.enabled = coll.is_visible_ancestors and not any_soloed
                    visibility.prop(coll, 'is_visible', toggle=True, text=title, translate=False)
                    solo.prop(coll, 'is_solo', toggle=True, text="", icon='RADIOBUT_OFF' if not coll.is_solo else 'RADIOBUT_ON', translate=False)
            else:
                row.separator()

class AETHER_PT_RigUIPanel(bpy.types.Panel):
    bl_label = "Rig UI"
    bl_idname = "AETHER_PT_rig_ui"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 7

    @classmethod
    def poll(cls, context):
        if not visible_in_current_area(context):
            return False
        if get_active_tab(context) != 'RIG_UI':
            return False

        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return False

        rig_id = armature.data.get("rig_id")
        if not rig_id:
            return False

        panel_name = "VIEW3D_PT_rig_ui_" + rig_id
        panel_class = getattr(bpy.types, panel_name, None)

        if panel_class and hasattr(panel_class, 'poll'):
            return panel_class.poll(context)

        return False

    def draw(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return

        rig_id = armature.data.get("rig_id")
        if not rig_id:
            return

        aether_rig = getattr(armature, 'aether_rig', None)
        # if not aether_rig:
        #     return

        panel_name = "VIEW3D_PT_rig_ui_" + rig_id
        panel_class = getattr(bpy.types, panel_name, None)

        ## Draw Links
        flags = [item.value for item in aether_rig.ui_flags]

        for flag in flags:
            ui_link = library.UI_LINKS.get(flag)
            if not ui_link:
                continue
            ui_link.draw(context, self.layout)

        ## Draw Rigify UI
        if panel_class and hasattr(panel_class, 'draw'):
            panel_class.draw(self, context)
        else:
            # Fallback to default behavior if panel not found
            layout = self.layout
            layout.label(text=f"Rig UI panel not found for: {rig_id}")


class AETHER_PT_RigBakeSettingsPanel(bpy.types.Panel):
    bl_label = "Rig Bake Settings"
    bl_idname = "AETHER_PT_rig_bake_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 9

    @classmethod
    def poll(cls, context):
        if not visible_in_current_area(context):
            return False
        if get_active_tab(context) != 'RIG_UI':
            return False

        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return False

        # Get rig_id from armature custom properties
        rig_id = armature.data.get("rig_id")
        if not rig_id:
            return False

        panel_name = "VIEW3D_PT_rig_bake_settings_" + rig_id
        panel_class = getattr(bpy.types, panel_name, None)

        if panel_class and hasattr(panel_class, 'poll'):
            return panel_class.poll(context)

        return False

    def draw(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return

        # Get rig_id from armature custom properties
        rig_id = armature.data.get("rig_id")
        if not rig_id:
            return

        panel_name = "VIEW3D_PT_rig_bake_settings_" + rig_id
        panel_class = getattr(bpy.types, panel_name, None)

        if panel_class and hasattr(panel_class, 'draw'):
            panel_class.draw(self, context)
        else:
            # Fallback to default behavior if panel not found
            layout = self.layout
            layout.label(text=f"Rig bake settings panel not found for: {rig_id}")


def register():
    bpy.utils.register_class(AETHER_PT_RigLayersPanel)
    bpy.utils.register_class(AETHER_PT_RigUIPanel)
    bpy.utils.register_class(AETHER_PT_RigBakeSettingsPanel)


def unregister():
    bpy.utils.unregister_class(AETHER_PT_RigBakeSettingsPanel)
    bpy.utils.unregister_class(AETHER_PT_RigUIPanel)
    bpy.utils.unregister_class(AETHER_PT_RigLayersPanel)
