import bpy
from bpy.props import StringProperty, EnumProperty

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
        ],
        default='PATHS'
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

        box = layout.box()
        box.label(text="Default File Paths")
        box.prop(self, "default_meddle_import_path")
        # box.prop(self, "default_pose_import_path")
        box.prop(self, "default_pose_export_path")
        box.prop(self, "default_anim_export_path")
        box.prop(self, "default_vfx_export_path")

def register():
    bpy.utils.register_class(AetherBlendPreferences)

def unregister():
    bpy.utils.unregister_class(AetherBlendPreferences)