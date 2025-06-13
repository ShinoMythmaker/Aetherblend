import bpy

BRANCH_MATCH_RESULT = True 
VERSION_MATCH_RESULT = True 
MEDDLE_INSTALLED = False
MEDDLE_VERSION_MATCH_RESULT = True 
PROMPT_USER_AETHER = False
PROMPT_USER_MEDDLE = False

def set_prompt_user_meddle():
    """Prompt the user to restart Blender."""
    global PROMPT_USER_MEDDLE
    PROMPT_USER_MEDDLE = True

def set_prompt_user_aether():
    """Prompt the user to restart Blender."""
    global PROMPT_USER_AETHER
    PROMPT_USER_AETHER = True

def set_meddle_installed(result: bool):
    """Set the global branch match result."""
    global MEDDLE_INSTALLED
    MEDDLE_INSTALLED = result

def set_meddle_version_match_result(result: bool):
    """Set the global branch match result."""
    global MEDDLE_VERSION_MATCH_RESULT
    MEDDLE_VERSION_MATCH_RESULT = result

def set_version_match_result(result: bool):
    """Set the global branch match result."""
    global VERSION_MATCH_RESULT
    VERSION_MATCH_RESULT = result

def set_branch_match_result(result: bool):
    """Set the global branch match result."""
    global BRANCH_MATCH_RESULT
    BRANCH_MATCH_RESULT = result

def get_meddle_installed():
    """Get the current branch match result."""
    return MEDDLE_INSTALLED

def get_meddle_version_match_result():
    """Get the current branch match result."""
    return MEDDLE_VERSION_MATCH_RESULT

def get_version_match_result():
    """Get the current branch match result."""
    return VERSION_MATCH_RESULT

def get_branch_match_result():
    """Get the current branch match result."""
    return BRANCH_MATCH_RESULT

def get_preferences():
    """Retrieve addon preferences."""
    return bpy.context.preferences.addons[__package__].preferences

def branch_changed(self, context):
    # Call the branch check operator when the branch changes
    bpy.ops.aether.check_branch_match('INVOKE_DEFAULT')

class AetherBlendPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    branch: bpy.props.EnumProperty(
        name="Branch",
        items=[
            ('main', "Main", "Stable release"),
            ('testing', "Testing", "Experimental features"),
            ('dev', "Developement", "Active dev branch")
        ],
        default='dev',
        update= branch_changed 
    ) # type: ignore

    def draw(self, context):
        layout = self.layout
        indent = 0.2  # Adjust for your preferred spacing
    

    
        # --- Main Status Box ---
        box = layout.box()
        col = box.column(align=False)

        # --- Status Row with Dynamic Button ---
        split = col.split(factor=indent)

        col1 = split.column(align=True)
        col1.alignment = 'RIGHT'
        col2 = split.column(align=True)

        col1.label(text="AetherBlend Branch:")

        right = col2.row(align=False)
        right.prop(self, "branch", text="")
        right.operator("aether.check_installs", text="Check for Updates", icon='RECOVER_LAST')

        col.separator() 
    
        # AetherBlend
        split = col.split(factor=indent)

        col1 = split.column(align=True)
        col1.alignment = 'RIGHT'
        col2 = split.column(align=False)

        col1.label(text="AetherBlend")

        status_text = "Up to date"
        status_icon = 'CHECKMARK'
        if not BRANCH_MATCH_RESULT:
            status_text = "Branch mismatch!"
            status_icon = 'ERROR'
        elif not VERSION_MATCH_RESULT:
            status_text = "Old version!"
            status_icon = 'ERROR'

    
        right = col2.row(align=True) 
        right.label(text=status_text, icon=status_icon)
        if PROMPT_USER_AETHER:
            right.operator("aether.restart_blender", text="Requires Restart", icon='FILE_REFRESH') 
        elif not VERSION_MATCH_RESULT:
            right.operator("aether.update", text="Update", icon='IMPORT')  

        col.separator() 
    
        # Meddle 
        split = col.split(factor=indent)

        col1 = split.column(align=True)
        col1.alignment = 'RIGHT'    
        col2 = split.column(align=False)

        col1.label(text="Meddle Tools")
        right = col2.row(align=True)

        if not MEDDLE_INSTALLED: 
            right.label(text="Not installed", icon='CANCEL')
            if PROMPT_USER_MEDDLE:
                right.operator("aether.restart_blender", text="Requires Restart", icon='FILE_REFRESH') 
            else:
                right.operator("wm.url_open", text="Download", icon="HELP").url = "https://github.com/PassiveModding/MeddleTools/releases/latest"
        elif not MEDDLE_VERSION_MATCH_RESULT:
            right.label(text="Old version!", icon='ERROR')
            if PROMPT_USER_MEDDLE:
                right.operator("aether.restart_blender", text="Requires Restart", icon='FILE_REFRESH') 
            else:
                right.operator("aether.meddle_update", text="Update", icon='IMPORT')
        else:
            right.label(text="Up to date", icon='CHECKMARK')
            if PROMPT_USER_MEDDLE:
                right.operator("aether.restart_blender", text="Requires Restart", icon='FILE_REFRESH') 
    
def register():
    bpy.utils.register_class(AetherBlendPreferences)

def unregister():
    bpy.utils.unregister_class(AetherBlendPreferences)