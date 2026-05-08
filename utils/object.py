import bpy
from collections import defaultdict
import os


def ensure_mode(mode: str = 'OBJECT'):
    """Switches Blender mode only when required."""
    if bpy.context.mode != mode:
        bpy.ops.object.mode_set(mode=mode)


def select_only(obj: bpy.types.Object, mode: str = 'OBJECT'):
    """Select exactly one object and set it as active."""
    ensure_mode(mode)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)


def set_visibility(obj: bpy.types.Object, visible: bool):
    """Sets viewport visibility for an object."""
    obj.hide_set(not visible)
    obj.hide_viewport = not visible


def uses_armature(obj: bpy.types.Object, armature: bpy.types.Object) -> bool:
    """Returns True if object has constraints/modifiers that reference the armature."""
    for constraint in obj.constraints:
        if hasattr(constraint, 'target') and constraint.target == armature:
            return True

    for modifier in obj.modifiers:
        if modifier.type == 'ARMATURE' and modifier.object == armature:
            return True

    if obj.type != 'ARMATURE' or not obj.pose:
        return False

    for pose_bone in obj.pose.bones:
        for constraint in pose_bone.constraints:
            if hasattr(constraint, 'target') and constraint.target == armature:
                return True

    return False


def has_material_property(obj: bpy.types.Object, property_name: str, property_value=None) -> bool:
    """Returns True if object has a material with the given custom property value."""
    if not obj.data or not hasattr(obj.data, 'materials'):
        return False

    for material_slot in obj.material_slots:
        material = material_slot.material
        if not material or property_name not in material:
            continue

        if property_value is None or material[property_name] == property_value:
            return True

    return False


def find_by_armature_and_material_property(
    armature: bpy.types.Object,
    property_name: str,
    property_value=None,
) -> list[bpy.types.Object]:
    """Finds objects driven by an armature and matching a material property filter."""
    return [
        obj
        for obj in bpy.data.objects
        if uses_armature(obj, armature)
        and has_material_property(obj, property_name, property_value)
    ]


def merge_by_material(objects):
    """Merges objects that share the same material and returns the updated list of all objects, including non-mesh objects that were not modified."""
    material_mesh_groups = defaultdict(list)
    all_objects = set(objects)  

    for obj in objects:
        try:
            if obj.type == "MESH" and obj.data.materials:
                material_name = obj.data.materials[0].name
                material_mesh_groups[material_name].append(obj)
        except ReferenceError:
            print(f"[AetherBlend] Skipping deleted object: {obj}")

    new_objects = set()  

    for material, meshes in material_mesh_groups.items():
        if len(meshes) < 2:
            new_objects.update(meshes)  # Keep unmerged meshes
            continue
        bpy.ops.object.select_all(action='DESELECT')
        for mesh in meshes:
            mesh.select_set(True)
        bpy.context.view_layer.objects.active = meshes[0]
        bpy.ops.object.join()
        merged_object = bpy.context.view_layer.objects.active
        new_objects.add(merged_object)
        bpy.ops.object.select_all(action='DESELECT')

    non_mesh_objects = set()
    for obj in all_objects:
        try:
            if obj.type != "MESH":
                non_mesh_objects.add(obj)
        except ReferenceError:
            print(f"[AetherBlend] Skipping deleted object: {obj}")
    
    updated_objects = new_objects | non_mesh_objects  

    return list(updated_objects)

def merge_by_name(objects, name_filter):
    """Merges all objects in the given list that contain the specified name_filter in their name. Returns an updated object list."""
    filtered_objects = [obj for obj in objects if name_filter.lower() in obj.name.lower() and obj.type == "MESH"]
    
    updated_objects = set(objects)

    if len(filtered_objects) < 2:
        return list(updated_objects)  

    bpy.ops.object.select_all(action='DESELECT')  
    for obj in filtered_objects:
        obj.select_set(True)

    bpy.context.view_layer.objects.active = filtered_objects[0]  
    bpy.ops.object.join() 

    merged_object = bpy.context.view_layer.objects.active

    updated_objects.difference_update(filtered_objects)  
    updated_objects.add(merged_object) 

    bpy.ops.object.select_all(action='DESELECT') 

    return list(updated_objects)  

def import_meddle_shader(filepath, imported_objects):
    """Imports Meddle shaders for the given objects."""
    for obj in imported_objects:
        try:
            if obj and obj.type == "MESH": 
                obj.select_set(True)
        except ReferenceError:
            print(f"Skipping deleted object: {obj}")  
        
    character_directory = os.path.dirname(filepath)
    meddle_cache_directory = os.path.join(character_directory, "cache","")

    try:
        bpy.ops.meddle.import_shaders('EXEC_DEFAULT')  
        bpy.ops.meddle.apply_to_selected('EXEC_DEFAULT', directory=meddle_cache_directory)  
    except Exception as e:
        print(f"[AetherBlend] Failed to append Meddle shaders: {e}")

def remove_shapekey(obj: bpy.types.Object, shapekey_name: str, enable_backup: bool = False, backup_shapekey_name: str = None) -> None:
    """
    Removes the specified shapekey from the object if it exists, or handles backup unmuting.
    """
    if obj.type != 'MESH' or not obj.data.shape_keys:
        return

    if enable_backup:
        if backup_shapekey_name:
            sk = obj.data.shape_keys.key_blocks.get(backup_shapekey_name)
            if sk:
                sk.mute = False
            else:
                for key_block in obj.data.shape_keys.key_blocks:
                    key_block.mute = False
        else:
            for key_block in obj.data.shape_keys.key_blocks:
                key_block.mute = False
                
        if obj.data.shape_keys:
            sk = obj.data.shape_keys.key_blocks.get(shapekey_name)
            if sk:
                obj.shape_key_remove(sk)