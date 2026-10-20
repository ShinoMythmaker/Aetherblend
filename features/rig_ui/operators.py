"""Operators for using a generated rig: layers and eyelid editing."""

import bpy

from ..rig_generator import instructions

EYELID_ANCHOR_BONES = [
    "lid.anchor.B.L.001",
    "lid.anchor.B.L.002",
    "lid.anchor.B.L.003",
    "lid.anchor.B.R.001",
    "lid.anchor.B.R.002",
    "lid.anchor.B.R.003",
]


class AETHER_OT_rig_ui_solo_collections(bpy.types.Operator):
    bl_idname = "aether.rig_ui_solo_collections"
    bl_label = "Solo Selected"
    bl_description = "Toggle solo for bone collections."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        armature = context.active_object
        if not armature or armature.type != "ARMATURE":
            return {"CANCELLED"}

        mode = bpy.context.mode
        if mode not in {"POSE", "EDIT_ARMATURE"}:
            return {"CANCELLED"}

        any_soloed = any(collection.is_solo for collection in armature.data.collections)

        if any_soloed:
            for collection in armature.data.collections:
                collection.is_solo = False
        else:
            selected_bones = context.selected_pose_bones if context.mode == "POSE" else []

            if not selected_bones:
                return {"CANCELLED"}

            selected_collections = set()
            for pose_bone in selected_bones:
                bone = armature.data.bones.get(pose_bone.name)
                if bone:
                    for collection in bone.collections:
                        selected_collections.add(collection)

            if not selected_collections:
                return {"CANCELLED"}

            for collection in selected_collections:
                collection.is_solo = True

        return {"FINISHED"}


######
# UI Links
######


class AETHER_OT_rig_ui_eyelid_edit_start(bpy.types.Operator):
    bl_idname = "aether.rig_ui_eyelid_edit_start"
    bl_label = "Start Editing Eye Lid Offset"
    bl_description = "Solo the eye anchor bones and unlock them so the eye lid offset can be adjusted"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
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
            instructions.restrict(armature, bone_name, lock_location=False, lock_rotation=False, lock_scale=False)

        return {"FINISHED"}


class AETHER_OT_rig_ui_eyelid_edit_end(bpy.types.Operator):
    bl_idname = "aether.rig_ui_eyelid_edit_end"
    bl_label = "End Editing Eye Lid Offset"
    bl_description = "Lock the eye anchor bones again and leave eye lid edit mode"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        armature = context.active_object
        rig_props = armature.aether_rig
        rig_props.eye_lid_edit_mode = False

        collection = armature.data.collections.get("Eyes_Anchors")
        if collection:
            collection.is_solo = False

        for bone_name in EYELID_ANCHOR_BONES:
            instructions.restrict(armature, bone_name, lock_location=True, lock_rotation=True, lock_scale=True)

        return {"FINISHED"}


def register() -> None:
    """Register this module's classes."""
    bpy.utils.register_class(AETHER_OT_rig_ui_solo_collections)
    bpy.utils.register_class(AETHER_OT_rig_ui_eyelid_edit_start)
    bpy.utils.register_class(AETHER_OT_rig_ui_eyelid_edit_end)


def unregister() -> None:
    """Unregister this module's classes."""
    bpy.utils.unregister_class(AETHER_OT_rig_ui_eyelid_edit_end)
    bpy.utils.unregister_class(AETHER_OT_rig_ui_eyelid_edit_start)
    bpy.utils.unregister_class(AETHER_OT_rig_ui_solo_collections)
