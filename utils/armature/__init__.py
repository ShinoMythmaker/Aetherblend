from . import b_collection

import bpy

def _select_single(obj: bpy.types.Object):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

def find_armature_in_objects(objects):
    """Finds the first armature in the objects imported."""
    for obj in objects:
        try:
            if obj.type == 'ARMATURE':
                return obj 
        except ReferenceError:
            print(f"[AetherBlend] Skipping deleted object: {obj}")  
    return None

def reset_pose_bones(armature: bpy.types.Object) -> None:
    """Reset all pose bone transforms (location/rotation/scale) to default."""
    if not armature or armature.type != 'ARMATURE':
        return

    original_mode = armature.mode
    _select_single(armature)

    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.transforms_clear()
    bpy.ops.pose.select_all(action='DESELECT')

    bpy.ops.object.mode_set(mode=original_mode)
    print(f"[AetherBlend] Pose bones of armature '{armature.name}' reset to default.")

def unparent_all_bones(armature: bpy.types.Object) -> None:
    """Unparents all bones in the given armature."""
    original_mode = armature.mode
    bpy.ops.object.mode_set(mode='EDIT')
    for bone in armature.data.edit_bones:
        bone.parent = None
    bpy.ops.object.mode_set(mode=original_mode)

def find_meshes(armature: bpy.types.Object) -> list:
    """Returns all mesh objects that use the given armature modifier."""
    meshes = []
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            for mod in obj.modifiers:
                if mod.type == 'ARMATURE' and mod.object == armature:
                    meshes.append(obj)
                    break
    return meshes

def _apply_as_shapekey(mesh_obj: bpy.types.Object, armature_obj: bpy.types.Object, shapekey_name: str = "Armature_Shapekey", disable_all: bool = True) -> None:
    """Applies all armature modifiers using armature_obj as a new shapekey."""
    original_mode = mesh_obj.mode
    object_state = mesh_obj.hide_get()
    try:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
                
        mesh_obj.hide_set(False)
        mesh_obj.select_set(True)
        
        bpy.context.view_layer.objects.active = mesh_obj

        
        armature_mods = [m for m in mesh_obj.modifiers if m.type == 'ARMATURE' and m.object == armature_obj]
        for mod in armature_mods:

            bpy.ops.object.modifier_apply_as_shapekey(modifier=mod.name, keep_modifier=True)

            if mesh_obj.data.shape_keys and disable_all:
                for key_block in mesh_obj.data.shape_keys.key_blocks:
                    key_block.mute = True

            mesh_obj.data.shape_keys.key_blocks[-1].name = shapekey_name
            mesh_obj.data.shape_keys.key_blocks[-1].value = 1.0
            mesh_obj.data.shape_keys.key_blocks[-1].mute = False    

    except Exception as e:
        print(f"[AetherBlend] Failed to apply armature modifier as shapekey on '{mesh_obj.name}': {e}")
    finally:
        mesh_obj.hide_set(object_state)
    bpy.ops.object.mode_set(mode=original_mode)

def apply_all_as_shapekey(armature_obj: bpy.types.Object, shapekey_name: str = "Armature_Shapekey", disable_all: bool = True) -> list:
    """Applies armature modifiers as shapekeys to all meshes using this armature."""
    meshes = find_meshes(armature_obj)
    for mesh_obj in meshes:
        _apply_as_shapekey(mesh_obj, armature_obj, shapekey_name, disable_all=disable_all)
    return meshes


def new_rest_pose(armature: bpy.types.Object) -> None:
    """Applies the current pose as the new rest pose for the armature."""
    original_mode = armature.mode
    bpy.ops.object.mode_set(mode='OBJECT')
    _select_single(armature)
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.armature_apply()
    bpy.ops.object.mode_set(mode=original_mode)


def snapshot_parenting(armature: bpy.types.Object) -> dict:
    """Returns a mapping of bone names to their current parent names."""
    original_mode = armature.mode
    bpy.ops.object.mode_set(mode='EDIT')
    parent_map = {}
    for bone in armature.data.edit_bones:
        parent_map[bone.name] = bone.parent.name if bone.parent else None
    bpy.ops.object.mode_set(mode=original_mode)
    return parent_map

def restore_bone_parenting(armature: bpy.types.Object, parent_map: dict) -> None:
    """Restores bone parenting from a map produced by snapshot_parenting."""
    original_mode = armature.mode
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones
    for bone_name, parent_name in parent_map.items():
        bone = edit_bones.get(bone_name)
        if bone:
            bone.parent = edit_bones.get(parent_name) if parent_name else None
    bpy.ops.object.mode_set(mode=original_mode)

def duplicate(armature: bpy.types.Object) -> bpy.types.Object:
    """Duplicates the given armature object."""
    _select_single(armature)
    bpy.ops.object.duplicate_move()
    duplicated_armature = bpy.context.active_object
    return duplicated_armature

def add_bone_prefix(armature: bpy.types.Object, prefix: str) -> None:
    """Adds a prefix to all bone names in the armature."""
    original_mode = armature.mode
    bpy.ops.object.mode_set(mode='EDIT')
    for bone in armature.data.edit_bones:
        bone.name = f"{prefix}{bone.name}"
    bpy.ops.object.mode_set(mode=original_mode)

def join(src: bpy.types.Object, target: bpy.types.Object) -> None:
    """Joins the source armature into the target armature."""
    bpy.ops.object.select_all(action='DESELECT')
    src.select_set(True)
    target.select_set(True)
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.join()