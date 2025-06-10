import bpy
from ..modules import system
from ..preferences import get_preferences

class AETHER_OT_Update(bpy.types.Operator):
    """Switch to a different branch"""
    bl_idname = "aether.update"
    bl_label = "Updates to newsest Version"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        prefs = get_preferences()
        branch = prefs.branch
        
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
        self.report({'INFO'}, "[AetherBlend] Restarting Blender after successful installation.")
        system.restart_blender()
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AETHER_OT_Update)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_Update)