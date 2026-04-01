import bpy
from bpy.props import StringProperty

from ... import utils
from . import decoder


class AETHER_OT_QuickApplyCustomizePlus(bpy.types.Operator):
    bl_label = "Apply C+ Bone Transforms"
    bl_idname = "aether.q_apply_cplus_string"
    bl_description = (
        "Apply C+ transforms to armature and shapekeys."
    )
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.active_object
        settings = getattr(armature, 'aether_cplus', None)
        cplus_string = settings.code.strip()

        if not armature or armature.type != "ARMATURE":
            self.report({'ERROR'}, "Please select a valid armature.")
            return {'CANCELLED'}

        version, cplus_dict = decoder.translate_hash(cplus_string)
        if not cplus_dict or version not in [4, 5]:
            self.report({'ERROR'}, "Invalid or unsupported C+ string (must be version 4 or 5).")
            return {'CANCELLED'}

        scale_dict = decoder.get_bone_values(cplus_dict, 'Scaling')
        rot_dict = decoder.get_bone_values(cplus_dict, 'Rotation')
        pos_dict = decoder.get_bone_values(cplus_dict, 'Translation')

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = armature
        parent_map = utils.armature.snapshot_parenting(armature)

        utils.armature.unparent_all_bones(armature)

        ffxiv_bones =utils.armature.b_collection.get_pose_bones(armature, "FFXIV")
        
        # Get stored bone orientation from import, or default to standard Y/X
        primary_axis = settings.import_bone_primary_axis if settings.import_bone_primary_axis else 'Y'
        secondary_axis = settings.import_bone_secondary_axis if settings.import_bone_secondary_axis else 'X'
        
        # Step 1 & 2: Revert bone orientation and apply C+ transforms
        decoder.apply_transforms(
            armature, 
            scale_dict, 
            rot_dict, 
            pos_dict, 
            ffxiv_bones,
            primary_axis=primary_axis,
            secondary_axis=secondary_axis,
        )

        utils.armature.apply_all_as_shapekey(armature, shapekey_name="CPlus")

        utils.armature.new_rest_pose(armature)
        
        # Step 3: Reapply bone orientation correction after rest pose is set
        decoder.reapply_bone_orientation(
            armature,
            primary_axis=primary_axis,
            secondary_axis=secondary_axis,
        )

        utils.armature.restore_bone_parenting(armature, parent_map)

        settings.applied = True

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = armature

        self.report({'INFO'}, "C+ transforms applied, shapekeys baked, rest pose set, parenting and modifiers restored.")
        return {'FINISHED'}   

class AETHER_OT_CreateBackupArmature(bpy.types.Operator):
    bl_label = "Create Backup Armature"
    bl_idname = "aether.create_backup_armature"
    bl_description = "Creates a backup armature for C+ reversion."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context) -> set[str]:
        armature = context.active_object
        cplus = getattr(armature, 'aether_cplus', None)
        
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "[AetherBlend] Select a valid armature object.")
            return {'CANCELLED'}

        bone_collections = armature.data.collections
        ffxiv_col = bone_collections.get('FFXIV')
        if not ffxiv_col:
            self.report({'ERROR'}, "[AetherBlend] No FFXIV bone collection found.")
            return {'CANCELLED'}

        # Delete old backup if it exists
        if cplus.backup_armature:
            old_backup = cplus.backup_armature
            old_backup.hide_set(False)
            old_backup.hide_viewport = False

            bpy.data.objects.remove(old_backup, do_unlink=True)
            cplus.backup_armature = None

        # Create backup armature
        backup = utils.armature.duplicate(armature)
        backup.name = f"BACKUP_{armature.name}"
        
        # Parent backup to original armature
        backup.parent = armature
        backup.matrix_parent_inverse = armature.matrix_world.inverted()
                
        # Store reference
        cplus.backup_armature = backup
        
        # Make sure it's in the same collection
        armature_collection = utils.collection.get_collection(armature)
        if armature_collection:
            utils.collection.link_to_collection([backup], armature_collection)

        # Hide backup in viewport
        backup.hide_set(True)
        backup.hide_viewport = True

        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, f"[AetherBlend] Created backup armature '{backup.name}'.")
        return {'FINISHED'}
    
