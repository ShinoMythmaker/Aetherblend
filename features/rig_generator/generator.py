"""The rig generation pipeline: runs rig modules and rigify."""

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import bpy

from ... import utils
from . import instructions, rigify
from .definitions import RigModule
from .instructions import resolve_pending_parents
from .instructions.pose_bone import LINKED_PROPERTY

_ASSET_DIR = Path(__file__).resolve().parents[2] / "assets" / "blend"
_WGTS_FILE = _ASSET_DIR / "wgts.blend"
_WGTS_PREFIX = "AB_WGT_"
_WGTS_COLLECTION_NAME = "WGTS"


@dataclass
class RigGenerationState:
    armature: bpy.types.Object
    meta_rig: bpy.types.Object
    visible_collections: list[bpy.types.BoneCollection]
    modules: list[RigModule]


def enter_mode(rig: bpy.types.Object, mode: str) -> None:
    """Make the rig active and switch it to the given mode."""
    if bpy.context.view_layer.objects.active is not rig:
        bpy.context.view_layer.objects.active = rig
    if rig.mode != mode:
        bpy.ops.object.mode_set(mode=mode)


class AetherRigGenerator:
    """Generates an armature by running the steps of the selected rig modules in order."""

    name: str
    module_groups: list[list[RigModule]]  # instances created from the template's module classes
    color_sets: "dict[str, rigify.ColorSet]"
    ui_layout: list[rigify.BoneCollection]

    def __init__(
        self,
        name: str,
        color_sets: "dict[str, rigify.ColorSet]",
        ui_layout: list[rigify.BoneCollection],
        modules: list[list[type[RigModule]]] | None = None,
    ) -> None:
        self.name = name
        self.color_sets = color_sets
        self.ui_layout = ui_layout
        self.module_groups = [[module_class() for module_class in group] for group in (modules or []) if group]

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
        self._configure_meta_rig(armature, meta_rig)

        original_bone_names = set(meta_rig.data.bones.keys())

        valid_modules = self._validate_modules(available_bones=original_bone_names)
        self._sync_ui_flags_property(armature, valid_modules)

        self._run_meta_edit(meta_rig, valid_modules)

        visible_collections = self._create_ui_collections(meta_rig)

        self._run_meta_pose(meta_rig, valid_modules, original_bone_names)
        self._sort_original_bones(meta_rig)
        self._finalize_meta_rig(armature, meta_rig)

        return RigGenerationState(
            armature=armature,
            meta_rig=meta_rig,
            visible_collections=visible_collections,
            modules=valid_modules,
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
        self._append_widgets(armature)
        self._run_final_steps(armature, state.modules)
        self._update_deform_bones(armature)
        # Rigify can add or reorder collections; keep the curated layout authoritative.
        state.visible_collections = self._create_ui_collections(armature)
        self._hide_generated_collections(armature, state.visible_collections)
        self._finalize_generated_rig(armature, meta_rig)
        return True

    def reveal_meta_rig(self, state: RigGenerationState) -> None:
        """Show meta rig for manual adjustments and hide the source armature."""
        self._set_meta_rig_visibility(state.meta_rig, visible=True)
        state.armature.hide_set(True)
        state.armature.hide_viewport = True
        utils.object.select_only(state.meta_rig)
        bpy.ops.object.mode_set(mode="POSE")

    # ------------------------------
    # Internal helpers
    # ------------------------------
    def _set_meta_rig_visibility(self, meta_rig: bpy.types.Object, visible: bool) -> None:
        utils.object.set_visibility(meta_rig, visible)

    def _prepare_source_armature(
        self,
        armature: bpy.types.Object,
        cleanup_existing: Callable[[], object] | None,
    ) -> bool:
        bpy.ops.object.mode_set(mode="OBJECT")

        utils.armature.reset_transforms(armature)

        armature.hide_set(False)
        utils.object.select_only(armature)

        # Always start generation from a neutral pose state.
        utils.armature.reset_pose_bones(armature)

        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        if cleanup_existing:
            cleanup_existing()

        if armature.aether_rig.rigified:
            return False

        return True

    def _append_widgets(self, armature: bpy.types.Object) -> None:
        """Append widget objects from wgts.blend and place them in the armature's WGTS collection."""

        def _base_object_name(object_name: str) -> str:
            # Blender duplicate suffixes use the pattern ".001", ".002", etc.
            if len(object_name) > 4 and object_name[-4] == "." and object_name[-3:].isdigit():
                return object_name[:-4]
            return object_name

        def _widgets_by_base() -> dict[str, bpy.types.Object]:
            """Return one widget object per base name, preferring non-suffixed names."""
            widgets: dict[str, bpy.types.Object] = {}
            for obj in bpy.data.objects:
                if not obj.name.startswith(_WGTS_PREFIX):
                    continue

                base_name = _base_object_name(obj.name)
                current = widgets.get(base_name)
                if current is None or current.name != base_name:
                    widgets[base_name] = obj
            return widgets

        if not _WGTS_FILE.exists():
            print(f"[AetherBlend] Widget source file not found: {_WGTS_FILE}")
            return

        armature_collection = utils.collection.get_collection(armature)
        if not armature_collection:
            print(f"[AetherBlend] Could not resolve collection for armature '{armature.name}'.")
            return

        wgts_collection = None
        for collection in utils.collection.collection_tree(armature_collection):
            if collection.name.upper().startswith(_WGTS_COLLECTION_NAME):
                wgts_collection = collection
                break

        if not wgts_collection:
            print(
                f"[AetherBlend] No WGTS collection found under armature collection '{armature_collection.name}' "
                f"for armature '{armature.name}'. Skipping widget append."
            )
            return

        with bpy.data.libraries.load(str(_WGTS_FILE), link=False) as (data_from, _):
            widget_names = [name for name in data_from.objects if name and name.startswith(_WGTS_PREFIX)]

        if not widget_names:
            print(f"[AetherBlend] No widget objects found in '{_WGTS_FILE.name}'.")
            return

        widget_base_names = {_base_object_name(name) for name in widget_names}
        existing_widgets = _widgets_by_base()

        missing_widget_names = [name for name in widget_names if _base_object_name(name) not in existing_widgets]

        if missing_widget_names:
            with bpy.data.libraries.load(str(_WGTS_FILE), link=False) as (_, data_to):
                data_to.objects = missing_widget_names

            existing_widgets = _widgets_by_base()

        widgets_to_link = [
            obj
            for base_name, obj in existing_widgets.items()
            if base_name in widget_base_names and all(existing is not obj for existing in wgts_collection.objects)
        ]

        if widgets_to_link:
            utils.collection.link_to_collection(widgets_to_link, wgts_collection)

    def _create_meta_rig(self, armature: bpy.types.Object) -> bpy.types.Object:
        meta_rig = utils.armature.duplicate(armature)
        meta_rig.name = f"META_{armature.name}"

        self._ensure_meta_rig_collections(meta_rig)
        self._join_link_rig(armature, meta_rig)
        return meta_rig

    def _ensure_meta_rig_collections(self, meta_rig: bpy.types.Object) -> None:
        linked_coll = meta_rig.data.collections.get("Linked")
        unlinked_coll = meta_rig.data.collections.get("Unlinked")
        original_coll = meta_rig.data.collections.get("Original")

        if not linked_coll:
            linked_coll = meta_rig.data.collections.new("Linked")
        if not unlinked_coll:
            unlinked_coll = meta_rig.data.collections.new("Unlinked")
        if not original_coll:
            original_coll = meta_rig.data.collections.new("Original")

        collections = meta_rig.data.collections
        collections.move(linked_coll.index, 0)
        collections.move(unlinked_coll.index, 1)
        collections.move(original_coll.index, 2)

    def _join_link_rig(self, armature: bpy.types.Object, meta_rig: bpy.types.Object) -> None:
        link_rig = utils.armature.duplicate(armature)
        utils.armature.add_bone_prefix(link_rig, "LINK-")

        if link_rig.data.collections.get("Original"):
            link_rig.data.collections.remove(link_rig.data.collections["Original"])

        utils.armature.b_collection.assign_bones(link_rig, list(link_rig.data.bones.keys()), "LINK", clear=True)
        utils.armature.join(src=link_rig, target=meta_rig)

    def _configure_meta_rig(self, armature: bpy.types.Object, meta_rig: bpy.types.Object) -> None:
        bpy.context.view_layer.objects.active = meta_rig
        meta_rig.show_in_front = True
        meta_rig.data.rigify_target_rig = armature

        armature_collection = utils.collection.get_collection(armature)
        if armature_collection:
            utils.collection.link_to_collection([meta_rig], armature_collection)

        for color_set in self.color_sets.values():
            color_set.add(meta_rig)

    def _validate_modules(self, available_bones: set[str]) -> list[RigModule]:
        """Pick the first module of every priority group whose required bones all exist."""
        valid: list[RigModule] = []

        for module_group in self.module_groups:
            for module in module_group:
                missing_bones = module.missing_bones(available_bones)
                if missing_bones:
                    print(f"[AetherBlend] Skipping module '{module.name}': missing bones {missing_bones}")
                    continue

                valid.append(module)
                break

        return valid

    def _run_meta_edit(self, meta_rig: bpy.types.Object, modules: list[RigModule]) -> None:
        enter_mode(meta_rig, "EDIT")
        for module in modules:
            module.meta_edit(meta_rig)
        resolve_pending_parents(meta_rig)

    def _sort_original_bones(self, meta_rig: bpy.types.Object) -> None:
        """Move original bones into Linked or Unlinked and drop the LINK bones that nothing uses."""
        enter_mode(meta_rig, "OBJECT")
        original_collection = meta_rig.data.collections.get("Original")
        if not original_collection:
            return

        original_bone_names = [bone.name for bone in original_collection.bones]
        linked_bones = [name for name in original_bone_names if self._is_linked(meta_rig, name)]
        unlinked_bones = [name for name in original_bone_names if name not in linked_bones]

        enter_mode(meta_rig, "EDIT")
        for bone_name in unlinked_bones:
            link_bone = meta_rig.data.edit_bones.get(f"LINK-{bone_name}")
            if link_bone:
                meta_rig.data.edit_bones.remove(link_bone)

        enter_mode(meta_rig, "OBJECT")
        utils.armature.b_collection.assign_bones(meta_rig, linked_bones, "Linked")
        utils.armature.b_collection.assign_bones(meta_rig, unlinked_bones, "Unlinked")

    @staticmethod
    def _is_linked(meta_rig: bpy.types.Object, bone_name: str) -> bool:
        link_pose_bone = meta_rig.pose.bones.get(f"LINK-{bone_name}")
        return bool(link_pose_bone and link_pose_bone.get(LINKED_PROPERTY))

    def _run_meta_pose(
        self, meta_rig: bpy.types.Object, modules: list[RigModule], original_bone_names: set[str]
    ) -> None:
        enter_mode(meta_rig, "POSE")
        for bone_name in original_bone_names:
            if bone_name in meta_rig.pose.bones:
                instructions.rigify.basic_raw_copy(meta_rig, bone_name, relink_constraints=True)

        for module in modules:
            module.meta_pose(meta_rig)

    def _run_final_steps(self, armature: bpy.types.Object, modules: list[RigModule]) -> None:
        enter_mode(armature, "EDIT")
        for module in modules:
            module.final_edit(armature)
        resolve_pending_parents(armature)

        enter_mode(armature, "POSE")
        instructions.widget(armature, "root", scale_factor=0.2)
        for module in modules:
            module.final_pose(armature)

    def _sync_ui_flags_property(self, armature: bpy.types.Object, modules: list[RigModule]) -> None:
        flags = {flag for module in modules for flag in module.ui_flags}
        armature.aether_rig.ui_flags.clear()
        for flag in sorted(flags):
            item = armature.aether_rig.ui_flags.add()
            item.value = flag

    def _create_ui_collections(self, meta_rig: bpy.types.Object) -> list[bpy.types.BoneCollection]:
        """Apply the curated layout in order, including collections without bones."""
        visible_collections: list[bpy.types.BoneCollection] = []

        for collection in meta_rig.data.collections_all:
            collection.rigify_ui_row = 0

        for index, collection in enumerate(self.ui_layout):
            collection.create(meta_rig)
            bone_collection, show_collection = collection.create_ui(meta_rig)
            if bone_collection:
                bone_collection.parent = None
                meta_rig.data.collections.move(meta_rig.data.collections.find(bone_collection.name), index)
                if show_collection:
                    visible_collections.append(bone_collection)

        return visible_collections

    def _finalize_meta_rig(self, armature: bpy.types.Object, meta_rig: bpy.types.Object) -> None:
        armature.aether_rig.meta_rig = meta_rig

        bpy.ops.object.mode_set(mode="OBJECT")
        meta_rig.parent = armature
        self._set_meta_rig_visibility(meta_rig, visible=False)
        utils.object.select_only(armature)

    def _set_all_collections_visibility(self, armature: bpy.types.Object, visible: bool) -> None:
        for collection in armature.data.collections:
            collection.is_visible = visible

    def _run_rigify_generation(self, meta_rig: bpy.types.Object) -> bool:
        self._set_meta_rig_visibility(meta_rig, visible=True)
        utils.object.select_only(meta_rig)

        if bpy.ops.pose.rigify_generate() == {"FINISHED"}:
            return True

        self._set_meta_rig_visibility(meta_rig, visible=False)
        return False

    def _update_deform_bones(self, armature: bpy.types.Object) -> None:
        bpy.ops.object.mode_set(mode="OBJECT")

        original_bone_names = set(utils.armature.b_collection.get_bones(armature, "Original").keys())
        for bone in armature.data.bones.values():
            bone.use_deform = bone.name in original_bone_names

    def _hide_generated_collections(
        self, armature: bpy.types.Object, visible_collections: list[bpy.types.BoneCollection]
    ) -> None:
        self._set_all_collections_visibility(armature, visible=False)
        visible_names = {coll.name for coll in visible_collections}
        for collection in armature.data.collections:
            if collection.name in visible_names:
                collection.is_visible = True

    def _finalize_generated_rig(self, armature: bpy.types.Object, meta_rig: bpy.types.Object) -> None:
        bpy.ops.object.mode_set(mode="OBJECT")
        armature.aether_rig.rigified = True
        self._set_meta_rig_visibility(meta_rig, visible=False)
        utils.object.select_only(armature)
