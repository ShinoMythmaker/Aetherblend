import bpy
from ...utils import rig as rig_utils
from ...utils.rig.meta_rig import create_limb_arm, create_meta_rig_collections, setup_rigify_standard_colors, setup_rigify_color_sets, assign_color_sets_to_collections, setup_meta_rig_viewport_display, setup_meta_rig_collection_ui, get_ffxiv_to_control_bone_mapping, setup_ffxiv_control_constraints, cleanup_ffxiv_control_constraints
from ...utils.rig.bone import bones_exist, collection_exists, delete_bone_collection_and_bones
from ...data.constants import (
    meta_rig_arm_l_bones, meta_rig_arm_r_bones,
    meta_rig_leg_l_bones, meta_rig_leg_r_bones,
    meta_rig_arm_l_names, meta_rig_arm_r_names,
    meta_rig_prefix, meta_rig_collection
)

class AETHER_OT_Generate_Meta_Rig(bpy.types.Operator):
    """Generate a meta rig based on available bones"""
    bl_idname = "aether.generate_meta_rig"
    bl_label = "Generate Meta Rig"
    bl_options = {'REGISTER', 'UNDO'}

    include_arm_l: bpy.props.BoolProperty(name="Arm L", default=False) # type: ignore
    include_arm_r: bpy.props.BoolProperty(name="Arm R", default=False) # type: ignore

    def invoke(self, context, event):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature object")
            return {'CANCELLED'}

        # Check if we're regenerating an existing meta rig
        existing_meta_rig = armature.aether_meta_rig
        
        if existing_meta_rig:
            # For regeneration, check what limbs currently exist in the meta rig
            meta_bones = existing_meta_rig.data.bones
            self.include_arm_l = any(bone_name in meta_bones for bone_name in meta_rig_arm_l_names)
            self.include_arm_r = any(bone_name in meta_bones for bone_name in meta_rig_arm_r_names)
            print(f"[AetherBlend] Regenerating meta rig - detected existing limbs: Arm.L={self.include_arm_l}, Arm.R={self.include_arm_r}")
        else:
            # For new generation, check which bone sets are available in source armature using utility function
            self.include_arm_l = bones_exist(armature, meta_rig_arm_l_bones)
            self.include_arm_r = bones_exist(armature, meta_rig_arm_r_bones)
            print(f"[AetherBlend] Creating new meta rig - available limbs: Arm.L={self.include_arm_l}, Arm.R={self.include_arm_r}")

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        armature = context.active_object
        existing_meta_rig = armature.aether_meta_rig if armature else None
        
        if existing_meta_rig:
            layout.label(text="Regenerate Meta Rig:", icon="FILE_REFRESH")
            layout.label(text=f"Updating: {existing_meta_rig.name}")
        else:
            layout.label(text="Generate New Meta Rig:", icon="ARMATURE_DATA")
            
        layout.separator()
        layout.label(text="Select limbs to include:")
        layout.prop(self, "include_arm_l")
        layout.prop(self, "include_arm_r")

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature object")
            return {'CANCELLED'}

        # Store original mode and switch to Object mode for reliable operations
        original_mode = bpy.context.object.mode if bpy.context.object else 'OBJECT'
        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            print(f"[AetherBlend] Switched from {original_mode} to Object mode for meta rig generation")

        try:
            # Store FFXIV rig visibility state and ensure it's visible for operations
            ffxiv_was_hidden = armature.hide_get()
            if ffxiv_was_hidden:
                armature.hide_set(False)
                print(f"[AetherBlend] Temporarily showing FFXIV rig for meta rig creation")

            # Check if meta rig already exists
            existing_meta_rig = armature.aether_meta_rig
            is_regeneration = bool(existing_meta_rig)
            
            if is_regeneration:
                # Step 1: Use existing meta rig and clear its bones
                meta_rig = existing_meta_rig
                self.clear_meta_rig_bones(meta_rig)
                action_text = "regenerated"
            else:
                # Step 1: Create and setup the meta rig armature
                meta_rig = self.setup_meta_rig_armature(context, armature)
                if not meta_rig:
                    return {'CANCELLED'}
                action_text = "generated"

                # Step 2: Create bone collections for rigify (only for new meta rigs)
                self.setup_meta_rig_collections(meta_rig)

                # Step 3: Setup general armature properties for rigify (only for new meta rigs)
                self.setup_meta_rig_properties(meta_rig)

            # Step 4: Generate individual limbs (always done)
            created_limbs = self.generate_limbs(armature, meta_rig)
                    
            # Step 5: Store reference and setup parenting/visibility (only for new meta rigs)
            if not is_regeneration:
                armature.aether_meta_rig = meta_rig
                
                # Parent meta rig to FFXIV rig and hide it
                meta_rig.parent = armature
                meta_rig.hide_set(True)
                print(f"[AetherBlend] Parented meta rig to FFXIV rig and hid it")

            # Reselect the original FFXIV rig to keep the panel visible
            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.select_all(action='DESELECT')
            armature.select_set(True)
            
            # Restore FFXIV rig visibility state
            if ffxiv_was_hidden:
                armature.hide_set(True)
                print(f"[AetherBlend] Restored FFXIV rig hidden state")

            limb_count = len([x for x in [self.include_arm_l, self.include_arm_r] if x])
            self.report({'INFO'}, f"Meta rig '{meta_rig.name}' {action_text} with {limb_count} limbs ({len(created_limbs)} bones)")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Error during meta rig generation: {str(e)}")
            return {'CANCELLED'}
        finally:
            # Restore original mode
            if original_mode != 'OBJECT':
                try:
                    bpy.ops.object.mode_set(mode=original_mode)
                    print(f"[AetherBlend] Restored {original_mode} mode")
                except:
                    print(f"[AetherBlend] Could not restore {original_mode} mode, staying in Object mode")

    def setup_meta_rig_armature(self, context, source_armature):
        """Create the base meta rig armature."""
        bpy.ops.object.armature_add(enter_editmode=False, location=(0, 0, 0))
        meta_rig = context.active_object
        meta_rig.name = f"{meta_rig_prefix}{source_armature.name}"

        # Remove default bone
        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = meta_rig.data.edit_bones
        if "Bone" in edit_bones:
            edit_bones.remove(edit_bones["Bone"])
        bpy.ops.object.mode_set(mode='OBJECT')

        return meta_rig

    def clear_meta_rig_bones(self, meta_rig):
        """Clear all bones from an existing meta rig while preserving collections and properties."""
        if not meta_rig or meta_rig.type != 'ARMATURE':
            print(f"[AetherBlend] Cannot clear bones - invalid meta rig object")
            return False
            
        print(f"[AetherBlend] Clearing bones from existing meta rig '{meta_rig.name}'")
        
        # Make sure the meta rig is active and switch to edit mode
        bpy.context.view_layer.objects.active = meta_rig
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Get all edit bones and remove them
        edit_bones = meta_rig.data.edit_bones
        bones_to_remove = list(edit_bones)  # Create a copy of the list
        
        for bone in bones_to_remove:
            edit_bones.remove(bone)
            
        print(f"[AetherBlend] Cleared {len(bones_to_remove)} bones from meta rig")
        
        bpy.ops.object.mode_set(mode='OBJECT')
        return True

    def setup_meta_rig_collections(self, meta_rig):
        """Create bone collections needed for rigify."""
        create_meta_rig_collections(meta_rig)

    def setup_meta_rig_properties(self, meta_rig):
        """Setup general armature properties for rigify meta rig."""
        print(f"[AetherBlend] Setting up general meta rig properties for '{meta_rig.name}'")
        
        # Set up viewport display (in front, stick display, names)
        setup_meta_rig_viewport_display(meta_rig)
        
        # Set up standard rigify colors
        setup_rigify_standard_colors(meta_rig)
        
        # Set up rigify color sets
        setup_rigify_color_sets(meta_rig)
        
        # Set up collection UI layout
        setup_meta_rig_collection_ui(meta_rig)
        
        # TODO: Add any other general meta rig armature properties here
        # For example, rigify generation settings, etc.

    def generate_limbs(self, source_armature, meta_rig):
        """Generate the individual limbs based on user selection."""
        created_limbs = []
        
        if self.include_arm_l:
            bones = create_limb_arm(source_armature, meta_rig, side="L", prefix="")
            if bones:
                created_limbs.extend(bones)
                
        if self.include_arm_r:
            bones = create_limb_arm(source_armature, meta_rig, side="R", prefix="")
            if bones:
                created_limbs.extend(bones)

        return created_limbs