class AETHER_OT_RevertToBackup(bpy.types.Operator):
    bl_label = "Revert to Backup"
    bl_idname = "aether.revert_cplus_to_backup"
    bl_description = (
        "Reverts the armature to the backup armature state."
    )
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.active_object
        cplus = getattr(armature, 'aether_cplus', None)
        
        if not cplus or not cplus.backup_armature:
            self.report({'ERROR'}, "[AetherBlend] No backup armature found. Create a backup first.")
            return {'CANCELLED'}
        
        backup = cplus.backup_armature
        
        # Make backup visible temporarily for data access
        backup.hide_set(False)
        backup.hide_viewport = False
        
        # Get FFXIV bones from both armatures
        ffxiv_col = armature.data.collections.get('FFXIV')
        if not ffxiv_col:
            self.report({'ERROR'}, "[AetherBlend] No FFXIV bone collection found.")
            backup.hide_set(True)
            backup.hide_viewport = True 
            return {'CANCELLED'}
        
        ffxiv_bone_names = [b.name for b in ffxiv_col.bones]
        
        # Copy bone transforms from backup to current armature
        # First, enter edit mode on backup to get bone data
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = backup
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Store backup bone transforms
        bone_data = {}
        for bone_name in ffxiv_bone_names:
            backup_bone = backup.data.edit_bones.get(bone_name)
            if backup_bone:
                bone_data[bone_name] = {
                    'head': backup_bone.head.copy(),
                    'tail': backup_bone.tail.copy(),
                    'roll': backup_bone.roll
                }
        
        # Switch to current armature and apply transforms
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')
        
        for bone_name, data in bone_data.items():
            current_bone = armature.data.edit_bones.get(bone_name)
            if current_bone:
                current_bone.head = data['head']
                current_bone.tail = data['tail']
                current_bone.roll = data['roll']
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Remove CPlus shapekeys from meshes
        meshes = utils.armature.find_meshes(armature)
        for mesh_obj in meshes:
            utils.object.remove_shapekey(mesh_obj, "CPlus", True, "ImportedPose")
        
        # Hide backup again
        backup.hide_set(True)
        backup.hide_viewport = True
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = armature
        
        cplus.applied = False
        self.report({'INFO'}, "Reverted CPlus changes to backup armature state.")
        return {'FINISHED'}
    
class AETHER_OT_ParseFromMCDF(bpy.types.Operator):
    bl_label = "Parse from MCDF file"
    bl_idname = "aether.parse_cplus_from_mcdf"
    bl_description = (
        "Parses the C+ string from an MCDF file."
    )
    bl_options = {'REGISTER', 'UNDO'}

    filepath: StringProperty(subtype="FILE_PATH")  # type: ignore
    filter_glob: StringProperty(default='*.mcdf', options={'HIDDEN'})  # type: ignore

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        context.window.cursor_set('WAIT')

        if not self.filepath or not self.filepath.lower().endswith('.mcdf'): 
            self.report({'ERROR'}, "[AetherBlend] Invalid file format. Please select a .mcdf file.")
            return {'CANCELLED'}

        self.report({'INFO'}, self.filepath)
        context.window.cursor_set('DEFAULT')
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AETHER_OT_QuickApplyCustomizePlus)
    bpy.utils.register_class(AETHER_OT_CreateBackupArmature)
    bpy.utils.register_class(AETHER_OT_RevertToBackup)
    bpy.utils.register_class(AETHER_OT_ParseFromMCDF)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_QuickApplyCustomizePlus)
    bpy.utils.unregister_class(AETHER_OT_CreateBackupArmature)
    bpy.utils.unregister_class(AETHER_OT_RevertToBackup)
    bpy.utils.unregister_class(AETHER_OT_ParseFromMCDF)
