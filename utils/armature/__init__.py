from . import b_collection

import bpy
from mathutils import Vector
from types import SimpleNamespace

def _select_single(obj: bpy.types.Object):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

def reset_transforms(obj: bpy.types.Object) -> None:
    """Resets location, rotation, and scale of the given object."""
    original_mode = obj.mode
    _select_single(obj)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.location_clear()
    bpy.ops.object.rotation_clear()
    bpy.ops.object.scale_clear()
    bpy.ops.object.mode_set(mode=original_mode)

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


def _set_mode(obj: bpy.types.Object, mode: str) -> str:
    original_mode = obj.mode
    if original_mode != mode:
        bpy.ops.object.mode_set(mode=mode)
    return original_mode


def _restore_mode(obj: bpy.types.Object, mode: str) -> None:
    if obj.mode != mode:
        bpy.ops.object.mode_set(mode=mode)


def _get_data_bones(armature: bpy.types.Object, bone_names: list[str]) -> list[bpy.types.Bone]:
    return [armature.data.bones.get(name) for name in bone_names if armature.data.bones.get(name)]


def _get_pose_bones(armature: bpy.types.Object, bone_names: list[str]) -> list[bpy.types.PoseBone]:
    return [armature.pose.bones.get(name) for name in bone_names if armature.pose.bones.get(name)]


def get_bone_visibility(armature: bpy.types.Object, bone_names: list[str]) -> dict[str, tuple[bool, bool]]:
    visibility: dict[str, tuple[bool, bool]] = {}
    for bone_name in bone_names:
        bone = armature.data.bones.get(bone_name)
        if bone:
            visibility[bone_name] = (bone.hide, bone.hide_select)
    return visibility


def restore_visibility(armature: bpy.types.Object, visibility: dict[str, tuple[bool, bool]]) -> None:
    for bone_name, (hide, hide_select) in visibility.items():
        bone = armature.data.bones.get(bone_name)
        if bone:
            bone.hide = hide
            bone.hide_select = hide_select


def exist(armature: bpy.types.Object, bone_names: list[str]) -> bool:
    return all(armature.data.bones.get(name) is not None for name in bone_names)


def _iter_channelbag_fcurves(action, anim_data):
    """Yield (channelbag, fcurve) pairs, supporting both legacy and Blender 4.4+ layered actions."""
    # Legacy actions (Blender < 4.4) expose fcurves directly on the action.
    legacy_fcurves = getattr(action, "fcurves", None)
    if legacy_fcurves is not None:
        for fc in legacy_fcurves:
            yield action.fcurves, fc
        return

    # Layered action format (Blender 4.4+).
    slot = getattr(anim_data, "action_slot", None)
    for layer in getattr(action, "layers", ()):
        for strip in getattr(layer, "strips", ()):
            try:
                channelbag = strip.channelbag(slot) if slot else None
            except Exception:
                channelbag = None
            if channelbag:
                for fc in channelbag.fcurves:
                    yield channelbag.fcurves, fc


def delete_keyframes(armature: bpy.types.Object, bone_names: list[str]) -> None:
    anim_data = getattr(armature, "animation_data", None)
    action = getattr(anim_data, "action", None) if anim_data else None
    if not action:
        return

    data_paths = set()
    for bone_name in bone_names:
        base = f'pose.bones["{bone_name}"]'
        for suffix in ("location", "rotation_euler", "rotation_quaternion", "scale"):
            data_paths.add(f"{base}.{suffix}")

    to_remove = [
        (fcurves_coll, fc)
        for fcurves_coll, fc in _iter_channelbag_fcurves(action, anim_data)
        if fc.data_path in data_paths
    ]
    for fcurves_coll, fc in to_remove:
        fcurves_coll.remove(fc)


def select_edit(armature: bpy.types.Object, bone_names: list[str]) -> None:
    original_mode = _set_mode(armature, 'EDIT')
    bpy.ops.armature.select_all(action='DESELECT')
    for bone_name in bone_names:
        bone = armature.data.edit_bones.get(bone_name)
        if bone:
            bone.select = True
            bone.select_head = True
            bone.select_tail = True
    _restore_mode(armature, original_mode)
    _set_mode(armature, 'POSE')
    bpy.ops.pose.select_all(action='DESELECT')
    for bone_name in bone_names:
        pose_bone = armature.pose.bones.get(bone_name)
        if pose_bone:
            pose_bone.select = True


