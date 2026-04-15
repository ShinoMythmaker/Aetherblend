import bpy
import time
from dataclasses import dataclass

from ... import utils
from ...core import rigify
from . import template_manager
from ...core.operations import ABOperationStack, PoseOperations, PoseOperationsStack


@dataclass
class _RigGenerationState:
    armature: bpy.types.Object
    meta_rig: bpy.types.Object
    rig_generator: object
    operation_stack: ABOperationStack


class AETHER_OT_Generate_Full_Rig(bpy.types.Operator):
    bl_idname = "aether.generate_full_rig"
    bl_label = "Generate Full Rig"
    bl_description = ("Generate meta rig, rigify rig, and link them in one operation")
    bl_options = {'REGISTER', 'UNDO'}

    def _get_active_armature(self, context) -> bpy.types.Object | None:
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature object")
            return None

        return armature

    def _select_object(self, obj: bpy.types.Object):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

    def _set_meta_rig_visibility(self, meta_rig: bpy.types.Object, visible: bool):
        meta_rig.hide_set(not visible)
        meta_rig.hide_viewport = not visible

    def _prepare_source_armature(self, armature: bpy.types.Object) -> bool:
        bpy.ops.object.mode_set(mode='OBJECT')

        armature.hide_set(False)
        self._select_object(armature)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        bpy.ops.aether.clean_up_rig()

        if armature.aether_rig.rigified:
            self.report({'ERROR'}, "Cannot generate meta rig on an armature that is already rigified.")
            return False

        return True

    def _create_meta_rig(self, armature: bpy.types.Object) -> bpy.types.Object:
        meta_rig = utils.armature.duplicate(armature)
        meta_rig.name = f"META_{armature.name}"

        self._ensure_meta_rig_collections(meta_rig)
        self._join_link_rig(armature, meta_rig)
        return meta_rig

    def _ensure_meta_rig_collections(self, meta_rig: bpy.types.Object):
        linked_coll = meta_rig.data.collections.get("Linked")
        unlinked_coll = meta_rig.data.collections.get("Unlinked")
        ffxiv_coll = meta_rig.data.collections.get("FFXIV")

        if not linked_coll:
            linked_coll = meta_rig.data.collections.new("Linked")
        if not unlinked_coll:
            unlinked_coll = meta_rig.data.collections.new("Unlinked")
        if not ffxiv_coll:
            ffxiv_coll = meta_rig.data.collections.new("FFXIV")

        collections = meta_rig.data.collections
        collections.move(linked_coll.index, 0)
        collections.move(unlinked_coll.index, 1)
        collections.move(ffxiv_coll.index, 2)

    def _build_operation_stacks(self, meta_rig: bpy.types.Object) -> tuple[PoseOperationsStack, ABOperationStack]:
        pose_ops_stack = PoseOperationsStack()
        operation_stack = ABOperationStack()

        for bone in meta_rig.data.bones:
            pose_ops_stack.add(bone.name, PoseOperations(rigify_settings=rigify.types.basic_raw_copy(True)))

        return pose_ops_stack, operation_stack

    def _join_link_rig(self, armature: bpy.types.Object, meta_rig: bpy.types.Object):
        link_rig = utils.armature.duplicate(armature)
        utils.armature.add_bone_prefix(link_rig, "LINK-")

        if link_rig.data.collections.get("FFXIV"):
            link_rig.data.collections.remove(link_rig.data.collections["FFXIV"])

        utils.armature.b_collection.assign_bones(link_rig, list(link_rig.data.bones.keys()), "LINK", clear=True)
        utils.armature.join(src=link_rig, target=meta_rig)

    def _configure_meta_rig(self, armature: bpy.types.Object, meta_rig: bpy.types.Object, rig_generator: object):
        bpy.context.view_layer.objects.active = meta_rig
        meta_rig.show_in_front = True
        meta_rig.data.rigify_target_rig = armature

        armature_collection = utils.collection.get_collection(armature)
        if armature_collection:
            utils.collection.link_to_collection([meta_rig], armature_collection)

        for color_set in rig_generator.color_sets.values():
            color_set.add(meta_rig)

    def _build_generation_data(self, armature: bpy.types.Object) -> dict | None:
        eye_occlusion_object = self._find_objects_with_armature_and_material_property(
            armature=armature,
            property_name="ShaderPackage",
            property_value="characterocclusion.shpk",
        )

        if not eye_occlusion_object:
            return None

        return {
            "eye_occlusion": eye_occlusion_object[0],
            "ffxiv_armature": armature,
        }

    def _run_generator_modules(
        self,
        meta_rig: bpy.types.Object,
        rig_generator: object,
        generation_data: dict | None,
        pose_ops_stack: PoseOperationsStack,
        operation_stack: ABOperationStack,
    ) -> rigify.settings.UI_Collections:
        ui_collections = rigify.settings.UI_Collections()

        for module_group in rig_generator.modules:
            for module in module_group:
                integrity, module_pose_ops, module_ui_collections, module_new_ops = module.execute(meta_rig, generation_data)
                if not integrity:
                    print(f"[AetherBlend] Module '{module.name}' failed integrity check during meta rig generation.")
                    continue

                pose_ops_stack.merge(module_pose_ops)

                if module_ui_collections:
                    ui_collections.add(module_ui_collections)

                if module_new_ops:
                    for operation in module_new_ops:
                        operation_stack.add_operation(operation)

                break

        return ui_collections

    def _collect_ffxiv_bone_updates(self, meta_rig: bpy.types.Object, pose_ops_stack: PoseOperationsStack) -> list[str]:
        bones_to_delete = []
        ffxiv_collection = meta_rig.data.collections.get("FFXIV")
        if not ffxiv_collection:
            return bones_to_delete

        for bone in meta_rig.data.bones.values():
            if bone.name not in ffxiv_collection.bones:
                continue

            if bone.get("ab_linked", False):
                pose_ops_stack.add(bone.name, PoseOperations(b_collection="Linked"))
                continue

            pose_ops_stack.add(bone.name, PoseOperations(b_collection="Unlinked"))
            link_bone = meta_rig.data.bones.get(f"LINK-{bone.name}")
            if link_bone:
                bones_to_delete.append(link_bone.name)

        return bones_to_delete

    def _remove_edit_bones(self, rig_object: bpy.types.Object, bone_names: list[str]):
        bpy.ops.object.mode_set(mode='EDIT')
        for bone_name in bone_names:
            bone = rig_object.data.edit_bones.get(bone_name)
            if bone:
                rig_object.data.edit_bones.remove(bone)

    def _create_ui_collections(self, meta_rig: bpy.types.Object, ui_collections: rigify.settings.UI_Collections) -> list[bpy.types.BoneCollection]:
        hidden_collections = []

        for collection in ui_collections.collections:
            collection.create(meta_rig)
            bone_collection, hide_collection = collection.create_ui(meta_rig)
            if hide_collection and bone_collection:
                hidden_collections.append(bone_collection)

        return hidden_collections

    def _apply_meta_rig_operations(
        self,
        meta_rig: bpy.types.Object,
        pose_ops_stack: PoseOperationsStack,
        operation_stack: ABOperationStack,
    ):
        operation_stack._addPoseOperationStack(pose_ops_stack)
        operation_stack.applyPreEditOperations(meta_rig)
        operation_stack.applyPrePoseOperations(meta_rig)

    def _finalize_meta_rig(self, armature: bpy.types.Object, meta_rig: bpy.types.Object):
        armature.aether_rig.meta_rig = meta_rig

        bpy.ops.object.mode_set(mode='OBJECT')
        meta_rig.parent = armature
        self._set_meta_rig_visibility(meta_rig, visible=False)
        self._select_object(armature)

    def _generate_meta_rig(self, armature: bpy.types.Object) -> _RigGenerationState | None:
        if not self._prepare_source_armature(armature):
            return None

        rig_generator = template_manager.get_rig_generator(armature.aether_rig)
        meta_rig = self._create_meta_rig(armature)
        pose_ops_stack, operation_stack = self._build_operation_stacks(meta_rig)

        self._configure_meta_rig(armature, meta_rig, rig_generator)

        generation_data = self._build_generation_data(armature)
        ui_collections = self._run_generator_modules(
            meta_rig,
            rig_generator,
            generation_data,
            pose_ops_stack,
            operation_stack,
        )

        bones_to_delete = self._collect_ffxiv_bone_updates(meta_rig, pose_ops_stack)
        self._remove_edit_bones(meta_rig, bones_to_delete)

        hidden_collections = self._create_ui_collections(meta_rig, ui_collections)
        self._apply_meta_rig_operations(meta_rig, pose_ops_stack, operation_stack)

        for bone_collection in hidden_collections:
            bone_collection.is_visible = False

        self._finalize_meta_rig(armature, meta_rig)

        return _RigGenerationState(
            armature=armature,
            meta_rig=meta_rig,
            rig_generator=rig_generator,
            operation_stack=operation_stack,
        )

    def _run_rigify_generation(self, meta_rig: bpy.types.Object) -> bool:
        self._set_meta_rig_visibility(meta_rig, visible=True)
        self._select_object(meta_rig)

        if bpy.ops.pose.rigify_generate() == {'FINISHED'}:
            return True

        self._set_meta_rig_visibility(meta_rig, visible=False)
        return False

    def _apply_post_generation_operations(self, armature: bpy.types.Object, operation_stack: ABOperationStack | None):
        if not operation_stack:
            return

        operation_stack.applyPostEditOperations(armature)
        operation_stack.applyPostPoseOperations(armature)

    def _update_deform_bones(self, armature: bpy.types.Object):
        ffxiv_data_bones = utils.armature.b_collection.get_bones(armature, "FFXIV")
        for bone in armature.data.bones.values():
            bone.use_deform = bone in ffxiv_data_bones.values()

    def _apply_widget_overrides(self, armature: bpy.types.Object, rig_generator: object):
        bpy.ops.object.mode_set(mode='POSE')
        for widget in rig_generator.getOverrides().values():
            widget.execute(armature)

    def _hide_generated_collections(self, armature: bpy.types.Object):
        for collection_name in ("FFXIV", "Linked", "Unlinked"):
            bone_collection = armature.data.collections.get(collection_name)
            if bone_collection:
                bone_collection.is_visible = False

    def _finalize_generated_rig(self, armature: bpy.types.Object, meta_rig: bpy.types.Object):
        bpy.ops.object.mode_set(mode='OBJECT')
        armature.aether_rig.rigified = True
        self._set_meta_rig_visibility(meta_rig, visible=False)
        self._select_object(armature)

    def _generate_rigify_rig(self, state: _RigGenerationState) -> bool:
        armature = state.armature
        meta_rig = state.meta_rig
        if not meta_rig:
            self.report({'ERROR'}, "No meta rig found. Generate a meta rig first.")
            return False

        if not self._run_rigify_generation(meta_rig):
            return False

        self._select_object(armature)
        self._apply_post_generation_operations(armature, state.operation_stack)
        self._update_deform_bones(armature)
        self._apply_widget_overrides(armature, state.rig_generator)
        self._hide_generated_collections(armature)
        self._finalize_generated_rig(armature, meta_rig)
        return True

    def _object_uses_armature(self, obj: bpy.types.Object, armature: bpy.types.Object) -> bool:
        for constraint in obj.constraints:
            if hasattr(constraint, 'target') and constraint.target == armature:
                return True

        for modifier in obj.modifiers:
            if modifier.type == 'ARMATURE' and modifier.object == armature:
                return True

        if obj.type != 'ARMATURE' or not obj.pose:
            return False

        for pose_bone in obj.pose.bones:
            for constraint in pose_bone.constraints:
                if hasattr(constraint, 'target') and constraint.target == armature:
                    return True

        return False

    def _object_has_material_property(self, obj: bpy.types.Object, property_name: str, property_value=None) -> bool:
        if not obj.data or not hasattr(obj.data, 'materials'):
            return False

        for material_slot in obj.material_slots:
            material = material_slot.material
            if not material or property_name not in material:
                continue

            if property_value is None or material[property_name] == property_value:
                return True

        return False

    def _find_objects_with_armature_and_material_property(self, armature: bpy.types.Object, property_name: str, property_value=None) -> list[bpy.types.Object]:
        return [
            obj for obj in bpy.data.objects
            if self._object_uses_armature(obj, armature)
            and self._object_has_material_property(obj, property_name, property_value)
        ]

    def execute(self, context):
        time_start = time.time()
        bpy.context.window.cursor_set('WAIT')

        try:
            armature = self._get_active_armature(context)
            if not armature:
                return {'CANCELLED'}

            state = self._generate_meta_rig(armature)
            if not state:
                return {'CANCELLED'}

            if not self._generate_rigify_rig(state):
                return {'CANCELLED'}

            print(f"[AetherBlend] Full rig generation: {time.time() - time_start:.3f}s")
            return {'FINISHED'}
        finally:
            bpy.context.window.cursor_set('DEFAULT')
    
