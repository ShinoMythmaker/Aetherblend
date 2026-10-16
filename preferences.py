import json

import bpy
from bpy.props import EnumProperty, StringProperty

from .utils import addon_dependencies

TOGGLE_ITEMS = [('ON', "Enable", ""), ('OFF', "Disable", "")]
GITHUB_URL = "https://github.com/ShinoMythmaker/Aetherblend"
DISCORD_URL = "https://discord.gg/NEF7TdXGqH"
PATREON_URL = "https://www.patreon.com/ShinoMythmaker"


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


class AETHER_OT_Toggle_Feature_Set(bpy.types.Operator):
    """Toggle one feature set used for dependency checks and UI state."""

    bl_idname = "aether.preferences_toggle_feature_set"
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
                toggle_op = header.operator("aether.preferences_toggle_feature_set", text=toggle_text, icon=toggle_icon, depress=is_enabled)
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
            left.label(text="- Djaal")

            right.separator()
            right.operator("wm.url_open", text="GitHub Issues", icon='URL').url = f"{GITHUB_URL}/issues"
            right.operator("wm.url_open", text="Discord", icon='COMMUNITY').url = DISCORD_URL
            right.operator("wm.url_open", text="Repository", icon='FILEBROWSER').url = GITHUB_URL
            right.operator("wm.url_open", text="Patreon", icon='FUND').url = PATREON_URL


def register():
    bpy.utils.register_class(AETHER_OT_Toggle_Feature_Set)
    bpy.utils.register_class(AetherBlendPreferences)

def unregister():
    bpy.utils.unregister_class(AetherBlendPreferences)
    bpy.utils.unregister_class(AETHER_OT_Toggle_Feature_Set)