class AETHER_OT_Generate_Control_Rig(bpy.types.Operator):
    """Generate a control rig from the meta rig using Rigify"""
    bl_idname = "aether.generate_control_rig"
    bl_label = "Generate Control Rig"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature object")
            return {'CANCELLED'}

        # Store original mode and switch to Object mode for reliable operations
        original_mode = bpy.context.object.mode if bpy.context.object else 'OBJECT'
        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            print(f"[AetherBlend] Switched from {original_mode} to Object mode for control rig generation")

        try:
            if not armature.aether_meta_rig:
                self.report({'ERROR'}, "No meta rig found. Generate a meta rig first.")
                return {'CANCELLED'}

            meta_rig = armature.aether_meta_rig
            
            # Store meta rig visibility state and ensure it's visible for operations
            meta_rig_was_hidden = meta_rig.hide_get()
            if meta_rig_was_hidden:
                meta_rig.hide_set(False)
                print(f"[AetherBlend] Temporarily showing meta rig for control rig generation")
            
            # Check if meta rig is valid for rigify generation
            if not self.validate_meta_rig_for_rigify(meta_rig):
                # Restore meta rig visibility before returning
                if meta_rig_was_hidden:
                    meta_rig.hide_set(True)
                return {'CANCELLED'}

            # Select the meta rig and make it active
            bpy.context.view_layer.objects.active = meta_rig
            bpy.ops.object.select_all(action='DESELECT')
            meta_rig.select_set(True)
            bpy.ops.object.mode_set(mode='POSE')

            # Check if a target rig already exists (for regeneration)
            existing_rig = getattr(meta_rig.data, 'rigify_target_rig', None)
            action_text = "regenerated" if existing_rig else "generated"
            
            # Use rigify's generate operator
            result = bpy.ops.pose.rigify_generate()
            
            if result == {'FINISHED'}:
                # Get the generated/regenerated control rig
                control_rig = getattr(meta_rig.data, 'rigify_target_rig', None)
                
                if control_rig:
                    # Store reference to control rig in original FFXIV armature
                    armature.aether_control_rig = control_rig
                    
                    # Parent control rig to FFXIV rig and hide it
                    control_rig.parent = armature
                    control_rig.hide_set(True)
                    print(f"[AetherBlend] Parented control rig to FFXIV rig and hid it")
                    
                    # Reselect the original FFXIV rig to keep the panel visible
                    bpy.context.view_layer.objects.active = armature
                    bpy.ops.object.select_all(action='DESELECT')
                    armature.select_set(True)
                    
                    # Restore meta rig visibility state
                    if meta_rig_was_hidden:
                        meta_rig.hide_set(True)
                        print(f"[AetherBlend] Restored meta rig hidden state")
                    
                    self.report({'INFO'}, f"Control rig '{control_rig.name}' {action_text} successfully")
                    return {'FINISHED'}
                else:
                    # Restore meta rig visibility before returning error
                    if meta_rig_was_hidden:
                        meta_rig.hide_set(True)
                    self.report({'ERROR'}, "Failed to get reference to generated control rig")
                    return {'CANCELLED'}
            else:
                # Restore meta rig visibility before returning error
                if meta_rig_was_hidden:
                    meta_rig.hide_set(True)
                self.report({'ERROR'}, "Rigify generation failed")
                return {'CANCELLED'}
                
        except Exception as e:
            # Restore meta rig visibility before returning error
            if 'meta_rig_was_hidden' in locals() and meta_rig_was_hidden:
                meta_rig.hide_set(True)
            self.report({'ERROR'}, f"Error during rigify generation: {str(e)}")
            return {'CANCELLED'}
        finally:
            # Ensure we're back in object mode and original armature is selected
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.select_all(action='DESELECT')
            armature.select_set(True)
            
            # Restore original mode
            if original_mode != 'OBJECT':
                try:
                    bpy.ops.object.mode_set(mode=original_mode)
                    print(f"[AetherBlend] Restored {original_mode} mode")
                except:
                    print(f"[AetherBlend] Could not restore {original_mode} mode, staying in Object mode")

    def validate_meta_rig_for_rigify(self, meta_rig):
        """Validates that the meta rig is properly set up for rigify generation."""
        
        if not meta_rig or meta_rig.type != 'ARMATURE':
            self.report({'ERROR'}, "Meta rig is not a valid armature")
            return False
            
        # Check if meta rig has any pose bones with rigify types
        rigify_bones = [bone for bone in meta_rig.pose.bones if bone.rigify_type != ""]
        
        if not rigify_bones:
            self.report({'ERROR'}, "Meta rig has no bones with rigify types assigned")
            return False
            
        # Check if meta rig has collections with UI rows assigned
        ui_collections = [coll for coll in meta_rig.data.collections_all if coll.rigify_ui_row > 0]
        
        if not ui_collections:
            self.report({'ERROR'}, "Meta rig has no bone collections assigned to UI rows")
            return False
            
        print(f"[AetherBlend] Meta rig validation passed: {len(rigify_bones)} rigify bones, {len(ui_collections)} UI collections")
        return True
    


