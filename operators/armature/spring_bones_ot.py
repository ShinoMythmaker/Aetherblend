import bpy
from ...utils import rig as rig_utils
from ...data.constants import sb_breast_collection, sb_ears_collection, sb_tail_collection

class AETHER_OT_Bake_All_Spring_Bones(bpy.types.Operator):
    """Bake all spring bones for the active armature object."""
    bl_idname = "aether.bake_all_spring_bones"
    bl_label = "Bake All Spring Bones"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "[AetherBlend] Select an armature object")
            return {'CANCELLED'}

        if context.scene.ab_sb_global_spring_frame == False:
            self.report({'ERROR'}, "[AetherBlend] Spring Frame is not enabled. Please enable it first.")
            return {'CANCELLED'}
        
        # Bake each type of spring bone

        if rig_utils.bone.get_collectiion(context.active_object, sb_breast_collection):
            bpy.ops.aether.bake_spring_breasts()
        if rig_utils.bone.get_collectiion(context.active_object, sb_ears_collection):
            bpy.ops.aether.bake_spring_ears()
        if rig_utils.bone.get_collectiion(context.active_object, sb_tail_collection):
            bpy.ops.aether.bake_spring_tail()

        self.report({'INFO'}, f"[AetherBlend] All spring bones baked for {armature.name}.")
        return {'FINISHED'}
    

def register():
    bpy.utils.register_class(AETHER_OT_Bake_All_Spring_Bones)   

def unregister():    
    bpy.utils.unregister_class(AETHER_OT_Bake_All_Spring_Bones)


