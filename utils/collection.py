import bpy

def link_to_collection(objects, collection):
    """Links objects to a collection."""
    for obj in objects:
        try:
            for user_collection in obj.users_collection:
                user_collection.objects.unlink(obj)
            collection.objects.link(obj)
        except ReferenceError:
            print(f"[AetherBlend] Skipping deleted object: {obj}")

def create_collection(name="Collection"):
    """Creates a Collection"""
    new_collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(new_collection)
    return new_collection 

def get_collection(obj):
    """Returns the first collection that contains this object."""
    for collection in bpy.data.collections:
        if any(obj is coll_obj for coll_obj in collection.objects):
            return collection  
    return None  