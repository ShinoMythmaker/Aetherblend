import bpy


class AETHER_OT_Solo_Bone_Collections(bpy.types.Operator):
    bl_idname = "aether.solo_bone_collections"
    bl_label = "Solo Selected"
    bl_description = "Toggle solo for bone collections."
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return {'CANCELLED'}
        
        mode = bpy.context.mode
        if mode not in {'POSE', 'EDIT_ARMATURE'}:
            return {'CANCELLED'}
        
        any_soloed = any(collection.is_solo for collection in armature.data.collections)
        
        if any_soloed:
            for collection in armature.data.collections:
                collection.is_solo = False
        else:
            selected_bones = context.selected_pose_bones if context.mode == 'POSE' else []
            
            if not selected_bones:
                return {'CANCELLED'}
            
            selected_collections = set()
            for pose_bone in selected_bones:
                bone = armature.data.bones.get(pose_bone.name)
                if bone:
                    for collection in bone.collections:
                        selected_collections.add(collection)
            
            if not selected_collections:
                return {'CANCELLED'}
            
            for collection in selected_collections:
                collection.is_solo = True
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(AETHER_OT_Solo_Bone_Collections)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_Solo_Bone_Collections)
