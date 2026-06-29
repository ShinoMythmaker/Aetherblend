import bpy
from bpy.props import StringProperty, EnumProperty
from pathlib import Path
import os
import json

from .utils import addon_dependencies

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

def is_set_enabled(feature_set_token: str) -> bool:
    """Return whether a feature set is enabled in addon preferences."""
    prefs = get_preferences()
    enabled_sets = prefs.get_enabled_feature_sets()
    try:
        return feature_set_token in enabled_sets
    except Exception:
        pass

    return False


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


class AETHER_OT_Toggle_Feature_Set(bpy.types.Operator):
    """Toggle one feature set used for dependency checks and UI state."""
    bl_idname = "aether.toggle_feature_set"
    bl_label = "Toggle Feature Set"
    bl_description = "Enable or disable one feature set"

    feature_set: StringProperty(
        name="Feature Set",
        options={'HIDDEN'},
    ) #type: ignore

    def execute(self, context):
        if addon_dependencies.is_common_feature_set(self.feature_set):
            self.report({'INFO'}, f"{self.feature_set} is always enabled")
            return {'CANCELLED'}

        feature_set_tokens = addon_dependencies.get_feature_set_tokens()
        if self.feature_set not in feature_set_tokens:
            self.report({'WARNING'}, "Unknown feature set")
            return {'CANCELLED'}

        prefs = get_preferences()
        raw = (getattr(prefs, 'enabled_feature_sets', '') or '').strip()

        enabled: set[str] = set()
        if raw:
            try:
                values = json.loads(raw)
                if isinstance(values, list):
                    enabled = {
                        value
                        for value in values
                        if isinstance(value, str) and value in feature_set_tokens
                    }
            except Exception:
                enabled = AetherBlendPreferences.get_default_enabled_feature_sets()

        if self.feature_set in enabled:
            enabled.remove(self.feature_set)
            state = "OFF"
        else:
            enabled.add(self.feature_set)
            state = "ON"

        ordered = [token for token in feature_set_tokens if token in enabled]
        prefs.enabled_feature_sets = json.dumps(ordered, ensure_ascii=True)
        self.report({'INFO'}, f"{self.feature_set}: {state}")
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

    enabled_feature_sets: StringProperty(
        name="Enabled Feature Sets",
        description="JSON list of enabled feature set tokens",
        default=json.dumps(
            [
                token
                for token in addon_dependencies.get_feature_set_tokens()
                if not addon_dependencies.is_common_feature_set(token)
            ],
            ensure_ascii=True,
        )
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

    @staticmethod
    def get_default_enabled_feature_sets() -> set[str]:
        return {
            token
            for token in addon_dependencies.get_feature_set_tokens()
            if not addon_dependencies.is_common_feature_set(token)
        }

    def get_enabled_feature_sets(self) -> set[str]:
        raw = (getattr(self, 'enabled_feature_sets', '') or '').strip()
        if not raw:
            return self.get_default_enabled_feature_sets()

        try:
            values = json.loads(raw)
        except Exception:
            return self.get_default_enabled_feature_sets()

        if not isinstance(values, list):
            return self.get_default_enabled_feature_sets()

        feature_set_tokens = addon_dependencies.get_feature_set_tokens()

        return {
            value
            for value in values
            if isinstance(value, str)
            and value in feature_set_tokens
            and not addon_dependencies.is_common_feature_set(value)
        }

    def draw(self, context):        
        layout = self.layout

        def draw_switch(parent, prop_name, label):
            row = parent.row(align=True)
            split = row.split(factor=0.72, align=True)
            split.label(text=label)
            toggle = split.row(align=True)
            toggle.prop(self, prop_name, expand=True)

        active_feature_sets =  self.get_enabled_feature_sets()

        dependency_col = layout.column(align=True)
        dependency_col.label(text="Dependency Add-ons", icon='PLUGIN')

        missing_active = addon_dependencies.get_missing_required_addons(active_feature_sets)
        if missing_active:
            dependency_col.label(
                text=f"Missing for active feature sets: {len(missing_active)}",
                icon='ERROR',
            )
        else:
            dependency_col.label(text="All active feature set dependencies are available", icon='CHECKMARK')

        for feature_set in addon_dependencies.get_feature_set_tokens():
            feature_box = dependency_col.box()
            header = feature_box.row(align=True)

            is_common = addon_dependencies.is_common_feature_set(feature_set)
            is_enabled = is_common or feature_set in active_feature_sets
            header_icon = 'CHECKMARK' if is_enabled else 'PAUSE'
            header.label(text=addon_dependencies.get_feature_set_label(feature_set), icon=header_icon)

            if is_common:
                header.label(text="Always On", icon='LOCKED')
            else:
                toggle_text = "On" if is_enabled else "Off"
                toggle_icon = 'CHECKMARK' if is_enabled else 'X'
                toggle_op = header.operator("aether.toggle_feature_set", text=toggle_text, icon=toggle_icon, depress=is_enabled)
                toggle_op.feature_set = feature_set

            grouped_addons = sorted(
                addon_dependencies.get_addons_for_feature_set(feature_set),
                key=lambda item: str(item.get("name") or item.get("module") or ""),
            )

            if not grouped_addons:
                feature_box.label(text="No dependencies configured", icon='INFO')
                continue

            for entry in grouped_addons:
                addon_name = entry.get("name") or entry.get("module") or "Unknown add-on"
                module_name = entry.get("module")
                required_now = addon_dependencies.is_addon_required_for_feature_sets(entry, active_feature_sets)
                enabled = addon_dependencies.is_addon_enabled(
                    module_name=module_name,
                    display_name=entry.get("name"),
                )

                row = feature_box.row(align=True)
                split = row.split(factor=0.72, align=True)

                left = split.row(align=True)
                if required_now:
                    icon = 'CHECKMARK' if enabled else 'ERROR'
                else:
                    icon = 'BLANK1' if enabled else 'HIDE_OFF'
                left.label(text=str(addon_name), icon=icon)

                right = split.row(align=True)
                right.alignment = 'RIGHT'
                right.ui_units_x = 10.0

                action_row = right.row(align=True)
                action_row.scale_y = 1.15

                is_builtin = addon_dependencies.is_builtin_addon_entry(entry)
                if is_builtin and not enabled and module_name:
                    op = action_row.operator("preferences.addon_enable", text="Enable", icon='CHECKMARK')
                    op.module = str(module_name)
                elif is_builtin:
                    status_text = "Built-in"
                    if not required_now:
                        status_text = "Built-in (Inactive)"
                    action_row.label(text=status_text, icon='BLENDER')
                else:
                    url = addon_dependencies.get_addon_support_url(
                        module_name=str(module_name) if isinstance(module_name, str) else None,
                        display_name=entry.get("name") if isinstance(entry.get("name"), str) else None,
                    )
                    if url:
                        cta_label = addon_dependencies.get_addon_link_label(entry)
                        button_text = cta_label if required_now else f"{cta_label} (Inactive)"
                        action_row.operator("wm.url_open", text=button_text, icon='URL').url = url
                    else:
                        action_row.label(text="No Link", icon='INFO')

        layout.separator()

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
    bpy.utils.register_class(AETHER_OT_Toggle_Feature_Set)
    bpy.utils.register_class(AetherBlendPreferences)

def unregister():
    bpy.utils.unregister_class(AetherBlendPreferences)
    bpy.utils.unregister_class(AETHER_OT_Toggle_Feature_Set)
    bpy.utils.unregister_class(AETHER_OT_Toggle_Template_Visibility)
    bpy.utils.unregister_class(AETHER_OT_Delete_Custom_Template)
    bpy.utils.unregister_class(AETHER_OT_Set_Default_Template)