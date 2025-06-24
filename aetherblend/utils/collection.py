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

def unlink_from_collection(collection):
    """Unlinks all objects and sub-collections from the given collection while keeping the objects in the scene."""
    scene_collection = bpy.context.scene.collection  

    for obj in list(collection.objects): 
        collection.objects.unlink(obj)  
        scene_collection.objects.link(obj) 
            
    for sub_collection in list(collection.children):       
        collection.children.unlink(sub_collection)  
        scene_collection.children.link(sub_collection)

def create_collection(name="Collection"):
    """Creates a Collection"""
    new_collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(new_collection)
    return new_collection 

def get_collection(object):
    """Returns the collection that contains this object."""
    for collection in bpy.data.collections:
        if any(object is coll_obj for coll_obj in collection.objects): 
            return collection  
    return None  