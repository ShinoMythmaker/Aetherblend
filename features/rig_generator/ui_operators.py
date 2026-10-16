import bpy

from .operations import BoneRestrictionOperation

EYELID_ANCHOR_BONES = [
    "lid.anchor.B.L.001", "lid.anchor.B.L.002", "lid.anchor.B.L.003",
    "lid.anchor.B.R.001", "lid.anchor.B.R.002", "lid.anchor.B.R.003",
]


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


######
# UI Links
######

class AETHER_OT_EyeLidOffsetEditStart(bpy.types.Operator):
    bl_idname = "aether.eyelid_offset_edit_start"
    bl_label = "Start Editing Eye Lid Offset"
    bl_description = "Begin interactively editing the eye lid control offset by dragging in the 3D view"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.active_object
        rig_props = armature.aether_rig
        rig_props.eye_lid_edit_mode = True
        # now unsolo every collection and only solo the EyesAnchors collections
        for collection in armature.data.collections:
            collection.is_solo = False
        collection = armature.data.collections.get("Eyes_Anchors")
        if collection:
            collection.is_solo = True

        for bone_name in EYELID_ANCHOR_BONES:
            RestrictOp = BoneRestrictionOperation(time="Post", bone_name=bone_name, lock_location=[False, False, False], lock_rotation=[False, False, False], lock_scale=[False, False, False])
            RestrictOp.apply(armature=armature)

        return {'FINISHED'}


class AETHER_OT_EyeLidOffsetEditEnd(bpy.types.Operator):
    bl_idname = "aether.eyelid_offset_edit_end"
    bl_label = "End Editing Eye Lid Offset"
    bl_description = "Finish interactively editing the eye lid control offset and apply the changes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.active_object
        rig_props = armature.aether_rig
        rig_props.eye_lid_edit_mode = False

        collection = armature.data.collections.get("Eyes_Anchors")
        if collection:
            collection.is_solo = False

        for bone_name in EYELID_ANCHOR_BONES:
            RestrictOp = BoneRestrictionOperation(time="Post", bone_name=bone_name, lock_location=[True, True, True], lock_rotation=[True, True, True], lock_scale=[True, True, True])
            RestrictOp.apply(armature=armature)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(AETHER_OT_Solo_Bone_Collections)
    bpy.utils.register_class(AETHER_OT_EyeLidOffsetEditStart)
    bpy.utils.register_class(AETHER_OT_EyeLidOffsetEditEnd)


def unregister():
    bpy.utils.unregister_class(AETHER_OT_EyeLidOffsetEditEnd)
    bpy.utils.unregister_class(AETHER_OT_EyeLidOffsetEditStart)
    bpy.utils.unregister_class(AETHER_OT_Solo_Bone_Collections)
