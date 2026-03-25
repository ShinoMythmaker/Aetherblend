import bpy
from bpy.types import Operator

class AETHER_OT_SetBoneInheritScale(Operator):
    bl_idname = "aether.set_bone_inherit_scale"
    bl_label = "Set Inherit Scale"
    bl_description = "Set inherit scale for bones in LINK collection"
    bl_options = {'REGISTER', 'UNDO'}
    
    inherit_scale: bpy.props.EnumProperty(
        name="Inherit Scale",
        items=[
            ('FULL', "Full", "Full inherit scale"),
            ('FIX_SHEAR', "Aligned", "Inherit scale with shear fixed"),
            ('AVERAGE', "Average", "Average scale inheritance"),
            ('NONE', "None", "No scale inheritance"),
            ('NONE_LEGACY', "None (Legacy)", "No scale inheritance (legacy)"),
        ],
        default='FULL',
    ) # type: ignore
    
    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}
        
        link_collection = armature.data.collections.get('LINK')
        if not link_collection:
            self.report({'ERROR'}, "LINK collection not found")
            return {'CANCELLED'}
        
        aether_rig = getattr(armature, 'aether_rig', None)
        if aether_rig:
            aether_rig.link_inherit_scale = self.inherit_scale
        
        bone_count = 0
        for bone in armature.pose.bones:
            if bone.bone.collections.get('LINK'):
                bone.bone.inherit_scale = self.inherit_scale
                bone_count += 1
        
        self.report({'INFO'}, f"Updated {bone_count} bones in LINK collection")
        return {'FINISHED'}

class AETHER_OT_DeleteNoAnim(Operator):
    bl_idname = "aether.delete_no_anim"
    bl_label = "Delete NoAnim"
    bl_description = "Deletes all bones containing the 'noanim' flag."
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        pattern = "noanim"
        armature = context.active_object
        original_mode = context.active_object.mode

        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='EDIT')

        edit_bones = armature.data.edit_bones
        
        for bone in edit_bones:
            if pattern in bone.name:
                edit_bones.remove(bone)

        bpy.ops.object.mode_set(mode=original_mode)  
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AETHER_OT_DeleteNoAnim)
    bpy.utils.register_class(AETHER_OT_SetBoneInheritScale)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_DeleteNoAnim)
    bpy.utils.unregister_class(AETHER_OT_SetBoneInheritScale)
