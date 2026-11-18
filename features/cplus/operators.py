"""Operators for applying and managing Customize+ armature data."""

import warnings

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
        ########
        # Check Armature and C+ Settings
        ########
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
        if settings.applied:
            self.report({"ERROR"}, "Revert the existing C+ changes before applying another string.")
            return {"CANCELLED"}

        ########
        # Decode C+ String and Check Bones
        ########
        cplus_data = decoder.decode_cplus_string(settings.code)

        original_bones = utils.armature.b_collection.get_pose_bones(armature, "Original")
        if not original_bones:
            self.report({"ERROR"}, "The Original bone collection contains no bones.")
            return {"CANCELLED"}
        missing_bones = sorted(set(cplus_data["Bones"]) - set(original_bones))
        if missing_bones:
            self.report({"WARNING"}, f"C+ bones absent from Original collection: {', '.join(missing_bones)}")

        ########
        # Check Meshes and Save Original State
        ########
        meshes = utils.armature.find_meshes(armature)
        for mesh in meshes:
            modifiers = [modifier for modifier in mesh.modifiers if modifier.type == "ARMATURE" and modifier.object == armature]
            if len(modifiers) != 1:
                self.report({"ERROR"}, f"Mesh '{mesh.name}' needs exactly one modifier referencing this armature to bake C+.")
                return {"CANCELLED"}
            if mesh.data.shape_keys and mesh.data.shape_keys.key_blocks.get("CPlus"):
                self.report({"ERROR"}, f"Mesh '{mesh.name}' already has a CPlus shapekey; revert or remove it first.")
                return {"CANCELLED"}
        original_pose = {bone.name: bone.matrix_basis.copy() for bone in armature.pose.bones}
        original_scale_inheritance = {bone.name: bone.inherit_scale for bone in armature.data.bones}
        original_shapekeys = {
            mesh.name: [(key.name, key.mute, key.value) for key in mesh.data.shape_keys.key_blocks]
            for mesh in meshes
            if mesh.data.shape_keys
        }
        original_rest_pose = {
            bone.name: (bone.head_local.copy(), bone.tail_local.copy(), bone.matrix_local.copy()) for bone in armature.data.bones
        }

        ########
        # Apply Transforms and Bake Shapekeys
        ########
        utils.object.select_only(armature)
        utils.armature.reset_pose_bones(armature)
        applied = False
        try:
            with warnings.catch_warnings(record=True) as transform_warnings:
                warnings.simplefilter("always", RuntimeWarning)
                decoder.apply_transforms(armature, cplus_data, original_bones)
            for message in dict.fromkeys(str(warning.message) for warning in transform_warnings):
                self.report({"WARNING"}, message)

            meshes = utils.armature.apply_all_as_shapekey(armature, shapekey_name="CPlus")
            failed_meshes = [mesh.name for mesh in meshes if not mesh.data.shape_keys or not mesh.data.shape_keys.key_blocks.get("CPlus")]
            if failed_meshes:
                raise RuntimeError(f"Could not bake C+ shapekeys on: {', '.join(failed_meshes)}")
            utils.armature.new_rest_pose(armature)
            applied = True
        except (ValueError, RuntimeError) as exc:
            self.report({"ERROR"}, f"Failed to apply C+ transforms: {exc}")
            return {"CANCELLED"}
        finally:
            ########
            # Restore State and Clean Up
            ########
            utils.object.select_only(armature)
            bpy.ops.object.mode_set(mode="OBJECT")
            if not applied:
                bpy.ops.object.mode_set(mode="EDIT")
                for bone in armature.data.edit_bones:
                    head, tail, matrix = original_rest_pose[bone.name]
                    bone.matrix = matrix
                    bone.head = head
                    bone.tail = tail
                bpy.ops.object.mode_set(mode="OBJECT")
                for mesh in meshes:
                    if not mesh.data.shape_keys:
                        continue
                    cplus_key = mesh.data.shape_keys.key_blocks.get("CPlus")
                    if cplus_key:
                        mesh.shape_key_remove(cplus_key)
                    if mesh.name not in original_shapekeys:
                        mesh.shape_key_clear()
                    for name, mute, value in original_shapekeys.get(mesh.name, []):
                        key = mesh.data.shape_keys.key_blocks.get(name)
                        if key:
                            key.mute = mute
                            key.value = value
                for bone in armature.pose.bones:
                    bone.matrix_basis = original_pose[bone.name]

            # Scale inheritance is restored on both success and failure.
            for bone in armature.data.bones:
                bone.inherit_scale = original_scale_inheritance[bone.name]
            context.view_layer.update()

        settings.applied = True
        self.report(
            {"INFO"},
            "C+ model-space transforms applied and baked",
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
        ########
        # Check Armature and Existing Backup
        ########
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

        ########
        # Create Backup
        ########
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
        ########
        # Check Armature and Backup
        ########
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
        backup_bones: dict[str, tuple[Vector, Vector, float]] = {}

        ########
        # Copy Original Bone Positions from Backup
        ########
        utils.object.set_visibility(backup, True)
        try:
            utils.object.select_only(backup)
            bpy.ops.object.mode_set(mode="EDIT")
            for bone_name in original_bone_names:
                bone = backup.data.edit_bones.get(bone_name)
                if bone:
                    backup_bones[bone_name] = (bone.head.copy(), bone.tail.copy(), bone.roll)

            ########
            # Restore Bone Positions on Armature
            ########
            utils.object.select_only(armature)
            bpy.ops.object.mode_set(mode="EDIT")
            for bone_name, (head, tail, roll) in backup_bones.items():
                bone = armature.data.edit_bones.get(bone_name)
                if bone:
                    bone.head = head
                    bone.tail = tail
                    bone.roll = roll
        finally:
            utils.object.select_only(armature)
            bpy.ops.object.mode_set(mode="OBJECT")
            utils.object.set_visibility(backup, False)

        ########
        # Remove C+ Shapekeys
        ########
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
