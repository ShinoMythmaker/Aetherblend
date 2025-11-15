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
            ('UI', "User Interface", "UI settings"),
            ('PATHS', "Paths", "Set default paths for various functions"),
        ],
        default='UI'
    ) #type: ignore

    import_panel: EnumProperty(
        name="Import Panel",
        description="Enables/Disables the Import Panel in the N sidebar",
        items=[('OFF', "Disable", ""), ('ON', "Enable", "")],
        default='ON'
    ) #type: ignore

    customize_plus_panel: EnumProperty(
        name="Customize Plus Panel",
        description="Enables/Disables the Customize Plus Panel in the N sidebar",
        items=[('OFF', "Disable", ""), ('ON', "Enable", "")],
        default='ON'
    ) #type: ignore

    export_panel: EnumProperty(
        name="Export Panel",
        description="Enables/Disables the Export Panel in the N sidebar",
        items=[('OFF', "Disable", ""), ('ON', "Enable", "")],
        default='ON'
    ) #type: ignore

    create_rig_panel: EnumProperty(
        name="Create Rig Panel",
        description="Enables/Disables the Create Rig Panel in the N sidebar",
        items=[('OFF', "Disable", ""), ('ON', "Enable", "")],
        default='ON'
    ) #type: ignore

    rig_layers_panel: EnumProperty(
        name="Rig Layers Panel",
        description="Enables/Disables the Rig Layers Panel in the N sidebar",
        items=[('OFF', "Disable", ""), ('ON', "Enable", "")],
        default='ON'
    ) #type: ignore

    rig_ui_panel: EnumProperty(
        name="Rig UI Panel",
        description="Enables/Disables the Rig UI Panel in the N sidebar",
        items=[('OFF', "Disable", ""), ('ON', "Enable", "")],
        default='ON'
    ) #type: ignore

    rig_bake_panel: EnumProperty(
        name="Rig Bake Panel",
        description="Enables/Disables the Rig Bake Panel in the N sidebar",
        items=[('OFF', "Disable", ""), ('ON', "Enable", "")],
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

    def draw(self, context):
        def draw_toggle(label, prop_name):
                row = box.row()
                row.label(text=label)
                row.prop(self, prop_name, expand=True)
        
        layout = self.layout

        # Tabs
        row = layout.row()
        row.prop(self, "tabs", expand=True)
        
        if self.tabs == 'UI':
            box = layout.box()
            box.label(text="User Interface Settings")
            draw_toggle("Import Panel", "import_panel")
            draw_toggle("Customize Plus Panel", "customize_plus_panel")
            draw_toggle("Export Panel", "export_panel")
            draw_toggle("Create Rig Panel", "create_rig_panel")
            draw_toggle("Rig Layers Panel", "rig_layers_panel")
            draw_toggle("Rig UI Panel", "rig_ui_panel")
            draw_toggle("Rig Bake Panel", "rig_bake_panel")
            
            
        elif self.tabs == 'PATHS':
            box = layout.box()
            box.label(text="Default File Paths")
            box.prop(self, "default_meddle_import_path")
            # box.prop(self, "default_pose_import_path")
            box.prop(self, "default_pose_export_path")
            box.prop(self, "default_anim_export_path")

def register():
    bpy.utils.register_class(AetherBlendPreferences)

def unregister():
    bpy.utils.unregister_class(AetherBlendPreferences)