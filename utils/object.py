import bpy
from collections import defaultdict
import os

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
  
def get_icon(obj):
    """Returns the icon for the given object type."""
    return bpy.types.Object.bl_rna.properties['type'].enum_items[obj.type].icon

def parent_objects(objects, parent_obj, keep_transform=True):
    """Parents a list of objects to a given parent object."""
    bpy.ops.object.mode_set(mode="OBJECT")  

    for obj in objects:
        try:
            if obj != parent_obj:  
                obj.parent = parent_obj
                obj.matrix_parent_inverse = parent_obj.matrix_world.inverted() if keep_transform else obj.matrix_parent_inverse
        except ReferenceError:
            print(f"[AetherBlend] Skipping deleted object: {obj}")    

def delete_rna_from_objects(objects):
    """Deletes the RNA data from a list of objects, returning only those that are still valid."""
    new_objects = set()
    for obj in objects:
        try:
            if obj.name:
                new_objects.add(obj)
        except ReferenceError:
            pass    
    return new_objects

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

def add_armature_modifier(mesh_obj: bpy.types.Object, armature_obj: bpy.types.Object) -> None:
    """
    Adds a new armature modifier to the mesh object for the given armature.
    """
    if mesh_obj.type != 'MESH':
        return

    original_mode = mesh_obj.mode
    object_state = mesh_obj.hide_get()
    try:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        mesh_obj.hide_set(False)
        mesh_obj.select_set(True)
        bpy.context.view_layer.objects.active = mesh_obj
        mod = mesh_obj.modifiers.new(name="Armature", type="ARMATURE")
        mod.object = armature_obj
    except Exception as e:
        print(f"[AetherBlend] Failed to add armature modifier: {e}")
    finally:
        mesh_obj.hide_set(object_state)
        bpy.ops.object.mode_set(mode=original_mode)

def remove_shapekey(obj: bpy.types.Object, shapekey_name: str) -> None:
    """
    Removes the specified shapekey from the object if it exists.
    """
    if obj.type != 'MESH' or not obj.data.shape_keys:
        return

    if obj.data.shape_keys:
        sk = obj.data.shape_keys.key_blocks.get(shapekey_name)
        if sk:
            obj.shape_key_remove(sk)