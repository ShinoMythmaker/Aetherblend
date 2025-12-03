import bpy
from bpy.props import StringProperty, EnumProperty, BoolProperty

def get_preferences():
    """Retrieve addon preferences."""
    return bpy.context.preferences.addons[__package__].preferences

class AetherBlendPreferences(bpy.types.AddonPreferences):
    """Addon preferences for AetherBlend."""
    bl_idname = __package__

    tabs: EnumProperty(
        name="Tabs",
        description="Select a preference tab",
        items=[
            ('PATHS', "Paths", "Set default paths for various functions"),
            ('GENERAL', "General", "General addon settings"),
        ],
        default='PATHS'
    ) #type: ignore

    # General Settings
    debug_mode: BoolProperty(
        name="Debug Mode",
        description="Enable detailed terminal logging and less simplified functionality for troubleshooting and development",
        default=False
    ) #type: ignore

    auto_navigate_tabs: BoolProperty(
        name="Auto Navigate Tabs",
        description="Automatically switch to relevant tabs after operations (Import → Generate, Link → Rig Layers)",
        default=True
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

    # default_pose_import_path: StringProperty(
    #     name="Pose Import",
    #     subtype='DIR_PATH',
    #     description="Select the default directory for importing pose files"
    # ) #type: ignore

    ## Test

    def draw(self, context):        
        layout = self.layout

        row = layout.row()
        row.prop(self, "tabs", expand=True)

        if self.tabs == 'GENERAL':
            box = layout.box()
            box.label(text="General Settings", icon='SETTINGS')
            box.prop(self, "debug_mode")
            box.label(text="When enabled, debug mode provides:", icon='INFO')
            box.label(text="  • Detailed terminal/console logging")
            box.label(text="  • Additional error information")
            box.label(text="  • Less simplified functionality for advanced users")
            
            box.separator()
            box.prop(self, "auto_navigate_tabs")
            box.label(text="When enabled, automatically switches tabs:", icon='INFO')
            box.label(text="  • After import → Generate tab")
            box.label(text="  • After linking → Rig Layers tab")

        elif self.tabs == 'PATHS':
            box = layout.box()
            box.label(text="Default File Paths", icon='FILE_FOLDER')
            box.prop(self, "default_meddle_import_path")
            # box.prop(self, "default_pose_import_path")
            box.prop(self, "default_pose_export_path")
            box.prop(self, "default_anim_export_path")
            box.prop(self, "default_vfx_export_path")

def register():
    bpy.utils.register_class(AetherBlendPreferences)

def unregister():
    bpy.utils.unregister_class(AetherBlendPreferences)