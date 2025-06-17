import bpy
from .status import AetherBlendStatus as status


def get_preferences():
    """Retrieve addon preferences."""
    return bpy.context.preferences.addons[__package__].preferences

def branch_changed(self, context):
    """Callback for when the branch preference changes."""
    # Call the branch check operator when the branch changes
    status.check_installs(self.branch)

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
        default='dev',
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
        right.operator("aether.check_installs", text="Run Version Control", icon='RECOVER_LAST')
    

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

        if not status.is_branch:
            status_text = "Branch mismatch!"
            status_icon = 'ERROR'
        elif not status.is_latest:
            status_text = "Old version!"
            status_icon = 'ERROR'
        right = col2.row(align=True) 
        
        if not status.restarted_check:
            right.label(text="Status Unkown", icon='QUESTION')
            right.operator("aether.check_installs", text="Run Version Control", icon='RECOVER_LAST')
        elif status.prompt_user_aether:
            right.label(text=status_text, icon=status_icon)
            right.operator("aether.restart_blender", text="Requires Restart", icon='FILE_REFRESH') 
        elif not status.is_latest or not status.is_branch:
            right.label(text=status_text, icon=status_icon)
            right.operator("aether.update", text="Update", icon='IMPORT')
        else: 
            right = col2.row(align=True) 
            right.label(text=status_text, icon=status_icon)  

        col.separator() 
    
        # Meddle 
        split = col.split(factor=indent)
        col1 = split.column(align=True)
        col1.alignment = 'RIGHT'    
        col2 = split.column(align=False)
        col1.label(text="Meddle Tools")
        right = col2.row(align=True)
        if not status.restarted_check:
            right.label(text="Status Unkown", icon='QUESTION')
            right.operator("aether.check_installs", text="Run Version Control", icon='RECOVER_LAST')
        elif not status.meddle_installed: 
            right.label(text="Not installed", icon='CANCEL')
            if status.prompt_user_meddle:
                right.operator("aether.restart_blender", text="Requires Restart", icon='FILE_REFRESH') 
            else:
                right.operator("wm.url_open", text="Github", icon="URL").url = "https://github.com/PassiveModding/MeddleTools/releases/latest"
        elif not status.meddle_is_latest:
            right.label(text="Old version!", icon='ERROR')
            if status.prompt_user_meddle:
                right.operator("aether.restart_blender", text="Requires Restart", icon='FILE_REFRESH') 
            else:
                right.operator("aether.meddle_update", text="Update", icon='IMPORT')
        elif not status.meddle_enabled:
            right.label(text="Disabled.", icon='CHECKBOX_DEHLT')
            right.operator("aether.enable_meddle", text="Enable", icon="CHECKBOX_HLT")
            if status.prompt_user_meddle:
                right.operator("aether.restart_blender", text="Requires Restart", icon='FILE_REFRESH') 
        else:
            right.label(text="Up to date", icon='CHECKMARK')
            if status.prompt_user_meddle:
                right.operator("aether.restart_blender", text="Requires Restart", icon='FILE_REFRESH') 
    
def register():
    bpy.utils.register_class(AetherBlendPreferences)

def unregister():
    bpy.utils.unregister_class(AetherBlendPreferences)