class AETHER_OT_Link_Control_Rig(bpy.types.Operator):
    """Link the control rig to the FFXIV rig by merging control bones"""
    bl_idname = "aether.link_control_rig"
    bl_label = "Link Control Rig"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature object")
            return {'CANCELLED'}

        # Store original mode and switch to Object mode for reliable operations
        original_mode = bpy.context.object.mode if bpy.context.object else 'OBJECT'
        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            print(f"[AetherBlend] Switched from {original_mode} to Object mode for control rig linking")

        try:
            if not armature.aether_control_rig:
                self.report({'ERROR'}, "No control rig found. Generate a control rig first.")
                return {'CANCELLED'}

            control_rig = armature.aether_control_rig
            
            # Store control rig visibility state and ensure it's visible for operations
            control_rig_was_hidden = control_rig.hide_get()
            if control_rig_was_hidden:
                control_rig.hide_set(False)
                print(f"[AetherBlend] Temporarily showing control rig for linking")

            # Check if already linked and clean up old control bones if needed
            if getattr(armature, 'aether_control_linked', False):
                print(f"[AetherBlend] Control rig already linked, cleaning up old control bones...")
                self.cleanup_old_control_bones(armature)

            # Merge control rig bones into FFXIV rig
            success = self.merge_control_rig_bones(armature, control_rig)
            
            if success:
                # Mark as linked
                armature.aether_control_linked = True
                
                # Restore control rig visibility state
                if control_rig_was_hidden:
                    control_rig.hide_set(True)
                    print(f"[AetherBlend] Restored control rig hidden state")
                
                self.report({'INFO'}, f"Control rig merged into {armature.name}")
                return {'FINISHED'}
            else:
                # Restore control rig visibility before returning error
                if control_rig_was_hidden:
                    control_rig.hide_set(True)
                self.report({'ERROR'}, "Failed to merge control rig")
                return {'CANCELLED'}
                
        except Exception as e:
            # Restore control rig visibility before returning error
            if 'control_rig_was_hidden' in locals() and control_rig_was_hidden:
                control_rig.hide_set(True)
            self.report({'ERROR'}, f"Error during control rig linking: {str(e)}")
            return {'CANCELLED'}
        finally:
            # Restore original mode
            if original_mode != 'OBJECT':
                try:
                    bpy.ops.object.mode_set(mode=original_mode)
                    print(f"[AetherBlend] Restored {original_mode} mode")
                except:
                    print(f"[AetherBlend] Could not restore {original_mode} mode, staying in Object mode")

    def cleanup_old_control_bones(self, ffxiv_armature):
        """Remove old control rig bones and data from FFXIV armature before linking new ones."""
        
        print(f"[AetherBlend] Cleaning up old control rig from '{ffxiv_armature.name}'")
        
        # First, clean up old constraints
        cleanup_ffxiv_control_constraints(ffxiv_armature)
        
        # Get all control rig collections from the reference control rig
        control_rig = ffxiv_armature.aether_control_rig
        if not control_rig:
            print(f"[AetherBlend] No control rig reference found for cleanup")
            return
        
        # Get list of all collection names from the control rig
        control_collection_names = [coll.name for coll in control_rig.data.collections_all]
        
        # Delete each control collection and all its bones from FFXIV armature
        collections_removed = 0
        for collection_name in control_collection_names:
            if collection_exists(ffxiv_armature, collection_name):
                delete_bone_collection_and_bones(ffxiv_armature, collection_name)
                collections_removed += 1
        
        print(f"[AetherBlend] Cleaned up {collections_removed} control collections and their bones")

    def merge_control_rig_bones(self, ffxiv_armature, control_rig):
        """Duplicate the control rig and merge it with the FFXIV armature."""
        
        print(f"[AetherBlend] Duplicating and merging control rig '{control_rig.name}' with FFXIV rig '{ffxiv_armature.name}'")
        
        # Step 1: Duplicate the control rig
        bpy.ops.object.select_all(action='DESELECT')
        control_rig.select_set(True)
        bpy.context.view_layer.objects.active = control_rig
        bpy.ops.object.duplicate()
        
        # Get the duplicated control rig
        duplicated_control_rig = bpy.context.active_object
        duplicated_control_rig.name = f"{control_rig.name}_temp_duplicate"
        
        print(f"[AetherBlend] Created duplicate: '{duplicated_control_rig.name}'")
        
        # Step 2: Join the duplicated control rig with the FFXIV rig
        bpy.ops.object.select_all(action='DESELECT')
        ffxiv_armature.select_set(True)
        duplicated_control_rig.select_set(True)
        bpy.context.view_layer.objects.active = ffxiv_armature  # Target armature must be active
        
        # Join them - this preserves all collections, constraints, custom shapes automatically
        bpy.ops.object.join()
        
        print(f"[AetherBlend] Joined control rig into FFXIV armature")
        
        # Step 3: Add the rig_id custom property that rigify needs
        success = self.copy_rigify_properties(ffxiv_armature, control_rig)
        
        if not success:
            print(f"[AetherBlend] Warning: Failed to copy rigify properties")
        
        # Step 4: Setup constraints from FFXIV bones to control bones
        constraint_count = self.setup_control_constraints(ffxiv_armature, control_rig)
        
        print(f"[AetherBlend] Merge completed: Control rig duplicated and joined, {constraint_count} constraints added")
        return True

    def copy_rigify_properties(self, ffxiv_armature, control_rig):
        """Copy essential rigify properties like rig_id that are needed for the UI."""
        
        print(f"[AetherBlend] Copying rigify properties...")
        
        try:
            # Copy the rig_id custom property from armature data (not object)
            if "rig_id" in control_rig.data:
                ffxiv_armature.data["rig_id"] = control_rig.data["rig_id"]
                print(f"[AetherBlend] Copied rig_id from armature data: {control_rig.data['rig_id']}")
            else:
                print(f"[AetherBlend] No rig_id found in control rig armature data")
            
            # Copy any other essential rigify properties from armature data
            rigify_properties = ["rigify_colors", "rigify_selection_colors"]
            for prop_name in rigify_properties:
                if prop_name in control_rig.data:
                    ffxiv_armature.data[prop_name] = control_rig.data[prop_name]
                    print(f"[AetherBlend] Copied rigify property from armature data: {prop_name}")
            
            return True
            
        except Exception as e:
            print(f"[AetherBlend] Error copying rigify properties: {e}")
            return False

    def setup_control_constraints(self, ffxiv_armature, control_rig):
        """Setup constraints from FFXIV bones to corresponding control bones (using original names)."""
        
        print(f"[AetherBlend] Setting up constraints from FFXIV bones to control bones...")
        
        # Get the bone mapping (now using original control bone names)
        bone_mapping = get_ffxiv_to_control_bone_mapping()
        
        # Setup constraints using our helper function
        constraint_count = setup_ffxiv_control_constraints(ffxiv_armature, bone_mapping)
        
        return constraint_count


