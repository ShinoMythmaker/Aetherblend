import os
import bpy

def import_model(filepath: str, pack_images=True, disable_bone_shape=False, merge_vertices=False):
    """Imports GLTF or FBX. Returns list of imported objects."""
    scene_objects = set(bpy.context.scene.objects)
    ext = os.path.splitext(filepath)[1].lower()

    if ext in [".gltf", ".glb"]:
        bpy.ops.import_scene.gltf(
            filepath=filepath,
            import_pack_images=pack_images,
            disable_bone_shape=disable_bone_shape,
            merge_vertices=merge_vertices
        )
        # Remove glTF garbage collection if present
        garbage_collection = bpy.data.collections.get("glTF_not_exported")
        if garbage_collection:
            bpy.data.collections.remove(garbage_collection)
    elif ext == ".fbx":
        bpy.ops.import_scene.fbx(filepath=filepath)
    else:
        raise ValueError(f"[AetherBlend] Unsupported file extension: {ext}")

    imported_objs = [obj for obj in bpy.context.scene.objects if obj not in scene_objects]

    return imported_objs