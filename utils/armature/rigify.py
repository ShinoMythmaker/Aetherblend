import bpy
from ...data import *

def _select_pose_bone(pose_bone: bpy.types.PoseBone, state: bool = True) -> None:
    """Helper function to select a pose bone in a version-compatible way.
    
    Blender 5.0+ uses pose_bone.select, while 4.x uses pose_bone.bone.select.
    """
    try:
        pose_bone.select = state
    except AttributeError:
        pose_bone.bone.select = state