class AETHER_OT_Unlink_Control_Rig(bpy.types.Operator):
    """Unlink the control rig from the FFXIV rig by removing control bones and constraints"""
    bl_idname = "aether.unlink_control_rig"
    bl_label = "Unlink Control Rig"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature object")
            return {'CANCELLED'}

        # Store original mode and switch to Object mode for reliable operations
        original_mode = bpy.context.object.mode if bpy.context.object else 'OBJECT'
        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            print(f"[AetherBlend] Switched from {original_mode} to Object mode for control rig unlinking")

        try:
            if not getattr(armature, 'aether_control_linked', False):
                self.report({'ERROR'}, "No control rig is currently linked.")
                return {'CANCELLED'}

            # Clean up control bones and constraints
            self.cleanup_control_bones_and_constraints(armature)
            
            # Remove rig_id from armature data
            if "rig_id" in armature.data:
                del armature.data["rig_id"]
                print(f"[AetherBlend] Removed rig_id from armature data")
            
            # Mark as unlinked
            armature.aether_control_linked = False
            
            self.report({'INFO'}, f"Control rig unlinked from {armature.name}")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Error during control rig unlinking: {str(e)}")
            return {'CANCELLED'}
        finally:
            # Restore original mode
            if original_mode != 'OBJECT':
                try:
                    bpy.ops.object.mode_set(mode=original_mode)
                    print(f"[AetherBlend] Restored {original_mode} mode")
                except:
                    print(f"[AetherBlend] Could not restore {original_mode} mode, staying in Object mode")

    def cleanup_control_bones_and_constraints(self, ffxiv_armature):
        """Remove all control bones and constraints from FFXIV armature using collection-based cleanup."""
        
        print(f"[AetherBlend] Unlinking control rig from '{ffxiv_armature.name}'")
        
        # Clean up constraints first
        constraint_count = cleanup_ffxiv_control_constraints(ffxiv_armature)
        
        # Get control rig reference to identify collections to remove
        control_rig = ffxiv_armature.aether_control_rig
        if not control_rig:
            print(f"[AetherBlend] No control rig reference found for cleanup")
            return
        
        # Get list of all collection names from the control rig
        control_collection_names = [coll.name for coll in control_rig.data.collections_all]
        
        # Delete each control collection and all its bones from FFXIV armature
        collections_removed = 0
        for collection_name in control_collection_names:
            if collection_exists(ffxiv_armature, collection_name):
                delete_bone_collection_and_bones(ffxiv_armature, collection_name)
                collections_removed += 1
        
        print(f"[AetherBlend] Unlink completed: removed {collections_removed} control collections and their bones, {constraint_count} constraints")


def register():
    bpy.utils.register_class(AETHER_OT_Generate_Meta_Rig)
    bpy.utils.register_class(AETHER_OT_Generate_Control_Rig)
    bpy.utils.register_class(AETHER_OT_Link_Control_Rig)
    bpy.utils.register_class(AETHER_OT_Unlink_Control_Rig)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_Generate_Meta_Rig)
    bpy.utils.unregister_class(AETHER_OT_Generate_Control_Rig)
    bpy.utils.unregister_class(AETHER_OT_Link_Control_Rig)
    bpy.utils.unregister_class(AETHER_OT_Unlink_Control_Rig)