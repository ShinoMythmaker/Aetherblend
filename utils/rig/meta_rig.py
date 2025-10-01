import bpy
from .bone import bones_exist, assign_bones_to_collection, add_constraint_copy_rotation, remove_copy_rotation_constraints, collection_exists
from .generate import meta_rig_bone_chain
from ...data.constants import (
    meta_rig_arm_l_bones, meta_rig_arm_r_bones, 
    meta_rig_leg_l_bones, meta_rig_leg_r_bones,
    meta_rig_arm_l_chain, meta_rig_arm_r_chain,
    meta_rig_leg_l_chain, meta_rig_leg_r_chain,
    meta_rig_arm_l_names, meta_rig_arm_r_names,
    meta_rig_leg_l_names, meta_rig_leg_r_names,
    meta_rig_prefix, meta_rig_collection
)

def create_meta_rig_collections(armature):
    """Creates the required bone collections for a meta rig."""
    
    if not armature or armature.type != 'ARMATURE':
        print(f"[AetherBlend] Object '{armature.name}' is not an armature.")
        return
        
    # Collection names as they appear in rigify
    collections_to_create = [
        "Arm.L (IK)",
        "Arm.L (FK)", 
        "Arm.L (Tweak)",
        "Arm.R (IK)",
        "Arm.R (FK)",
        "Arm.R (Tweak)"
    ]
    
    # Switch to edit mode to access bone collections
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    
    for collection_name in collections_to_create:
        # Use utility function to check if collection already exists
        if not collection_exists(armature, collection_name):
            armature.data.collections.new(collection_name)
            print(f"[AetherBlend] Created bone collection: {collection_name}")
        else:
            print(f"[AetherBlend] Bone collection already exists: {collection_name}")
    
    bpy.ops.object.mode_set(mode='OBJECT')

def setup_rigify_arm_properties(armature, upper_arm_bone_name, side="L"):
    """Sets up rigify properties for an arm upper bone.
    
    Args:
        armature: The armature containing the bone
        upper_arm_bone_name: Name of the upper arm bone
        side: "L" or "R" for left or right arm
    """
    
    if not armature or armature.type != 'ARMATURE':
        print(f"[AetherBlend] Object '{armature.name}' is not an armature.")
        return
        
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    
    if upper_arm_bone_name not in armature.data.edit_bones:
        print(f"[AetherBlend] Upper arm bone '{upper_arm_bone_name}' not found in armature.")
        bpy.ops.object.mode_set(mode='OBJECT')
        return
    
    bpy.ops.object.mode_set(mode='POSE')
    
    # Get the pose bone
    pose_bone = armature.pose.bones.get(upper_arm_bone_name)
    if not pose_bone:
        print(f"[AetherBlend] Pose bone '{upper_arm_bone_name}' not found.")
        bpy.ops.object.mode_set(mode='OBJECT')
        return
    
    # Select and activate the pose bone - this is required for the rigify operator
    bpy.ops.pose.select_all(action='DESELECT')
    pose_bone.bone.select = True
    armature.data.bones.active = pose_bone.bone
    
    # Set rigify type to limbs.arm
    pose_bone.rigify_type = "limbs.arm"
    
    # Collection names
    fk_collection_name = f"Arm.{side} (FK)"
    tweak_collection_name = f"Arm.{side} (Tweak)"
    
    try:
        # Get rigify parameters
        rigify_params = pose_bone.rigify_parameters
        
        # Clear existing collection references first
        rigify_params.fk_coll_refs.clear()
        rigify_params.tweak_coll_refs.clear()
        
        # Add FK collection reference
        if fk_collection_name in armature.data.collections:
            # Use the rigify operator to add a new reference item
            bpy.ops.pose.rigify_collection_ref_add(prop_name="fk_coll_refs")
            
            # Set the collection on the newly added item using .name property
            if len(rigify_params.fk_coll_refs) > 0:
                fk_ref = rigify_params.fk_coll_refs[-1]
                fk_ref.name = fk_collection_name
                print(f"[AetherBlend] Added FK collection reference: '{fk_collection_name}'")
        else:
            print(f"[AetherBlend] FK collection '{fk_collection_name}' not found")
        
        # Add Tweak collection reference
        if tweak_collection_name in armature.data.collections:
            # Use the rigify operator to add a new reference item
            bpy.ops.pose.rigify_collection_ref_add(prop_name="tweak_coll_refs")
            
            # Set the collection on the newly added item using .name property
            if len(rigify_params.tweak_coll_refs) > 0:
                tweak_ref = rigify_params.tweak_coll_refs[-1]
                tweak_ref.name = tweak_collection_name
                print(f"[AetherBlend] Added Tweak collection reference: '{tweak_collection_name}'")
        else:
            print(f"[AetherBlend] Tweak collection '{tweak_collection_name}' not found")
            
    except Exception as e:
        print(f"[AetherBlend] Error setting rigify collection properties: {e}")
    
    print(f"[AetherBlend] Set up rigify properties for '{upper_arm_bone_name}' with limbs.arm rig type")
    
    bpy.ops.object.mode_set(mode='OBJECT')

