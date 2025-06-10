import bpy
import os

def get_preferences():
    """Retrieve addon preferences."""
    return bpy.context.preferences.addons[__package__].preferences

class AetherBlendPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    github_repo: bpy.props.StringProperty(
        name= "GitHub Repository URL",
        default= "https://github.com/ShinoMythmaker/Aetherblend/archive/refs/heads/"
    )

    addon_path: bpy.props.StringProperty(
        name= "Addon Path",
        default= os.path.join(bpy.utils.user_resource('EXTENSIONS', path="user_default"), "AetherBlend")
    )

    branch: bpy.props.EnumProperty(
        name="Branch",
        items=[
            ('main', "Main", "Stable release"),
            ('testing', "Testing", "Experimental features"),
            ('dev', "Developement", "Active dev branch")
        ],
        default='main'
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "branch")
        layout.operator("aether.switch_branch", text="Switch Branch")

def register():
    bpy.utils.register_class(AetherBlendPreferences)

def unregister():
    bpy.utils.unregister_class(AetherBlendPreferences)