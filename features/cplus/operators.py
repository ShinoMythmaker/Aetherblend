"""Operators for applying and managing Customize+ armature data."""

import base64
import binascii
import json
import zlib
from io import BytesIO

import bpy
from bpy.props import StringProperty
from mathutils import Vector

from ... import utils
from ...preferences import get_preferences
from . import decoder


class AETHER_OT_QuickApplyCustomizePlus(bpy.types.Operator):
    """Apply a Customize+ string to an armature."""

    bl_label = "Apply C+ Bone Transforms"
    bl_idname = "aether.q_apply_cplus_string"
    bl_description = "Apply C+ transforms to the armature and bake them to a shapekey."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        """Decode and apply the active armature's Customize+ data."""
        armature = context.active_object
        if armature is None or armature.type != "ARMATURE":
            self.report({"ERROR"}, "Please select a valid armature.")
            return {"CANCELLED"}

        settings = getattr(armature, "aether_cplus", None)
        if not settings or not settings.code.strip():
            self.report({"ERROR"}, "Enter a Customize+ string before applying it.")
            return {"CANCELLED"}
        if armature.data.collections.get("Original") is None:
            self.report({"ERROR"}, "The armature is missing its Original bone collection.")
            return {"CANCELLED"}

        try:
            decoded = base64.b64decode(settings.code.strip(), validate=True)
            with BytesIO(decoded) as reader:
                signature = decoder.read_int(reader)

            if signature == 0x88B1F:
                version, cplus_data = decoder.translate_hash(decoded)
                # Im Tired of upping the version
                # if version not in {4, 5, 6}:
                #     raise ValueError(f"Unsupported C+ version: {version}")
            else:
                cplus_data = json.loads(decoded)
            if not isinstance(cplus_data, dict) or not isinstance(cplus_data.get("Bones"), dict):
                raise ValueError("The C+ data does not contain a Bones object")
            scales = decoder.get_bone_values(cplus_data, "Scaling")
            rotations = decoder.get_bone_values(cplus_data, "Rotation")
            translations = decoder.get_bone_values(cplus_data, "Translation")
        except (
            binascii.Error,
            UnicodeDecodeError,
            json.JSONDecodeError,
            ValueError,
            OSError,
            zlib.error,
            TypeError,
            AttributeError,
        ) as exc:
            self.report({"ERROR"}, f"Invalid or unsupported C+ string: {exc}")
            return {"CANCELLED"}

        original_bones = utils.armature.b_collection.get_pose_bones(armature, "Original")
        if not original_bones:
            self.report({"ERROR"}, "The Original bone collection contains no bones.")
            return {"CANCELLED"}
        primary_axis = settings.cplus_primary_axis
        secondary_axis = settings.cplus_secondary_axis

        utils.object.select_only(armature)
        utils.armature.reset_pose_bones(armature)
        parent_map = utils.armature.snapshot_parenting(armature)
        axes_reverted = False
        try:
            utils.armature.unparent_all_bones(armature)
            utils.axis_conversion.revert_bone_axis_on_armature(armature, primary_axis, secondary_axis)
            axes_reverted = True
            decoder.apply_transforms(
                armature,
                scales,
                rotations,
                translations,
                original_bones,
            )
            meshes = utils.armature.apply_all_as_shapekey(armature, shapekey_name="CPlus")
            failed_meshes = [mesh.name for mesh in meshes if not mesh.data.shape_keys or not mesh.data.shape_keys.key_blocks.get("CPlus")]
            if failed_meshes:
                raise RuntimeError(f"Could not bake C+ shapekeys on: {', '.join(failed_meshes)}")
            utils.armature.new_rest_pose(armature)
            utils.axis_conversion.apply_bone_axis_to_armature(armature, primary_axis, secondary_axis)
            axes_reverted = False
        except Exception as exc:
            self.report({"ERROR"}, f"Failed to apply C+ transforms: {exc}")
            return {"CANCELLED"}
        finally:
            if axes_reverted:
                utils.axis_conversion.apply_bone_axis_to_armature(armature, primary_axis, secondary_axis)
            utils.armature.restore_bone_parenting(armature, parent_map)
            utils.object.select_only(armature)
            bpy.ops.object.mode_set(mode="OBJECT")

        settings.applied = True
        self.report(
            {"INFO"},
            "C+ transforms applied, shapekeys baked, rest pose set, and parenting restored.",
        )
        return {"FINISHED"}


class AETHER_OT_CreateBackupArmature(bpy.types.Operator):
    """Create or replace the C+ revert backup armature."""

    bl_label = "Create Backup Armature"
    bl_idname = "aether.create_backup_armature"
    bl_description = "Create a backup armature for C+ reversion."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        """Duplicate the active armature as its C+ backup."""
        armature = context.active_object
        if armature is None or armature.type != "ARMATURE":
            self.report({"ERROR"}, "Select a valid armature object.")
            return {"CANCELLED"}
        settings = getattr(armature, "aether_cplus", None)
        if settings is None:
            self.report({"ERROR"}, "C+ settings are unavailable for this armature.")
            return {"CANCELLED"}
        if armature.data.collections.get("Original") is None:
            self.report({"ERROR"}, "The armature is missing its Original bone collection.")
            return {"CANCELLED"}

        if settings.backup_armature:
            old_backup = settings.backup_armature
            old_backup.hide_set(False)
            old_backup.hide_viewport = False
            bpy.data.objects.remove(old_backup, do_unlink=True)
            settings.backup_armature = None

        utils.object.select_only(armature)
        backup = utils.armature.duplicate(armature)
        backup.name = f"BACKUP_{armature.name}"
        backup.parent = armature
        backup.matrix_parent_inverse = armature.matrix_world.inverted()
        settings.backup_armature = backup

        collection = utils.collection.get_collection(armature)
        if collection:
            utils.collection.link_to_collection([backup], collection)
        utils.object.set_visibility(backup, False)
        utils.object.select_only(armature)
        self.report({"INFO"}, f"Created backup armature '{backup.name}'.")
        return {"FINISHED"}


