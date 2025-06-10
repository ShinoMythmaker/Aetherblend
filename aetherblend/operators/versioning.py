import bpy
from ..modules import system
from ..preferences import get_preferences

class AETHER_OT_SwitchBranch(bpy.types.Operator):
    """Switch to a different branch"""
    bl_idname = "aether.switch_branch"
    bl_label = "Switch Addon Branch"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        prefs = get_preferences()
        branch = prefs.branch
        
        # Confirm before switching
        if not system.confirm_action(f"Switch to {branch} branch?"):
            return {'CANCELLED'}

        # Download branch
        zip_path = system.download_branch(branch)
        if not zip_path:
            self.report({'ERROR'}, "[AetherBlend] Failed to download branch.")
            return {'CANCELLED'}

        # Install new branch version
        if not system.install_branch(zip_path):
            self.report({'ERROR'}, "[AetherBlend] Failed to install branch.")
            return {'CANCELLED'}

        # Restart Blender after successful installation
        system.restart_blender()
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AETHER_OT_SwitchBranch)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_SwitchBranch)