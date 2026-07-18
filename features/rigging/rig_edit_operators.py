import bpy
from bpy.types import Operator
from ...utils import armature as armature_utils 

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


class AETHER_OT_RemoveGameSupport(Operator):
    bl_idname = "aether.remove_game_support"
    bl_label = "Remove Game Support"
    bl_description = "Removes all Bones and systems that make the Armature compatible for the Game/Engine it is for. This is irreversable. " \
    "Results in an overall better Rig"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        ## Our goal is to rename or vertex groups from the original deformation bones to the new rigify bones but only if a rigify bone for that original bone exists. If not, we will keep the original bone and its vertex group.
        ## For this we need a map. Mapping the oriinal bone to the corresponding Rigify bone. 
        ## We can fetch this since rn every deformation bone that has a rigify bone, has a copy transforms constraint (Starting with AB-LINK) wich is pointing to a LINK bone, wich is parented to the rigify bone. 

        ## check if armature is selected
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}
        
        ## store current mode
        original_mode = context.active_object.mode

        ## go inot pose mode
        bpy.ops.object.mode_set(mode='POSE')

        ## prepare dict 
        transplant_map = {}  ## map to rename vertex groups 
        reparent_map = {}  ## map to reparent lost childs to new rigify bones.

        ## loop through all deformation bones 
        
        data_bones = armature.data.bones
        pose_bones = armature.pose.bones

        for data_bone in data_bones:
            if data_bone.use_deform:
                pose_bone = pose_bones.get(data_bone.name)
                if not pose_bone:
                    continue
                for constraint in pose_bone.constraints:
                    if constraint.type == 'COPY_TRANSFORMS' and constraint.name.startswith("AB-LINK"):
                        if constraint.target and constraint.subtarget:
                            link_bone = data_bones.get(constraint.subtarget)
                            rigify_bone = link_bone.parent
                            transplant_map[data_bone.name] = rigify_bone.name
                        break
                
        ## Now check for any future lost childs. If a bone is parented to a bone that is going to be deleted, we need to reparent it to the new rigify bone.
        for data_bone in data_bones:
            if data_bone.use_deform:
                if data_bone.name in transplant_map:
                    new_parent_name = transplant_map[data_bone.name]
                    for child in data_bone.children:
                        if child.use_deform and child.name not in transplant_map:
                            reparent_map[child.name] = new_parent_name
            
        print(f"[AetherBlend] Transplant Map: {transplant_map}")

        ## Now we simply rename any vertex group that has the original DEF bone aka the key, to the rigify bone aka the value.
        meshes = armature_utils.find_meshes(armature)

        for mesh in meshes:
            for vertex_group in mesh.vertex_groups:
                if vertex_group.name in transplant_map:
                    old_name = vertex_group.name
                    new_name = transplant_map[vertex_group.name]
                    vertex_group.name = new_name
                    print(f"[AetherBlend] Renamed Vertex Group: {old_name} to {new_name}")

        ## Now we need to enable all new DEF bones and delete all old DEF bones. But only the ones from our dictionary. 
        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = armature.data.edit_bones   

        for old_bone_name, new_bone_name in transplant_map.items():
            old_bone = edit_bones.get(old_bone_name)
            link_bone = edit_bones.get(f"LINK-{old_bone_name}")
            new_bone = edit_bones.get(new_bone_name)
            if old_bone and new_bone:
                new_bone.use_deform = True
                edit_bones.remove(old_bone)
                edit_bones.remove(link_bone)
                print(f"[AetherBlend] Deleted Old DEF Bone: {old_bone_name} and enabled New DEF Bone: {new_bone_name}")

        ## Now we need to reparent any lost childs to the new rigify bones.
        for child_name, new_parent_name in reparent_map.items():
            child_bone = edit_bones.get(child_name)
            new_parent_bone = edit_bones.get(new_parent_name)
            if child_bone and new_parent_bone:
                child_bone.parent = new_parent_bone
                print(f"[AetherBlend] Reparented Lost Child Bone: {child_name} to New Parent Bone: {new_parent_name}")

        ## go back to original mode
        bpy.ops.object.mode_set(mode=original_mode)
        
        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(AETHER_OT_RemoveGameSupport)
    bpy.utils.register_class(AETHER_OT_DeleteNoAnim)
    bpy.utils.register_class(AETHER_OT_SetBoneInheritScale)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_DeleteNoAnim)
    bpy.utils.unregister_class(AETHER_OT_SetBoneInheritScale)
    bpy.utils.unregister_class(AETHER_OT_RemoveGameSupport)
