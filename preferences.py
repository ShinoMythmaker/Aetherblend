import bpy
from bpy.props import StringProperty, EnumProperty
from pathlib import Path
import os

TOGGLE_ITEMS = [('ON', "Enable", ""), ('OFF', "Disable", "")]
GITHUB_URL = "https://github.com/ShinoMythmaker/Aetherblend"
DISCORD_URL = "https://discord.gg/NEF7TdXGqH"
PATREON_URL = "https://www.patreon.com/ShinoMythmaker"


def get_default_custom_template_path() -> str:
    """Return the default custom template folder in the user's AppData profile."""
    appdata = os.getenv("APPDATA")
    if appdata:
        return str(Path(appdata) / "AetherBlend" / "templates" / "custom")

    return str(Path.home() / "AppData" / "Roaming" / "AetherBlend" / "templates" / "custom")

def get_preferences():
    """Retrieve addon preferences."""
    return bpy.context.preferences.addons[__package__].preferences


class AETHER_OT_Delete_Custom_Template(bpy.types.Operator):
    """Delete one custom template file from addon preferences."""
    bl_idname = "aether.delete_custom_template"
    bl_label = "Delete Custom Template"
    bl_description = "Delete this custom template JSON file"

    template_path: StringProperty(
        name="Template Path",
        options={'HIDDEN'},
    ) #type: ignore

    def execute(self, context):
        from .features.rigging import template_manager

        if not self.template_path:
            self.report({'WARNING'}, "No custom template path was provided")
            return {'CANCELLED'}

        deleted = template_manager.delete_custom_template_file(self.template_path)
        if not deleted:
            self.report({'WARNING'}, "Could not delete custom template")
            return {'CANCELLED'}

        self.report({'INFO'}, "Custom template deleted")
        return {'FINISHED'}

