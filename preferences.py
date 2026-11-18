"""Add-on preferences and additional plugin status."""

import bpy
from bpy.props import EnumProperty, StringProperty

from .utils import addon_dependencies

TOGGLE_ITEMS = [("ON", "Enable", ""), ("OFF", "Disable", "")]
GITHUB_URL = "https://github.com/ShinoMythmaker/Aetherblend"
DISCORD_URL = "https://discord.gg/NEF7TdXGqH"
PATREON_URL = "https://www.patreon.com/ShinoMythmaker"


def get_preferences() -> bpy.types.AddonPreferences:
    """Retrieve addon preferences."""
    return bpy.context.preferences.addons[__package__].preferences


class AetherBlendPreferences(bpy.types.AddonPreferences):
    """Addon preferences for AetherBlend."""

    bl_idname = __package__

    tabs: EnumProperty(
        name="Tabs",
        description="Select a preference tab",
        items=[
            ("GENERAL", "General", "General addon settings"),
            ("PATHS", "Paths", "Set default paths for various functions"),
            ("CONTRIBUTION", "Contribution", "How to support and contribute"),
        ],
        default="GENERAL",
    )  # type: ignore

    # General Settings
    auto_navigate_tabs: EnumProperty(
        name="Auto Navigate Tabs",
        description="Automatically switch to relevant tabs after operations (Import → Generate, Link → Rig Layers)",
        items=TOGGLE_ITEMS,
        default="ON",
    )  # type: ignore

    show_n_panel: EnumProperty(
        name="Show N-Panel UI",
        description="Show AetherBlend panels in the 3D View sidebar",
        items=TOGGLE_ITEMS,
        default="ON",
    )  # type: ignore

    show_properties_tool_tab: EnumProperty(
        name="Show Properties Tool UI",
        description="Show AetherBlend panels in the Properties editor Tool context",
        items=TOGGLE_ITEMS,
        default="ON",
    )  # type: ignore

    # Default File Paths
    default_meddle_import_path: StringProperty(
        name="Meddle Import", subtype="DIR_PATH", description="Select the default directory for importing Meddle files"
    )  # type: ignore

    default_cplus_import_path: StringProperty(
        name="C+ Import", subtype="DIR_PATH", description="Select the default directory for importing MCDF files"
    )  # type: ignore

    default_pose_export_path: StringProperty(
        name="Pose Export", subtype="DIR_PATH", description="Select the default directory for saving pose files"
    )  # type: ignore

    default_anim_export_path: StringProperty(
        name="Anim Export", subtype="DIR_PATH", description="Select the default directory for saving animation files"
    )  # type: ignore

    default_vfx_export_path: StringProperty(
        name="VFX Export", subtype="DIR_PATH", description="Select the default directory for saving VFX files"
    )  # type: ignore

    # default_pose_import_path: StringProperty(
    #     name="Pose Import",
    #     subtype='DIR_PATH',
    #     description="Select the default directory for importing pose files"
    # ) #type: ignore

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout

        def draw_switch(parent: bpy.types.UILayout, prop_name: str, label: str) -> None:
            row = parent.row(align=True)
            split = row.split(factor=0.72, align=True)
            split.label(text=label)
            toggle = split.row(align=True)
            toggle.prop(self, prop_name, expand=True)

        dependency_col = layout.column(align=True)
        dependency_col.label(text="Additional Plugins", icon="PLUGIN")

        missing_required = addon_dependencies.get_missing_required_addons()
        if missing_required:
            dependency_col.label(
                text="Rig generation requires Rigify. Install or enable it below.",
                icon="ERROR",
            )
        else:
            dependency_col.label(text="Rigify is enabled for rig generation", icon="CHECKMARK")

        for addon in addon_dependencies.ADDONS:
            box = dependency_col.box()
            row = box.row(align=True)
            row.label(text=addon.name)
            row.label(text="Required" if addon.required else "Optional")
            status = addon_dependencies.get_addon_status(addon)
            if status == "ENABLED":
                row.label(text="Enabled", icon="CHECKMARK")
            elif status == "INACTIVE":
                row.label(text="Inactive", icon="PAUSE")
                module = addon_dependencies.resolve_addon_module_name(module_name=addon.module, display_name=addon.name)
                row.operator("preferences.addon_enable", text="Enable", icon="CHECKMARK").module = module
            else:
                row.label(text="Missing", icon="ERROR" if addon.required else "INFO")
            # box.label(text=addon.purpose)
            row.operator("wm.url_open", text="Documentation" if addon.builtin else "GitHub", icon="URL").url = addon.url

        layout.separator()

        row = layout.row()
        row.prop(self, "tabs", expand=True)

        if self.tabs == "GENERAL":
            box = layout.box()
            box.label(text="General Settings", icon="SETTINGS")

            box.separator()
            draw_switch(box, "auto_navigate_tabs", "Auto Navigate Tabs")
            box.separator()
            draw_switch(box, "show_n_panel", "Show N-Panel UI")
            draw_switch(box, "show_properties_tool_tab", "Show Properties Tool UI")

        elif self.tabs == "PATHS":
            box = layout.box()
            box.label(text="Default File Paths", icon="FILE_FOLDER")
            box.prop(self, "default_meddle_import_path")
            box.prop(self, "default_cplus_import_path")
            # box.prop(self, "default_pose_import_path")
            box.prop(self, "default_pose_export_path")
            box.prop(self, "default_anim_export_path")
            box.prop(self, "default_vfx_export_path")

        elif self.tabs == "CONTRIBUTION":
            main_box = layout.box()
            main_box.label(text="Contribution", icon="HEART")

            split = main_box.split(factor=0.68, align=False)
            left = split.column(align=True)
            right = split.column(align=True)
            left.label(text="Support us on Patreon!")
            left.label(text="Supporters in the highest tier (`Mythmaker`) are listed below.")
            left.separator()
            left.label(text="- Zed")
            left.label(text="- PancakePapi")
            left.label(text="- Pizzadabbin")
            left.label(text="- Djaal")

            right.separator()
            right.operator("wm.url_open", text="GitHub Issues", icon="URL").url = f"{GITHUB_URL}/issues"
            right.operator("wm.url_open", text="Discord", icon="COMMUNITY").url = DISCORD_URL
            right.operator("wm.url_open", text="Repository", icon="FILEBROWSER").url = GITHUB_URL
            right.operator("wm.url_open", text="Patreon", icon="FUND").url = PATREON_URL


def register() -> None:
    """Register this module's classes."""
    bpy.utils.register_class(AetherBlendPreferences)


def unregister() -> None:
    """Unregister this module's classes."""
    bpy.utils.unregister_class(AetherBlendPreferences)