def setup_rigify_standard_colors(armature):
    """Sets up standard rigify colors on the armature."""
    
    if not armature or armature.type != 'ARMATURE':
        print(f"[AetherBlend] Object '{armature.name}' is not an armature.")
        return False
        
    # Make sure the armature is active
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='OBJECT')
    
    try:
        # Use the rigify operator to set standard colors
        bpy.ops.armature.rigify_use_standard_colors()
        print(f"[AetherBlend] Applied standard rigify colors to '{armature.name}'")
        return True
        
    except Exception as e:
        print(f"[AetherBlend] Error setting standard rigify colors: {e}")
        return False

def setup_rigify_color_sets(armature):
    """Sets up rigify color sets on the armature and assigns them to collections."""
    
    if not armature or armature.type != 'ARMATURE':
        print(f"[AetherBlend] Object '{armature.name}' is not an armature.")
        return False
        
    # Make sure the armature is active
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='OBJECT')
    
    try:
        # First, add standard rigify color sets
        bpy.ops.armature.rigify_add_color_sets()
        print(f"[AetherBlend] Added standard rigify color sets")
        
        # Now assign color sets to our collections
        assign_color_sets_to_collections(armature)
        
        print(f"[AetherBlend] Color sets setup completed for '{armature.name}'")
        return True
        
    except Exception as e:
        print(f"[AetherBlend] Error setting rigify color sets: {e}")
        return False

def assign_color_sets_to_collections(armature):
    """Assigns appropriate color sets to bone collections."""
    
    if not armature or armature.type != 'ARMATURE':
        print(f"[AetherBlend] Object '{armature.name}' is not an armature.")
        return False
        
    # Color set assignments for our collections
    color_assignments = {
        "Arm.L (IK)": "IK",
        "Arm.L (FK)": "FK", 
        "Arm.L (Tweak)": "Tweak",
        "Arm.R (IK)": "IK",
        "Arm.R (FK)": "FK",
        "Arm.R (Tweak)": "Tweak"
    }
    
    assigned_count = 0
    
    for collection_name, color_set_name in color_assignments.items():
        if collection_name in armature.data.collections:
            collection = armature.data.collections[collection_name]
            collection.rigify_color_set_name = color_set_name
            print(f"[AetherBlend] Assigned '{color_set_name}' color set to collection '{collection_name}'")
            assigned_count += 1
        else:
            print(f"[AetherBlend] Collection '{collection_name}' not found for color assignment")
    
    print(f"[AetherBlend] Assigned color sets to {assigned_count} collections")
    return assigned_count > 0

