"""Customize+ panels for C+ import, application, and axis conversion."""

import bpy

from ...ui.tabs import get_active_tab
from ...ui.visibility import visible_in_current_area


class AETHER_PT_CustomizePlus(bpy.types.Panel):
    """Provide Customize+ controls for the active armature."""

    bl_label = "Customize Plus"
    bl_idname = "AETHER_PT_customize_plus"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AetherBlend"
    bl_order = 2

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        """Show this panel for armatures with C+ settings in the C+ tab."""
        armature = context.active_object
        return bool(
            visible_in_current_area(context)
            and get_active_tab(context) == "CPLUS"
            and armature is not None
            and armature.type == "ARMATURE"
            and getattr(armature, "aether_cplus", None)
        )

    def draw(self, context: bpy.types.Context) -> None:
        """Draw the C+ import and apply controls."""
        armature = context.active_object
        if armature is None or armature.type != "ARMATURE":
            return

        settings = armature.aether_cplus
        layout = self.layout
        column = layout.column(align=True)
        if armature.data.collections.get("Original") is None:
            row = column.box().row()
            row.alignment = "CENTER"
            row.label(text="Missing Original Bone Collection", icon="ERROR")
            return

        import_row = column.row(align=True)
        import_row.operator("aether.paste_cplus_from_clipboard", text="Clipboard", icon="PASTEDOWN")
        import_row.operator("aether.parse_cplus_from_mcdf", text="MCDF", icon="IMPORT")

        column.separator()
        code_row = column.row(align=True)
        label_column = code_row.column(align=True)
        label_column.scale_x = 0.8
        label_column.label(text="C+ String")
        field_column = code_row.column(align=True)
        field_column.scale_x = 1.2
        field_column.prop(settings, "code", text="")

        if settings.code:
            column.separator()
            status = column.box().row()
            status.alignment = "CENTER"
            if settings.applied:
                status.label(text="C+ currently applied", icon="RECORD_ON")
            else:
                status.label(text="C+ not applied", icon="PAUSE")

        column.separator()
        rig_settings = getattr(armature, "aether_rig", None)
        if rig_settings and rig_settings.rigified:
            column.operator("aether.rig_generator_clean_up", text="Clean Up Rig", icon="BRUSH_DATA")
            return

        actions = column.row(align=True)
        backup_column = actions.column(align=True)
        backup_column.scale_x = 2.0
        if settings.backup_armature:
            backup_column.operator("aether.create_backup_armature", text="Update Backup", icon="RECOVER_LAST")
        else:
            backup_column.operator("aether.create_backup_armature", text="Create Backup", icon="DUPLICATE")

        arrow_column = actions.column(align=True)
        arrow_column.scale_x = 0.3
        arrow_column.label(text="→")

        apply_column = actions.column(align=True)
        apply_column.scale_x = 2.0
        apply_column.enabled = bool(settings.code) and bool(settings.backup_armature)
        if settings.applied:
            apply_column.operator("aether.revert_cplus_to_backup", text="Revert", icon="LOOP_BACK")
        else:
            apply_column.operator("aether.q_apply_cplus_string", text="Quick Apply", icon="CHECKBOX_HLT")


class AETHER_PT_CustomizePlus_AxisConversion(bpy.types.Panel):
    """Configure the axes associated with the imported character."""

    bl_label = "Axis Conversion"
    bl_idname = "AETHER_PT_customize_plus_axis_conversion"
    bl_parent_id = "AETHER_PT_customize_plus"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AetherBlend"

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        """Show axis settings when an armature has an Original collection."""
        armature = context.active_object
        return bool(
            visible_in_current_area(context)
            and get_active_tab(context) == "CPLUS"
            and armature is not None
            and armature.type == "ARMATURE"
            and getattr(armature, "aether_cplus", None)
            and armature.data.collections.get("Original") is not None
        )

    def draw(self, context: bpy.types.Context) -> None:
        """Draw the C+ axis selection controls."""
        armature = context.active_object
        settings = getattr(armature, "aether_cplus", None)
        if settings is None:
            return
        column = self.layout.column(align=True)
        column.prop(settings, "cplus_primary_axis", text="Primary")
        column.prop(settings, "cplus_secondary_axis", text="Secondary")


CLASSES = (AETHER_PT_CustomizePlus, AETHER_PT_CustomizePlus_AxisConversion)


def register() -> None:
    """Register C+ panels."""
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister() -> None:
    """Unregister C+ panels."""
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