class AetherBlendPreferences(bpy.types.AddonPreferences):
    """Addon preferences for AetherBlend."""
    bl_idname = __package__

    tabs: EnumProperty(
        name="Tabs",
        description="Select a preference tab",
        items=[
            ('GENERAL', "General", "General addon settings"),
            ('PATHS', "Paths", "Set default paths for various functions"),
            ('TEMPLATES', "Templates", "View available base and custom templates"),
            ('CONTRIBUTION', "Contribution", "How to support and contribute"),
        ],
        default='GENERAL'
    ) #type: ignore

    # General Settings
    auto_navigate_tabs: EnumProperty(
        name="Auto Navigate Tabs",
        description="Automatically switch to relevant tabs after operations (Import → Generate, Link → Rig Layers)",
        items=TOGGLE_ITEMS,
        default='ON'
    ) #type: ignore

    show_n_panel: EnumProperty(
        name="Show N-Panel UI",
        description="Show AetherBlend panels in the 3D View sidebar",
        items=TOGGLE_ITEMS,
        default='ON'
    ) #type: ignore

    show_properties_tool_tab: EnumProperty(
        name="Show Properties Tool UI",
        description="Show AetherBlend panels in the Properties editor Tool context",
        items=TOGGLE_ITEMS,
        default='ON'
    ) #type: ignore

    # Default File Paths
    default_meddle_import_path: StringProperty(
        name="Meddle Import",
        subtype='DIR_PATH',
        description="Select the default directory for importing Meddle files"
    ) #type: ignore

    default_pose_export_path: StringProperty(
        name="Pose Export",
        subtype='DIR_PATH',
        description="Select the default directory for saving pose files"
    ) #type: ignore

    default_anim_export_path: StringProperty(
        name="Anim Export",
        subtype='DIR_PATH',
        description="Select the default directory for saving animation files"
    ) #type: ignore

    default_vfx_export_path: StringProperty(
        name="VFX Export",
        subtype='DIR_PATH',
        description="Select the default directory for saving VFX model files"
    ) #type: ignore

    custom_template_path: StringProperty(
        name="Custom Templates",
        subtype='DIR_PATH',
        description="Directory used to save and load custom rig template JSON files",
        default=get_default_custom_template_path()
    ) #type: ignore

    # default_pose_import_path: StringProperty(
    #     name="Pose Import",
    #     subtype='DIR_PATH',
    #     description="Select the default directory for importing pose files"
    # ) #type: ignore

    ## Test

    def draw(self, context):        
        layout = self.layout

        def draw_switch(parent, prop_name, label):
            row = parent.row(align=True)
            split = row.split(factor=0.72, align=True)
            split.label(text=label)
            toggle = split.row(align=True)
            toggle.prop(self, prop_name, expand=True)

        row = layout.row()
        row.prop(self, "tabs", expand=True)

        if self.tabs == 'GENERAL':
            box = layout.box()
            box.label(text="General Settings", icon='SETTINGS')
            
            box.separator()
            draw_switch(box, "auto_navigate_tabs", "Auto Navigate Tabs")
            box.separator()
            draw_switch(box, "show_n_panel", "Show N-Panel UI")
            draw_switch(box, "show_properties_tool_tab", "Show Properties Tool UI")

        elif self.tabs == 'PATHS':
            box = layout.box()
            box.label(text="Default File Paths", icon='FILE_FOLDER')
            box.prop(self, "default_meddle_import_path")
            # box.prop(self, "default_pose_import_path")
            box.prop(self, "default_pose_export_path")
            box.prop(self, "default_anim_export_path")
            box.prop(self, "default_vfx_export_path")
            box.separator()
            box.label(text="Rig Templates", icon='PRESET')
            box.prop(self, "custom_template_path")

        elif self.tabs == 'TEMPLATES':
            from .features.rigging import template_manager

            catalogue = template_manager.get_template_catalogue()
            base_entries = catalogue.get("base", [])
            custom_entries = catalogue.get("custom", [])

            base_box = layout.box()
            base_box.label(text=f"Base Templates ({len(base_entries)})", icon='PRESET')
            if base_entries:
                for entry in base_entries:
                    base_box.label(text=entry["name"], icon='DOT')
            else:
                base_box.label(text="No base templates found", icon='INFO')

            custom_box = layout.box()
            custom_box.label(text=f"Custom Templates ({len(custom_entries)})", icon='FILE_FOLDER')
            custom_box.label(text=f"Path: {template_manager.get_custom_template_json_dir()}", icon='BLANK1')
            if custom_entries:
                for entry in custom_entries:
                    row = custom_box.row(align=True)
                    row.label(text=entry["name"], icon='DOT')
                    delete_op = row.operator("aether.delete_custom_template", text="", icon='TRASH')
                    delete_op.template_path = entry["path"]
            else:
                custom_box.label(text="No custom templates found", icon='INFO')

        elif self.tabs == 'CONTRIBUTION':
            main_box = layout.box()
            main_box.label(text="Contribution", icon='HEART')

            split = main_box.split(factor=0.68, align=False)
            left = split.column(align=True)
            right = split.column(align=True)
            left.label(text="Support us on Patreon!")
            left.label(text="Supporters in the highest tier (`Mythmaker`) are listed below.")
            left.separator()
            left.label(text="- Zed")
            left.label(text="- PancakePapi")
            left.label(text="- Pizzadabbin")

            right.separator()
            right.operator("wm.url_open", text="GitHub Issues", icon='URL').url = f"{GITHUB_URL}/issues"
            right.operator("wm.url_open", text="Discord", icon='COMMUNITY').url = DISCORD_URL
            right.operator("wm.url_open", text="Repository", icon='FILEBROWSER').url = GITHUB_URL
            right.operator("wm.url_open", text="Patreon", icon='FUND').url = PATREON_URL

def register():
    bpy.utils.register_class(AETHER_OT_Delete_Custom_Template)
    bpy.utils.register_class(AetherBlendPreferences)

def unregister():
    bpy.utils.unregister_class(AetherBlendPreferences)
    bpy.utils.unregister_class(AETHER_OT_Delete_Custom_Template)