class AETHER_OT_RevertToBackup(bpy.types.Operator):
    """Restore the Original bones from the saved backup."""

    bl_label = "Revert to Backup"
    bl_idname = "aether.revert_cplus_to_backup"
    bl_description = "Revert the armature to its backup state."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        """Restore armature bones and remove the applied C+ shapekey."""
        armature = context.active_object
        if armature is None or armature.type != "ARMATURE":
            self.report({"ERROR"}, "Select a valid armature object.")
            return {"CANCELLED"}
        settings = getattr(armature, "aether_cplus", None)
        backup = settings.backup_armature if settings else None
        if backup is None:
            self.report({"ERROR"}, "No backup armature found. Create a backup first.")
            return {"CANCELLED"}

        original_collection = armature.data.collections.get("Original")
        if original_collection is None:
            self.report({"ERROR"}, "The armature is missing its Original bone collection.")
            return {"CANCELLED"}

        original_bone_names = [bone.name for bone in original_collection.bones]
        bone_data: dict[str, tuple[Vector, Vector, float]] = {}
        utils.object.set_visibility(backup, True)
        try:
            utils.object.select_only(backup)
            bpy.ops.object.mode_set(mode="EDIT")
            for bone_name in original_bone_names:
                bone = backup.data.edit_bones.get(bone_name)
                if bone:
                    bone_data[bone_name] = (bone.head.copy(), bone.tail.copy(), bone.roll)

            utils.object.select_only(armature)
            bpy.ops.object.mode_set(mode="EDIT")
            for bone_name, (head, tail, roll) in bone_data.items():
                bone = armature.data.edit_bones.get(bone_name)
                if bone:
                    bone.head = head
                    bone.tail = tail
                    bone.roll = roll
        finally:
            utils.object.select_only(armature)
            bpy.ops.object.mode_set(mode="OBJECT")
            utils.object.set_visibility(backup, False)

        for mesh in utils.armature.find_meshes(armature):
            utils.object.remove_shapekey(mesh, "CPlus", True, "ImportedPose")

        settings.applied = False
        self.report({"INFO"}, "Reverted C+ changes to the backup armature state.")
        return {"FINISHED"}


class AETHER_OT_ParseFromMCDF(bpy.types.Operator):
    """Load a Customize+ string from an MCDF file."""

    bl_label = "Parse from MCDF file"
    bl_idname = "aether.parse_cplus_from_mcdf"
    bl_description = "Read the C+ string from an MCDF file."
    bl_options = {"REGISTER", "UNDO"}

    filepath: StringProperty(subtype="FILE_PATH")  # type: ignore
    filter_glob: StringProperty(default="*.mcdf", options={"HIDDEN"})  # type: ignore

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set[str]:
        """Open the file browser for an MCDF file."""
        default_path = get_preferences().default_cplus_import_path
        if default_path:
            self.filepath = default_path
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        """Extract C+ data from the selected MCDF file."""
        armature = context.active_object
        settings = getattr(armature, "aether_cplus", None)
        if settings is None:
            self.report({"ERROR"}, "Select an armature with C+ settings.")
            return {"CANCELLED"}
        if not self.filepath.lower().endswith(".mcdf"):
            self.report({"ERROR"}, "Select a valid .mcdf file.")
            return {"CANCELLED"}

        context.window.cursor_set("WAIT")
        try:
            cplus_string = decoder.get_mcdf_cplus(self.filepath)
        finally:
            context.window.cursor_set("DEFAULT")

        if cplus_string is None:
            self.report({"ERROR"}, "The MCDF file is invalid or could not be read.")
            return {"CANCELLED"}
        if not cplus_string:
            self.report({"WARNING"}, "The MCDF file does not contain C+ data.")
            return {"CANCELLED"}

        settings.code = cplus_string
        self.report({"INFO"}, "C+ string read from MCDF file.")
        return {"FINISHED"}


class AETHER_OT_PasteFromClipboard(bpy.types.Operator):
    """Paste a Customize+ string from the clipboard."""

    bl_label = "Paste from Clipboard"
    bl_idname = "aether.paste_cplus_from_clipboard"
    bl_description = "Paste a C+ string from the clipboard."
    bl_options = {"REGISTER"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        """Store clipboard contents in the active armature's C+ settings."""
        armature = context.active_object
        settings = getattr(armature, "aether_cplus", None)
        if settings is None:
            self.report({"ERROR"}, "Select an armature with C+ settings.")
            return {"CANCELLED"}

        clipboard_text = context.window_manager.clipboard.strip()
        if not clipboard_text:
            self.report({"ERROR"}, "The clipboard is empty.")
            return {"CANCELLED"}

        settings.code = clipboard_text
        self.report({"INFO"}, "C+ string pasted from clipboard.")
        return {"FINISHED"}


CLASSES = (
    AETHER_OT_QuickApplyCustomizePlus,
    AETHER_OT_CreateBackupArmature,
    AETHER_OT_RevertToBackup,
    AETHER_OT_ParseFromMCDF,
    AETHER_OT_PasteFromClipboard,
)


def register() -> None:
    """Register this module's operators."""
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister() -> None:
    """Unregister this module's operators."""
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
