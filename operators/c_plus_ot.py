import bpy
from .. import utils


class AETHER_OT_QuickApplyCustomizePlus(bpy.types.Operator):
    bl_label = "Apply C+ Bone Transforms"
    bl_idname = "aether.q_apply_cplus_string"
    bl_description = (
        "Apply C+ transforms to armature and shapekeys."
    )
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.active_object
        settings = getattr(armature, 'aether_cplus', None)
        cplus_string = settings.code.strip()

        if not armature or armature.type != "ARMATURE":
            self.report({'ERROR'}, "Please select a valid armature.")
            return {'CANCELLED'}

        version, cplus_dict = utils.c_plus.translate_hash(cplus_string)
        if not cplus_dict or version != 4:
            self.report({'ERROR'}, "Invalid or unsupported C+ string (must be version 4).")
            return {'CANCELLED'}

        scale_dict = utils.c_plus.get_bone_values(cplus_dict, 'Scaling')
        rot_dict = utils.c_plus.get_bone_values(cplus_dict, 'Rotation')
        pos_dict = utils.c_plus.get_bone_values(cplus_dict, 'Translation')

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = armature
        parent_map = utils.armature.snapshot_parenting(armature)

        utils.armature.unparent_all_bones(armature)

        ffxiv_bones =utils.armature.b_collection.get_pose_bones(armature, "FFXIV")
        utils.c_plus.apply_transforms(armature, scale_dict, rot_dict, pos_dict, ffxiv_bones)

        utils.armature.apply_all_as_shapekey(armature, shapekey_name="CPlus")

        utils.armature.new_rest_pose(armature)

        utils.armature.restore_bone_parenting(armature, parent_map)

        settings.applied = True

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = armature

        self.report({'INFO'}, "C+ transforms applied, shapekeys baked, rest pose set, parenting and modifiers restored.")
        return {'FINISHED'}   

class AETHER_OT_CreateREFCollection(bpy.types.Operator):
    bl_label = "Create REF Collection"
    bl_idname = "aether.create_ref_collection"
    bl_description = "Creates the FFXIV-REF collection for storing reference bones."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context) -> set[str]:
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "[AetherBlend] Select a valid armature object.")
            return {'CANCELLED'}

        bone_collections = armature.data.collections
        ffxiv_col = bone_collections.get('FFXIV')
        ref_col = bone_collections.get('FFXIV-REF')
        if not ffxiv_col:
            self.report({'ERROR'}, "[AetherBlend] No FFXIV bone collection found.")
            return {'CANCELLED'}

        if ref_col:
            utils.armature.b_collection.delete_with_bones(armature, ref_col.name)

        ref_col = bone_collections.new('FFXIV-REF')

        bpy.ops.object.mode_set(mode='POSE')
        utils.armature.bone.select_edit(armature, [b.name for b in ffxiv_col.bones])

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.duplicate()

        bpy.ops.armature.collection_assign(name=ref_col.name)
        bpy.ops.armature.collection_unassign(name=ffxiv_col.name)


        bpy.ops.object.mode_set(mode='POSE')
        new_bones = []
        for bone in ref_col.bones:
            name = bone.name
            if "." in name:
                name = name.split(".")[0]
            bone.name = f"REF-{name}"
            new_bones.append(bone.name)
            
        bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, f"[AetherBlend] Created/updated FFXIV-REF collection with {len(new_bones)} bones.")
        return {'FINISHED'}
    
class AETHER_OT_RevertToREF(bpy.types.Operator):
    bl_label = "Revert to REF Collection"
    bl_idname = "aether.revert_cplus_to_ref"
    bl_description = (
        "Reverts the armature to the FFXIV-REF collection."
    )
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ### This is WIP and just a dummy rn ###
        armature = context.active_object
        cplus = getattr(armature, 'aether_cplus', None)

        ref_col = armature.data.collections.get('FFXIV-REF')
        ref_bone_names = [b.name for b in ref_col.bones] if ref_col else []

        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = armature.data.edit_bones
        for ref_name in ref_bone_names:
            ref_edit = edit_bones.get(ref_name)
            ffxiv_name = ref_name[4:] if ref_name.startswith('REF-') else ref_name
            ffxiv_edit = edit_bones.get(ffxiv_name)
            if ref_edit and ffxiv_edit:
                ffxiv_edit.head = ref_edit.head.copy()
                ffxiv_edit.tail = ref_edit.tail.copy()
                ffxiv_edit.roll = ref_edit.roll

        meshes = utils.armature.find_meshes(armature)

        for mesh_obj in meshes:
            utils.object.remove_shapekey(mesh_obj, "CPlus")

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = armature

        cplus.applied = False
        self.report({'INFO'}, "Reverted CPlus changes to Reference Collection.")
        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(AETHER_OT_QuickApplyCustomizePlus)
    bpy.utils.register_class(AETHER_OT_CreateREFCollection)
    bpy.utils.register_class(AETHER_OT_RevertToREF)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_QuickApplyCustomizePlus)
    bpy.utils.unregister_class(AETHER_OT_CreateREFCollection)
    bpy.utils.unregister_class(AETHER_OT_RevertToREF)
