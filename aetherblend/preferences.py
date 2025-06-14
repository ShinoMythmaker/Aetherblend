import bpy
import os

# Aetherblend GitHub repository information
GITHUB_USER = "ShinoMythmaker"
GITHUB_REPO = "Aetherblend"

# Meddle Github repository information
GITHUB_MEDDLE_USER = "PassiveModding"
GITHUB_MEDDLE_REPO = "MeddleTools"

# Extension and manifest paths
EXTENSIONS_PATH = bpy.utils.user_resource('EXTENSIONS', path="user_default")
AETHERBLEND_FOLDER = os.path.join(EXTENSIONS_PATH, "aetherblend")
MEDDLE_FOLDER = os.path.join(EXTENSIONS_PATH, "meddle_tools")


class AetherBlendStatus:
    """Class to hold the status of AetherBlend and Meddle installations."""
    BRANCH_MATCH_RESULT = True
    VERSION_MATCH_RESULT = True
    MEDDLE_INSTALLED = False
    MEDDLE_VERSION_MATCH_RESULT = True
    PROMPT_USER_AETHER = False
    PROMPT_USER_MEDDLE = False

    @classmethod
    def set(cls, **kwargs):
        for k, v in kwargs.items():
            if hasattr(cls, k):
                setattr(cls, k, v)
            else:
                # Handle name-mangled private attributes
                mangled = f"_{cls.__name__}__{k}" if k.startswith("__") and not k.endswith("__") else None
                if mangled and hasattr(cls, mangled):
                    setattr(cls, mangled, v)

    @classmethod
    def get(cls, name):
        return getattr(cls, name, None)
    
status = AetherBlendStatus  #Alias for convenience

def get_preferences():
    """Retrieve addon preferences."""
    return bpy.context.preferences.addons[__package__].preferences

def branch_changed(self, context):
    """Callback for when the branch preference changes."""
    # Call the branch check operator when the branch changes
    bpy.ops.aether.check_installs('EXEC_DEFAULT')

class AetherBlendPreferences(bpy.types.AddonPreferences):
    """Addon preferences for AetherBlend."""
    bl_idname = __package__

    branch: bpy.props.EnumProperty(
        name="Branch",
        items=[
            ('main', "Main", "Stable release"),
            ('testing', "Testing", "Experimental features"),
            ('dev', "Developement", "Active dev branch")
        ],
        default='main',
        update=branch_changed 
    ) # type: ignore

    run_check_on_startup: bpy.props.BoolProperty(
        name="Check for updates on startup",
        description="Automatically check for AetherBlend and Meddle updates when Blender starts",
        default=True
    ) # type: ignore

    def draw(self, context):
        layout = self.layout
        indent = 0.2  

        col = layout.column()
        split = col.split(factor=indent)
        col1 = split.column()
        col1.alignment = 'RIGHT'
        col1.label(text="Version Checks:")
        col2 = split.column()
        right = col2.row(align=True)
        right.prop(self, "run_check_on_startup")
        right.operator("aether.check_installs", text="Check for Updates", icon='RECOVER_LAST')
    

        col = layout.column(align=False)

        split = col.split(factor=indent)
        col1 = split.column(align=True)
        col1.alignment = 'RIGHT'
        col2 = split.column(align=True)
        col1.label(text="AetherBlend Branch:")
        right = col2.row(align=False)
        right.prop(self, "branch", text="")

        col.separator() 
    
        # AetherBlend
        split = col.split(factor=indent)
        col1 = split.column(align=True)
        col1.alignment = 'RIGHT'
        col2 = split.column(align=False)
        col1.label(text="AetherBlend")
        status_text = "Up to date"
        status_icon = 'CHECKMARK'
        if not status.BRANCH_MATCH_RESULT:
            status_text = "Branch mismatch!"
            status_icon = 'ERROR'
        elif not status.VERSION_MATCH_RESULT:
            status_text = "Old version!"
            status_icon = 'ERROR'
        right = col2.row(align=True) 
        right.label(text=status_text, icon=status_icon)
        if status.PROMPT_USER_AETHER:
            right.operator("aether.restart_blender", text="Requires Restart", icon='FILE_REFRESH') 
        elif not status.VERSION_MATCH_RESULT or not status.BRANCH_MATCH_RESULT:
            right.operator("aether.update", text="Update", icon='IMPORT')  

        col.separator() 
    
        # Meddle 
        split = col.split(factor=indent)
        col1 = split.column(align=True)
        col1.alignment = 'RIGHT'    
        col2 = split.column(align=False)
        col1.label(text="Meddle Tools")
        right = col2.row(align=True)
        if not status.MEDDLE_INSTALLED: 
            right.label(text="Not installed", icon='CANCEL')
            if status.PROMPT_USER_MEDDLE:
                right.operator("aether.restart_blender", text="Requires Restart", icon='FILE_REFRESH') 
            else:
                right.operator("wm.url_open", text="Github", icon="URL").url = "https://github.com/PassiveModding/MeddleTools/releases/latest"
        elif not status.MEDDLE_VERSION_MATCH_RESULT:
            right.label(text="Old version!", icon='ERROR')
            if status.PROMPT_USER_MEDDLE:
                right.operator("aether.restart_blender", text="Requires Restart", icon='FILE_REFRESH') 
            else:
                right.operator("aether.meddle_update", text="Update", icon='IMPORT')
        else:
            right.label(text="Up to date", icon='CHECKMARK')
            if status.PROMPT_USER_MEDDLE:
                right.operator("aether.restart_blender", text="Requires Restart", icon='FILE_REFRESH') 
    
def register():
    bpy.utils.register_class(AetherBlendPreferences)

def unregister():
    bpy.utils.unregister_class(AetherBlendPreferences)