"""Shared bone lookup for instructions."""
import bpy


def get_pose_bone(rig: bpy.types.Object, bone_name: str) -> bpy.types.PoseBone | None:
    """Return the pose bone, or print a warning and return None when it does not exist."""
    pose_bone = rig.pose.bones.get(bone_name)
    if not pose_bone:
        print(f"[AetherBlend] Pose bone '{bone_name}' not found in '{rig.name}'.")
    return pose_bone
