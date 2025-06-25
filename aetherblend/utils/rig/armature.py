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

def reset_armature_transforms(armature):
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