def setup_meta_rig_viewport_display(armature):
    """Sets up viewport display properties for the meta rig armature."""
    
    if not armature or armature.type != 'ARMATURE':
        print(f"[AetherBlend] Object '{armature.name}' is not an armature.")
        return False
        
    try:
        # Set armature to display in front
        armature.show_in_front = True 
        print(f"[AetherBlend] Set up viewport display for meta rig '{armature.name}' (in front)")
        return True
        
    except Exception as e:
        print(f"[AetherBlend] Error setting viewport display properties: {e}")
        return False

def setup_meta_rig_collection_ui(armature):
    """Sets up UI row assignments for bone collections to create the rigify panel layout."""
    
    if not armature or armature.type != 'ARMATURE':
        print(f"[AetherBlend] Object '{armature.name}' is not an armature.")
        return False
        
    try:
        # UI row assignments - collections in the same row appear as buttons on the same row
        ui_assignments = {
            # Row 1: IK controls
            "Arm.L (IK)": 1,
            "Arm.R (IK)": 1,
            
            # Row 2: FK controls  
            "Arm.L (FK)": 2,
            "Arm.R (FK)": 2,
            
            # Row 3: Tweak controls
            "Arm.L (Tweak)": 3,
            "Arm.R (Tweak)": 3,
        }
        
        assigned_count = 0
        
        for collection_name, ui_row in ui_assignments.items():
            if collection_name in armature.data.collections:
                collection = armature.data.collections[collection_name]
                collection.rigify_ui_row = ui_row
                
                # Set UI title if not already set
                if not collection.rigify_ui_title:
                    # Extract the control type from collection name for UI title
                    if "(IK)" in collection_name:
                        side = "L" if ".L" in collection_name else "R"
                        collection.rigify_ui_title = f"IK.{side}"
                    elif "(FK)" in collection_name:
                        side = "L" if ".L" in collection_name else "R" 
                        collection.rigify_ui_title = f"FK.{side}"
                    elif "(Tweak)" in collection_name:
                        side = "L" if ".L" in collection_name else "R"
                        collection.rigify_ui_title = f"Tweak.{side}"
                
                print(f"[AetherBlend] Assigned collection '{collection_name}' to UI row {ui_row} with title '{collection.rigify_ui_title}'")
                assigned_count += 1
            else:
                print(f"[AetherBlend] Collection '{collection_name}' not found for UI assignment")
        
        print(f"[AetherBlend] Set up UI layout for {assigned_count} collections")
        return assigned_count > 0
        
    except Exception as e:
        print(f"[AetherBlend] Error setting up collection UI layout: {e}")
        return False

def assign_rigify_color_set(armature, bone_name, color_set_index):
    """Assigns a rigify color set to a specific bone.
    
    Args:
        armature: The armature containing the bone
        bone_name: Name of the bone to assign color to
        color_set_index: Index of the color set to assign (experimental)
    """
    
    if not armature or armature.type != 'ARMATURE':
        print(f"[AetherBlend] Object '{armature.name}' is not an armature.")
        return False
        
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    
    try:
        pose_bone = armature.pose.bones.get(bone_name)
        if not pose_bone:
            print(f"[AetherBlend] Pose bone '{bone_name}' not found.")
            return False
        
        # TODO: Research the correct way to assign color sets
        # This might involve setting properties on the pose bone or using operators
        
        print(f"[AetherBlend] Color set assignment for '{bone_name}' - TODO: Implement")
        return True
        
    except Exception as e:
        print(f"[AetherBlend] Error assigning color set to '{bone_name}': {e}")
        return False
    finally:
        bpy.ops.object.mode_set(mode='OBJECT')

