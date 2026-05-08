import bpy
from bpy.props import StringProperty, EnumProperty
from pathlib import Path
import os
import json

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


class AETHER_OT_Set_Default_Template(bpy.types.Operator):
    """Set the default rig template used for new rigs."""
    bl_idname = "aether.set_default_template"
    bl_label = "Set as Default Template"
    bl_description = "Use this template as the default when creating a new rig"

    template_name: StringProperty(
        name="Template Name",
        options={'HIDDEN'},
    ) # type: ignore

    def execute(self, context):
        prefs = get_preferences()
        prefs.default_template = self.template_name
        
        # If the template being set as default is hidden, unhide it
        raw = (getattr(prefs, 'hidden_templates', '') or '').strip()
        hidden: set[str] = set()
        if raw:
            try:
                values = json.loads(raw)
                if isinstance(values, list):
                    hidden = {
                        value.strip()
                        for value in values
                        if isinstance(value, str) and value.strip()
                    }
            except Exception:
                pass
        
        if self.template_name in hidden:
            hidden.remove(self.template_name)
            prefs.hidden_templates = json.dumps(sorted(hidden), ensure_ascii=True)
        
        self.report({'INFO'}, f"Default template set to: {self.template_name}")
        return {'FINISHED'}


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


class AETHER_OT_Toggle_Template_Visibility(bpy.types.Operator):
    """Toggle whether a template appears in dropdown lists."""
    bl_idname = "aether.toggle_template_visibility"
    bl_label = "Toggle Template Visibility"
    bl_description = "Hide or show this template in template dropdowns"

    template_name: StringProperty(
        name="Template Name",
        options={'HIDDEN'},
    ) #type: ignore

    def execute(self, context):
        if not self.template_name:
            self.report({'WARNING'}, "No template name was provided")
            return {'CANCELLED'}

        prefs = get_preferences()
        default_name = (getattr(prefs, 'default_template', '') or '').strip()
        
        if self.template_name == default_name:
            self.report({'WARNING'}, "Cannot hide the default template")
            return {'CANCELLED'}

        raw = (getattr(prefs, 'hidden_templates', '') or '').strip()

        hidden: set[str] = set()
        if raw:
            try:
                values = json.loads(raw)
                if isinstance(values, list):
                    hidden = {
                        value.strip()
                        for value in values
                        if isinstance(value, str) and value.strip()
                    }
            except Exception:
                hidden = set()

        if self.template_name in hidden:
            hidden.remove(self.template_name)
            action = "shown"
        else:
            hidden.add(self.template_name)
            action = "hidden"

        prefs.hidden_templates = json.dumps(sorted(hidden), ensure_ascii=True)
        self.report({'INFO'}, f"Template {action}: {self.template_name}")
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

    default_template: StringProperty(
        name="Default Template",
        description="Template selected by default when creating a new rig",
        default=""
    ) #type: ignore

    hidden_templates: StringProperty(
        name="Hidden Templates",
        description="JSON list of template names hidden from dropdown menus",
        default=""
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
            current_default = template_manager.get_default_template_name()
            hidden_names = template_manager.get_hidden_template_names()

            col = layout.column(align=True)

            # col.label(text="Base Templates", icon='PRESET')
            for entry in base_entries:
                row = col.row(align=True)
                is_default = entry["name"] == current_default
                is_hidden = entry["name"] in hidden_names

                row.label(text="", icon='SOLO_ON' if is_default else 'BLANK1')
                row.label(text=entry["name"], icon='HIDE_ON' if is_hidden else 'HIDE_OFF')

                visibility_sub = row.row()
                visibility_sub.enabled = not is_default
                visibility_op = visibility_sub.operator("aether.toggle_template_visibility",text="",icon='HIDE_ON' if is_hidden else 'HIDE_OFF')
                visibility_op.template_name = entry["name"]

                set_op = row.operator("aether.set_default_template", text="", icon='SOLO_OFF' if not is_default else 'SOLO_ON')
                set_op.template_name = entry["name"] if not is_default else " "

            col.separator()

            # col.label(text="Custom Templates", icon='FILE_FOLDER')
            for entry in custom_entries:
                row = col.row(align=True)
                is_default = entry["name"] == current_default
                is_hidden = entry["name"] in hidden_names

                row.label(text="", icon='SOLO_ON' if is_default else 'BLANK1')
                row.label(text=entry["name"], icon='HIDE_ON' if is_hidden else 'HIDE_OFF')

                delete_op = row.operator("aether.delete_custom_template", text="", icon='TRASH')
                delete_op.template_path = entry["path"]

                visibility_sub = row.row()
                visibility_sub.enabled = not is_default
                visibility_op = visibility_sub.operator("aether.toggle_template_visibility",text="",icon='HIDE_ON' if is_hidden else 'HIDE_OFF')
                visibility_op.template_name = entry["name"]

                set_op = row.operator("aether.set_default_template", text="", icon='SOLO_OFF' if not is_default else 'SOLO_ON')
                set_op.template_name = entry["name"] if not is_default else " "

            if not custom_entries:
                col.label(text="No custom templates saved yet", icon='INFO')

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
    bpy.utils.register_class(AETHER_OT_Set_Default_Template)
    bpy.utils.register_class(AETHER_OT_Delete_Custom_Template)
    bpy.utils.register_class(AETHER_OT_Toggle_Template_Visibility)
    bpy.utils.register_class(AetherBlendPreferences)

def unregister():
    bpy.utils.unregister_class(AetherBlendPreferences)
    bpy.utils.unregister_class(AETHER_OT_Toggle_Template_Visibility)
    bpy.utils.unregister_class(AETHER_OT_Delete_Custom_Template)
    bpy.utils.unregister_class(AETHER_OT_Set_Default_Template)