def add_constraint_copy_rotation(source_bone_names: list[str], armature: bpy.types.Object, target_bone_names: list[str], overwrite: bool = False) -> None:
    for source_name, target_name in zip(source_bone_names, target_bone_names):
        pose_bone = armature.pose.bones.get(source_name)
        if not pose_bone:
            continue
        if overwrite:
            for constraint in [c for c in pose_bone.constraints if c.type == 'COPY_ROTATION' and c.name == 'spring']:
                pose_bone.constraints.remove(constraint)
        constraint = pose_bone.constraints.new('COPY_ROTATION')
        constraint.name = 'spring'
        constraint.target = armature
        constraint.subtarget = target_name
        constraint.mix_mode = 'REPLACE'
        constraint.use_x = True
        constraint.use_y = True
        constraint.use_z = True


def remove_copy_rotation_constraints(armature: bpy.types.Object, bone_names: list[str]) -> None:
    for bone_name in bone_names:
        pose_bone = armature.pose.bones.get(bone_name)
        if not pose_bone:
            continue
        for constraint in [c for c in pose_bone.constraints if c.type == 'COPY_ROTATION']:
            pose_bone.constraints.remove(constraint)


def bone_chain(armature: bpy.types.Object, reference_bone_names: list[str], prefix: str = "", parent_bone: str | None = None) -> list[str]:
    if not reference_bone_names:
        return []

    original_mode = _set_mode(armature, 'EDIT')
    edit_bones = armature.data.edit_bones
    created: list[str] = []
    previous_name: str | None = None

    for index, reference_name in enumerate(reference_bone_names):
        source_bone = edit_bones.get(reference_name)
        if not source_bone:
            continue

        new_name = f"{prefix}{reference_name}"
        if edit_bones.get(new_name):
            edit_bones.remove(edit_bones[new_name])

        new_bone = edit_bones.new(new_name)
        new_bone.head = source_bone.head.copy()
        new_bone.tail = source_bone.tail.copy()
        new_bone.roll = source_bone.roll

        if previous_name:
            new_bone.parent = edit_bones.get(previous_name)
            new_bone.use_connect = False
        elif parent_bone:
            new_bone.parent = edit_bones.get(parent_bone)
            new_bone.use_connect = False

        created.append(new_name)
        previous_name = new_name

    _restore_mode(armature, original_mode)
    return created


def bone_on_local_axis_x(armature: bpy.types.Object, reference_bone_name: str, parent_bone: str | None = None, prefix: str = "") -> str | None:
    original_mode = _set_mode(armature, 'EDIT')
    edit_bones = armature.data.edit_bones
    source_bone = edit_bones.get(reference_bone_name)
    if not source_bone:
        _restore_mode(armature, original_mode)
        return None

    new_name = f"{prefix}{reference_bone_name}"
    if edit_bones.get(new_name):
        edit_bones.remove(edit_bones[new_name])

    new_bone = edit_bones.new(new_name)
    new_bone.head = source_bone.head.copy()
    local_x = source_bone.matrix.to_3x3().col[0].normalized()
    new_bone.tail = new_bone.head + local_x * max(source_bone.length, 0.001)
    new_bone.roll = source_bone.roll

    if parent_bone:
        new_bone.parent = edit_bones.get(parent_bone)
        new_bone.use_connect = False

    _restore_mode(armature, original_mode)
    return new_name


def reset_bone_transforms(armature: bpy.types.Object, bone_names: list[str]) -> None:
    """Reset pose-bone location/rotation/scale to rest for each named bone."""
    original_mode = armature.mode
    _set_mode(armature, 'POSE')
    for bone_name in bone_names:
        pose_bone = armature.pose.bones.get(bone_name)
        if pose_bone:
            pose_bone.location = (0.0, 0.0, 0.0)
            pose_bone.rotation_euler = (0.0, 0.0, 0.0)
            pose_bone.rotation_quaternion = (1.0, 0.0, 0.0, 0.0)
            pose_bone.scale = (1.0, 1.0, 1.0)
    _set_mode(armature, original_mode)


bone = SimpleNamespace(
    get_bone_visibility=get_bone_visibility,
    restore_visibility=restore_visibility,
    exist=exist,
    delete_keyframes=delete_keyframes,
    select_edit=select_edit,
    add_constraint_copy_rotation=add_constraint_copy_rotation,
    remove_copy_rotation_constraints=remove_copy_rotation_constraints,
    reset_transforms=reset_bone_transforms,
)


generate = SimpleNamespace(
    bone_chain=bone_chain,
    bone_on_local_axis_x=bone_on_local_axis_x,
)
