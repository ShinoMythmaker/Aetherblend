import bpy

def dupe_armature_with_childs(armature):
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