class AETHER_OT_Clean_Up_Rig(bpy.types.Operator):
    bl_idname = "aether.clean_up_rig"
    bl_label = "Remove Rigify Rig"
    bl_description = ("Removes Rigify Control bones while preserving FFXIV animation Data")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        time_start = time.time()
        bpy.context.window.cursor_set('WAIT') 

        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return {'CANCELLED'}
        
        rig_collections = armature.data.collections
        if not rig_collections.get("FFXIV"):
            return {'FINISHED'} # If it doesnt have a FFXIV collection, we can assume its already clean and just exit

        ## Delete Meta Rig and Scripts
        existing_meta_rig = armature.aether_rig.meta_rig
        
        if existing_meta_rig:
            if hasattr(existing_meta_rig.data, 'rigify_rig_ui') and existing_meta_rig.data.rigify_rig_ui:
                script = existing_meta_rig.data.rigify_rig_ui
                if script and script.name in bpy.data.texts:
                    bpy.data.texts.remove(script)
            bpy.data.objects.remove(existing_meta_rig, do_unlink=True)
        
        ## Cleanup Rigify ID
        if "rig_id" in armature.data:
            del armature.data["rig_id"]

        ## Delete Drivers 
        try:
            for fc in armature.data.animation_data.drivers:
                armature.data.driver_remove(fc.data_path, fc.array_index)
        except:
            pass
        
        # Cleanup Bones
        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = armature.data.edit_bones
        for bone in edit_bones:
            delete = True
            for coll in bone.collections:
                if coll.name == "FFXIV":
                    delete = False
                else:
                    coll.unassign(bone)
            if delete:
                edit_bones.remove(bone)

        try:
            bpy.ops.armature.collection_remove_unused()
        except RuntimeError:
            pass

        armature.aether_rig.rigified = False

        for coll in armature.data.collections:
            if coll.name == "FFXIV":
                coll.is_visible = True

        ## Cleanup Rigify Settings and Constrains
        for pose_bone in armature.pose.bones:
            pose_bone.rigify_type = " "
            for constraint in pose_bone.constraints:
                pose_bone.constraints.remove(constraint)

        bpy.ops.object.mode_set(mode='OBJECT')

        print(f"[AetherBlend] Clean Up rig: {time.time() - time_start:.3f}s")
        return {'FINISHED'}
    
class AETHER_OT_Reset_Rig(bpy.types.Operator):
    bl_idname = "aether.reset_rig"
    bl_label = "Reset FFXIV Rig"
    bl_description = ("Resets the armature to its original state (removes animation data)")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return {'CANCELLED'}
        
        result = bpy.ops.aether.clean_up_rig()
        if result != {'FINISHED'}:
            self.report({'ERROR'}, "Clean Up process Failed")
            return {'CANCELLED'}
        
        # Remove all animation data
        if armature.animation_data:
            armature.animation_data_clear()
    
        
        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AETHER_OT_Clean_Up_Rig)
    bpy.utils.register_class(AETHER_OT_Reset_Rig)
    bpy.utils.register_class(AETHER_OT_Generate_Full_Rig)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_Clean_Up_Rig)
    bpy.utils.unregister_class(AETHER_OT_Reset_Rig)
    bpy.utils.unregister_class(AETHER_OT_Generate_Full_Rig)