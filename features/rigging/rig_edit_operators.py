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
    bl_description = (
        "Removes bones and systems used for game/engine compatibility. "
        "This is irreversible, but animation data persists."
    )
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Are you sure? This is irreversible!", icon='ERROR')

    def execute(self, context):
        ## What we do here is actually quite simple. Rename all vertex groups to the Rigify DEF bones. 
        ## Then delete all LINK and orginal bones that have no longer any influence
        ## At last we reparent all remaining children to there new parents. 
        ## Since we are not changing any rigify bones, this can be done without harming animation data. 
        ## Downsides are, no backwards compatibility with the game/engine, other meshes with old vertex groups will no longer work.
        ## Since the original bones no longer exist.

        ## How could we implement a reverse of this ? 
        ## We do have a backup armature we coulkd use to restore the old bones. 
        ## However what about the vertex groups ? I dont want to store the mapping in blender. 
        ## We would have more options if the user would have something like "restore to backup"
        ## then regenerates. Cause then we have basicly the mappings again and could re-rename the vertex groups.
        ## All that wuld be easier if we would store transformLink pairs during rig generation on a custom property from teh armature.
        ## I know i jsut said that i dont want to store the mapping in blender, but this would be a good use case for it.
        ## There are many places where we could use it.
        ## Maybe for another time (Shino) 

        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}

        original_mode = armature_utils._set_mode(armature, 'POSE')
        try:
            bpy.context.window.cursor_set('WAIT')

            transplant_map: dict[str, str] = {}
            reparent_map: dict[str, str] = {}

            data_bones = armature.data.bones
            pose_bones = armature.pose.bones

            for pose_bone in pose_bones:
                if not pose_bone.bone.use_deform:
                    continue

                for constraint in pose_bone.constraints:
                    if constraint.type != 'COPY_TRANSFORMS' or not constraint.name.startswith("AB-LINK"):
                        continue

                    if not (constraint.target and constraint.subtarget):
                        break

                    link_bone = data_bones.get(constraint.subtarget)
                    rigify_bone = link_bone.parent if link_bone else None
                    if rigify_bone:
                        transplant_map[pose_bone.name] = rigify_bone.name
                    break

            for data_bone in data_bones:
                if not data_bone.use_deform or data_bone.name not in transplant_map:
                    continue

                new_parent_name = transplant_map[data_bone.name]
                for child in data_bone.children:
                    if child.use_deform and child.name not in transplant_map:
                        reparent_map[child.name] = new_parent_name

            meshes = armature_utils.find_meshes(armature)
            for mesh in meshes:
                for vertex_group in mesh.vertex_groups:
                    new_name = transplant_map.get(vertex_group.name)
                    if new_name:
                        old_name = vertex_group.name
                        vertex_group.name = new_name

            bpy.ops.object.mode_set(mode='EDIT')
            edit_bones = armature.data.edit_bones

            for old_bone_name, new_bone_name in transplant_map.items():
                old_bone = edit_bones.get(old_bone_name)
                link_bone = edit_bones.get(f"LINK-{old_bone_name}")
                new_bone = edit_bones.get(new_bone_name)
                if not old_bone or not new_bone:
                    continue

                new_bone.use_deform = True
                edit_bones.remove(old_bone)
                if link_bone:
                    edit_bones.remove(link_bone)

            for child_name, new_parent_name in reparent_map.items():
                child_bone = edit_bones.get(child_name)
                new_parent_bone = edit_bones.get(new_parent_name)
                if child_bone and new_parent_bone:
                    child_bone.parent = new_parent_bone

            aether_rig = getattr(armature, 'aether_rig', None)
            if aether_rig is not None:
                aether_rig.converted = True

        finally:
            armature_utils._restore_mode(armature, original_mode)
            bpy.context.window.cursor_set('DEFAULT')

        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(AETHER_OT_RemoveGameSupport)
    bpy.utils.register_class(AETHER_OT_DeleteNoAnim)
    bpy.utils.register_class(AETHER_OT_SetBoneInheritScale)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_DeleteNoAnim)
    bpy.utils.unregister_class(AETHER_OT_SetBoneInheritScale)
    bpy.utils.unregister_class(AETHER_OT_RemoveGameSupport)
