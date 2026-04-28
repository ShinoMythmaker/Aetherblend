import bpy

from dataclasses import dataclass
from typing import Callable

from . import rigify
from .operations import ABOperationStack, PoseOperations, PoseOperationsStack
from .shared import Override, RigModule
from .. import utils


@dataclass
class RigGenerationState:
    armature: bpy.types.Object
    meta_rig: bpy.types.Object
    visible_collections: list[bpy.types.BoneCollection]
    operation_stack: ABOperationStack


class AetherRigGenerator:
    """Generates an armature based on ordered module priority groups."""
    name: str
    modules: 'list[list[RigModule]]'
    color_sets: 'dict[str, rigify.ColorSet]'
    overrides: 'list[dict[str, Override]] | None' = None

    def __init__(self, name: str, color_sets: 'list[dict[str, rigify.ColorSet]] | None' = None, overrides: 'list[dict[str, Override]] | None' = None, modules: 'list[list[RigModule]] | None' = None):
        self.name = name
        self.color_sets = color_sets
        self.overrides = overrides

        self.set_modules(modules or [])

    def getOverrides(self) -> dict[str, Override]:
        """Combine all widget overrides into a single dictionary."""
        combined: dict[str, Override] = {}
        for ov_dict in self.overrides or []:
            combined.update(ov_dict)
        return combined

    def set_modules(self, modules: 'list[list[RigModule]]'):
        """Store the already-resolved module priority groups."""
        self.modules = [list(group) for group in modules if group]

    # ------------------------------
    # Meta rig generation pipeline
    # ------------------------------
    def generate_meta_rig(
        self,
        armature: bpy.types.Object,
        cleanup_existing: Callable[[], object] | None = None,
    ) -> RigGenerationState | None:
        """Build and configure a meta rig for this generator."""
        if not self._prepare_source_armature(armature, cleanup_existing):
            return None

        meta_rig = self._create_meta_rig(armature)
        pose_ops_stack, operation_stack = self._build_operation_stacks(meta_rig)

        self._configure_meta_rig(armature, meta_rig)

        generation_data = self._build_generation_data(armature)
        ui_collections = self._run_generator_modules(
            meta_rig,
            generation_data,
            pose_ops_stack,
            operation_stack,
        )

        bones_to_delete = self._collect_ffxiv_bone_updates(meta_rig, pose_ops_stack)
        self._remove_edit_bones(meta_rig, bones_to_delete)

        visible_collections = self._create_ui_collections(meta_rig, ui_collections)
        self._apply_meta_rig_operations(meta_rig, pose_ops_stack, operation_stack)
        self._finalize_meta_rig(armature, meta_rig)

        return RigGenerationState(
            armature=armature,
            meta_rig=meta_rig,
            visible_collections=visible_collections,
            operation_stack=operation_stack,
        )

    # ------------------------------
    # Rigify generation pipeline
    # ------------------------------
    def generate_rigify_rig(self, state: RigGenerationState) -> bool:
        """Run rigify generation and apply post-generation setup."""
        armature = state.armature
        meta_rig = state.meta_rig

        if not meta_rig:
            return False

        if not self._run_rigify_generation(meta_rig):
            return False

        utils.object.select_only(armature)
        self._set_all_collections_visibility(armature, visible=True)
        self._apply_post_generation_operations(armature, state.operation_stack)
        self._update_deform_bones(armature)
        self._apply_widget_overrides(armature)
        self._hide_generated_collections(armature, state.visible_collections)
        self._finalize_generated_rig(armature, meta_rig)
        return True

    def reveal_meta_rig(self, state: RigGenerationState):
        """Show meta rig for manual adjustments and hide the source armature."""
        self._set_meta_rig_visibility(state.meta_rig, visible=True)
        state.armature.hide_set(True)
        state.armature.hide_viewport = True
        utils.object.select_only(state.meta_rig)
        bpy.ops.object.mode_set(mode='POSE')

    # ------------------------------
    # Internal helpers
    # ------------------------------
    def _set_meta_rig_visibility(self, meta_rig: bpy.types.Object, visible: bool):
        utils.object.set_visibility(meta_rig, visible)

    def _prepare_source_armature(
        self,
        armature: bpy.types.Object,
        cleanup_existing: Callable[[], object] | None,
    ) -> bool:
        bpy.ops.object.mode_set(mode='OBJECT')

        armature.hide_set(False)
        utils.object.select_only(armature)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        if cleanup_existing:
            cleanup_existing()

        if armature.aether_rig.rigified:
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

    def _configure_meta_rig(self, armature: bpy.types.Object, meta_rig: bpy.types.Object):
        bpy.context.view_layer.objects.active = meta_rig
        meta_rig.show_in_front = True
        meta_rig.data.rigify_target_rig = armature

        armature_collection = utils.collection.get_collection(armature)
        if armature_collection:
            utils.collection.link_to_collection([meta_rig], armature_collection)

        for color_set in self.color_sets.values():
            color_set.add(meta_rig)

    def _build_generation_data(self, armature: bpy.types.Object) -> dict | None:
        eye_occlusion_objects = utils.object.find_by_armature_and_material_property(
            armature=armature,
            property_name="ShaderPackage",
            property_value="characterocclusion.shpk",
        )

        if not eye_occlusion_objects:
            return None

        return {
            "eye_occlusion": eye_occlusion_objects[0],
            "ffxiv_armature": armature,
        }

    def _run_generator_modules(
        self,
        meta_rig: bpy.types.Object,
        generation_data: dict | None,
        pose_ops_stack: PoseOperationsStack,
        operation_stack: ABOperationStack,
    ) -> rigify.settings.UI_Collections:
        ui_collections = rigify.settings.UI_Collections()

        for module_group in self.modules:
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
        bones_to_delete: list[str] = []
        ffxiv_collection = meta_rig.data.collections.get("FFXIV")
        if not ffxiv_collection:
            return bones_to_delete

        ffxiv_bone_names = {bone.name for bone in ffxiv_collection.bones}
        for bone in meta_rig.data.bones.values():
            if bone.name not in ffxiv_bone_names:
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
        if not bone_names:
            return

        utils.object.select_only(rig_object)
        bpy.ops.object.mode_set(mode='EDIT')
        for bone_name in bone_names:
            bone = rig_object.data.edit_bones.get(bone_name)
            if bone:
                rig_object.data.edit_bones.remove(bone)

    def _create_ui_collections(self, meta_rig: bpy.types.Object, ui_collections: rigify.settings.UI_Collections) -> list[bpy.types.BoneCollection]:
        visible_collections: list[bpy.types.BoneCollection] = []

        for collection in ui_collections.collections:
            collection.create(meta_rig)
            bone_collection, show_collection = collection.create_ui(meta_rig)
            if show_collection and bone_collection:
                visible_collections.append(bone_collection)

        return visible_collections

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
        utils.object.select_only(armature)

    def _set_all_collections_visibility(self, armature: bpy.types.Object, visible: bool):
        for collection in armature.data.collections:
            collection.is_visible = visible

    def _run_rigify_generation(self, meta_rig: bpy.types.Object) -> bool:
        self._set_meta_rig_visibility(meta_rig, visible=True)
        utils.object.select_only(meta_rig)

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
        bpy.ops.object.mode_set(mode='OBJECT')

        ffxiv_bone_names = set(utils.armature.b_collection.get_bones(armature, "FFXIV").keys())
        for bone in armature.data.bones.values():
            bone.use_deform = bone.name in ffxiv_bone_names

    def _apply_widget_overrides(self, armature: bpy.types.Object):
        bpy.ops.object.mode_set(mode='POSE')
        for widget in self.getOverrides().values():
            widget.execute(armature)

    def _hide_generated_collections(self, armature: bpy.types.Object, visible_collections: list[bpy.types.BoneCollection]):
        self._set_all_collections_visibility(armature, visible=False)
        visible_names = {coll.name for coll in visible_collections}
        for collection in armature.data.collections:
            if collection.name in visible_names:
                collection.is_visible = True

    def _finalize_generated_rig(self, armature: bpy.types.Object, meta_rig: bpy.types.Object):
        bpy.ops.object.mode_set(mode='OBJECT')
        armature.aether_rig.rigified = True
        self._set_meta_rig_visibility(meta_rig, visible=False)
        utils.object.select_only(armature)