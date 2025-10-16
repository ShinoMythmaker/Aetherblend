from . import generate
from . import bone
from . import b_collection
from . import meta_rig


import bpy

def dupe_with_childs(armature):
    """Duplicates an armature and its children."""
    bpy.ops.object.select_all(action='DESELECT')
    armature.select_set(True)
    for child in armature.children:
        print(child.name)
        child.select_set(True) 
    bpy.ops.object.duplicate_move()

def find_armature_in_objects(objects):
    """Finds the first armature in the objects imported."""
    for obj in objects:
        try:
            if obj.type == 'ARMATURE':
                return obj 
        except ReferenceError:
            print(f"[AetherBlend] Skipping deleted object: {obj}")  
    return None

def get_frame_range(armature):
    """Returns the frame range of the armature's animation."""
    if not armature or not armature.animation_data:
        return (0, 0)
    
    action = armature.animation_data.action
    if not action:
        return (0, 0)
    
    start_frame = int(action.frame_range[0])
    end_frame = int(action.frame_range[1])
    
    return start_frame, end_frame


def delete_keyframes(armature):
    """Deletes all keyframes from the armature."""
    if not armature or not armature.animation_data:
        return

    action = armature.animation_data.action
    if not action:
        return

    for fcurve in action.fcurves:
        action.fcurves.remove(fcurve)

    # Clear the action to remove all keyframes
    action.clear()
    print(f"[AetherBlend] All keyframes deleted from armature '{armature.name}'.")

def reset_transforms(armature):
    """Resets the transforms of the armature."""
    if not armature:
        return

    bpy.ops.object.mode_set(mode='POSE')
    for bone in armature.pose.bones:
        bone.location = (0.0, 0.0, 0.0)
        bone.rotation_euler = (0.0, 0.0, 0.0)
        bone.scale = (1.0, 1.0, 1.0)

    bpy.ops.object.mode_set(mode='OBJECT')
    print(f"[AetherBlend] Transforms of armature '{armature.name}' reset to default.")


def unparent_all_bones(armature: bpy.types.Object) -> None:
    """
    Unparents all bones in the given armature.
    """
    original_mode = armature.mode
    bpy.ops.object.mode_set(mode='EDIT')
    for bone in armature.data.edit_bones:
        bone.parent = None
    bpy.ops.object.mode_set(mode=original_mode)

def find_meshes(armature: bpy.types.Object) -> list:
    """
    Returns a list of mesh objects using the given armature as an armature modifier.
    """
    meshes = []
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            for mod in obj.modifiers:
                if mod.type == 'ARMATURE' and mod.object == armature:
                    meshes.append(obj)
                    break
    return meshes

def apply_as_shapekey(mesh_obj: bpy.types.Object, armature_obj: bpy.types.Object, shapekey_name: str = "Armature_Shapekey") -> None:
    """
    Applies the armature modifier as a shapekey to the mesh object and renames the shapekey.
    """
    original_mode = mesh_obj.mode
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    mesh_obj.select_set(True)
    bpy.context.view_layer.objects.active = mesh_obj

    # Find armature modifiers for this armature (could be more than one, but usually just one)
    armature_mods = [m for m in mesh_obj.modifiers if m.type == 'ARMATURE' and m.object == armature_obj]
    for mod in armature_mods:
        bpy.ops.object.modifier_apply_as_shapekey(modifier=mod.name)
        mesh_obj.data.shape_keys.key_blocks[-1].name = shapekey_name
        mesh_obj.data.shape_keys.key_blocks[-1].value = 1.0

    bpy.ops.object.mode_set(mode=original_mode)

def apply_all_as_shapekey(armature_obj: bpy.types.Object, shapekey_name: str = "Armature_Shapekey") -> list:
    """
    Applies the armature modifier as a shapekey to all mesh objects using the given armature. Returns the list of affected mesh objects.
    """
    meshes = find_meshes(armature_obj)
    for mesh_obj in meshes:
        apply_as_shapekey(mesh_obj, armature_obj, shapekey_name)
    return meshes


def new_rest_pose(armature: bpy.types.Object) -> None:
    """
    Applies the current pose of the armature as the new rest pose.
    """
    original_mode = armature.mode
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.armature_apply()
    bpy.ops.object.mode_set(mode=original_mode)


def snapshot_parenting(armature: bpy.types.Object) -> dict:
    """
    Returns a mapping of bone names to their parent names for the given armature.
    """
    original_mode = armature.mode
    bpy.ops.object.mode_set(mode='EDIT')
    parent_map = {}
    for bone in armature.data.edit_bones:
        parent_map[bone.name] = bone.parent.name if bone.parent else None
    bpy.ops.object.mode_set(mode=original_mode)
    return parent_map

def restore_bone_parenting(armature: bpy.types.Object, parent_map: dict) -> None:
    """
    Restores bone parenting in the armature from the given parent map.
    """
    original_mode = armature.mode
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones
    for bone_name, parent_name in parent_map.items():
        bone = edit_bones.get(bone_name)
        if bone:
            bone.parent = edit_bones.get(parent_name) if parent_name else None
    bpy.ops.object.mode_set(mode=original_mode)