def create_limb_arm(source_armature, target_armature, side="L", prefix=None, collection_name=None):
    """Creates a meta rig arm limb following j_ude_a_l/r to j_te_l/r with extension.
    
    Args:
        source_armature: FFXIV armature to read bone positions from
        target_armature: Meta rig armature to create bones in
        side: "L" or "R" for left or right arm
        prefix: Optional prefix for bone names
        collection_name: Optional collection name (legacy parameter, now ignored)
    """
    
    if prefix is None:
        prefix = meta_rig_prefix
        
    if not source_armature or source_armature.type != 'ARMATURE':
        print(f"[AetherBlend] Source object '{source_armature.name}' is not an armature.")
        return []
        
    if not target_armature or target_armature.type != 'ARMATURE':
        print(f"[AetherBlend] Target object '{target_armature.name}' is not an armature.")
        return []
    
    # Get the appropriate constants based on side
    if side == "L":
        chain_bones = meta_rig_arm_l_chain
        bone_names = meta_rig_arm_l_names
    elif side == "R":
        chain_bones = meta_rig_arm_r_chain
        bone_names = meta_rig_arm_r_names
    else:
        print(f"[AetherBlend] Invalid side '{side}'. Must be 'L' or 'R'.")
        return []
    
    # Check if required bones exist in source armature
    if not bones_exist(source_armature, chain_bones):
        print(f"[AetherBlend] One or more required arm {side} bones do not exist in source armature '{source_armature.name}'.")
        return []

    # Generate the bone chain using the unified function with both armatures
    created_bones = meta_rig_bone_chain(
        source_armature=source_armature,
        target_armature=target_armature,
        reference_bones=chain_bones,
        meta_bone_names=bone_names,
        prefix=prefix,
        extend_last=True,
        extension_factor=0.4  # Extend hand bone by half bone length
    )
    
    # Assign bones to IK collection
    if created_bones:
        ik_collection_name = f"Arm.{side} (IK)"
        assign_bones_to_collection(target_armature, created_bones, ik_collection_name)
        
        # Set up rigify properties on the upper arm bone (first bone in the chain)
        if len(created_bones) > 0:
            upper_arm_bone = created_bones[0]
            setup_rigify_arm_properties(target_armature, upper_arm_bone, side=side)
    
    print(f"[AetherBlend] Created arm {side} limb with bones: {created_bones}")
    return created_bones

def get_ffxiv_to_control_bone_mapping():
    """Returns a mapping dictionary from FFXIV bone names to control bone names.
    
    This mapping is used to set up constraints when linking control rig to FFXIV rig.
    """
    
    # Define the mapping between FFXIV bones and their control counterparts
    bone_mapping = {
        # Left Arm
        "j_ude_a_l": "ORG-upper_arm.L",
        "j_ude_b_l": "ORG-forearm.L", 
        "j_te_l": "ORG-hand.L",
        
        # Right Arm  
        "j_ude_a_r": "ORG-upper_arm.R",
        "j_ude_b_r": "ORG-forearm.R",
        "j_te_r": "ORG-hand.R",
    }
    
    return bone_mapping

