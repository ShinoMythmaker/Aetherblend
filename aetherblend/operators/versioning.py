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
        
        if not system.confirm_action(f"Switch to {branch} branch?"):
            return {'CANCELLED'}
        
        if not system.download_branch(branch):
            self.report({'ERROR'}, "[AetherBlend] Failed to switch branch.")
            return {'CANCELLED'}

        system.restart_blender()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AETHER_OT_SwitchBranch)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_SwitchBranch)