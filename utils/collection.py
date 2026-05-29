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


def collection_tree(root_collection: bpy.types.Collection) -> list[bpy.types.Collection]:
    """Returns the root collection and all descendants."""
    collections: list[bpy.types.Collection] = []
    stack = [root_collection]
    seen: set[str] = set()

    while stack:
        current = stack.pop()
        if current.name in seen:
            continue
        seen.add(current.name)
        collections.append(current)
        for child in current.children:
            stack.append(child)

    return collections


def find_object_name_in_prefixed_collections(
    collections: list[bpy.types.Collection],
    name_prefix: str,
    object_name_match: callable,
) -> str | None:
    """Finds the first object name in collections whose names start with prefix and match predicate."""
    uppercase_prefix = name_prefix.upper()
    for collection in collections:
        if not collection.name.upper().startswith(uppercase_prefix):
            continue
        for obj in collection.objects:
            if object_name_match(obj.name):
                return obj.name
    return None