def setup_ffxiv_control_constraints(ffxiv_armature, bone_mapping):
    """Sets up copy rotation constraints from FFXIV bones to control bones.
    
    Args:
        ffxiv_armature: The FFXIV armature containing both original and control bones
        bone_mapping: Dictionary mapping FFXIV bone names to control bone names
    """
    
    if not ffxiv_armature or ffxiv_armature.type != 'ARMATURE':
        print(f"[AetherBlend] Invalid armature for constraint setup")
        return 0
        
    print(f"[AetherBlend] Setting up constraints from FFXIV bones to control bones...")
    
    # Switch to pose mode for constraint operations
    bpy.context.view_layer.objects.active = ffxiv_armature
    bpy.ops.object.mode_set(mode='POSE')
    
    # Prepare lists for the utility function
    ffxiv_bone_names = []
    control_bone_names = []
    
    # Validate and collect bone pairs
    for ffxiv_bone_name, control_bone_name in bone_mapping.items():
        # Check if both bones exist
        ffxiv_pose_bone = ffxiv_armature.pose.bones.get(ffxiv_bone_name)
        control_pose_bone = ffxiv_armature.pose.bones.get(control_bone_name)
        
        if not ffxiv_pose_bone:
            print(f"[AetherBlend] FFXIV bone '{ffxiv_bone_name}' not found, skipping constraint")
            continue
            
        if not control_pose_bone:
            print(f"[AetherBlend] Control bone '{control_bone_name}' not found, skipping constraint")
            continue
        
        ffxiv_bone_names.append(ffxiv_bone_name)
        control_bone_names.append(control_bone_name)
        print(f"[AetherBlend] Will add copy rotation constraint: {ffxiv_bone_name} -> {control_bone_name}")
    
    if not ffxiv_bone_names:
        print(f"[AetherBlend] No valid bone pairs found for constraints")
        bpy.ops.object.mode_set(mode='OBJECT')
        return 0
    
    # Remove existing AetherBlend constraints first
    for bone_name in ffxiv_bone_names:
        pose_bone = ffxiv_armature.pose.bones[bone_name]
        constraints_to_remove = [c for c in pose_bone.constraints if c.name.startswith('AetherBlend_Control_')]
        for constraint in constraints_to_remove:
            pose_bone.constraints.remove(constraint)
    
    # Use the utility function to add copy rotation constraints
    add_constraint_copy_rotation(
        bone_names=ffxiv_bone_names,
        armature=ffxiv_armature,
        target_bone_names=control_bone_names
    )
    
    # Rename constraints to follow our naming convention
    for i, ffxiv_bone_name in enumerate(ffxiv_bone_names):
        pose_bone = ffxiv_armature.pose.bones[ffxiv_bone_name]
        control_bone_name = control_bone_names[i]
        
        # Find the constraint that was just added (should be the last Copy Rotation constraint)
        for constraint in reversed(pose_bone.constraints):
            if constraint.type == 'COPY_ROTATION' and not constraint.name.startswith('AetherBlend_'):
                constraint.name = f"AetherBlend_Control_{control_bone_name}"
                break
    
    bpy.ops.object.mode_set(mode='OBJECT')
    constraint_count = len(ffxiv_bone_names)
    print(f"[AetherBlend] Set up {constraint_count} control constraints using utility function")
    return constraint_count

def cleanup_ffxiv_control_constraints(ffxiv_armature):
    """Removes all AetherBlend control constraints from FFXIV bones.
    
    Args:
        ffxiv_armature: The FFXIV armature to clean up
    """
    
    if not ffxiv_armature or ffxiv_armature.type != 'ARMATURE':
        print(f"[AetherBlend] Invalid armature for constraint cleanup")
        return 0
        
    print(f"[AetherBlend] Cleaning up AetherBlend control constraints...")
    
    # Switch to pose mode to remove constraints
    bpy.context.view_layer.objects.active = ffxiv_armature
    bpy.ops.object.mode_set(mode='POSE')
    
    removed_count = 0
    
    # Find all bones with AetherBlend control constraints
    bones_with_constraints = []
    for pose_bone in ffxiv_armature.pose.bones:
        has_aetherblend_constraints = any(c.name.startswith('AetherBlend_Control_') for c in pose_bone.constraints)
        if has_aetherblend_constraints:
            bones_with_constraints.append(pose_bone.name)
    
    if bones_with_constraints:
        print(f"[AetherBlend] Found {len(bones_with_constraints)} bones with AetherBlend constraints")
        
        # Remove AetherBlend constraints manually since the utility function removes ALL copy rotation constraints
        for bone_name in bones_with_constraints:
            pose_bone = ffxiv_armature.pose.bones[bone_name]
            constraints_to_remove = [c for c in pose_bone.constraints if c.name.startswith('AetherBlend_Control_')]
            
            for constraint in constraints_to_remove:
                constraint_name = constraint.name
                pose_bone.constraints.remove(constraint)
                removed_count += 1
                print(f"[AetherBlend] Removed constraint '{constraint_name}' from bone '{pose_bone.name}'")
    else:
        print(f"[AetherBlend] No AetherBlend control constraints found")
    
    bpy.ops.object.mode_set(mode='OBJECT')
    print(f"[AetherBlend] Cleaned up {removed_count} control constraints")
    return removed_count
