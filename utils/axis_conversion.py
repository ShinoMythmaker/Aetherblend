"""Axis conversion utilities shared across all AetherBlend import/export systems.
"""

import bpy
from bpy.props import EnumProperty
from bpy_extras.io_utils import axis_conversion as _bpy_axis_conversion
from mathutils import Matrix


# ---------------------------------------------------------------------------
# Shared axis-choice enum items
# ---------------------------------------------------------------------------

AXIS_ITEMS = (
    ('X',  "X",  ""),
    ('Y',  "Y",  ""),
    ('Z',  "Z",  ""),
    ('-X', "-X", ""),
    ('-Y', "-Y", ""),
    ('-Z', "-Z", ""),
)


# ---------------------------------------------------------------------------
# Matrix helpers
# ---------------------------------------------------------------------------

def get_import_correction_matrix(primary_axis: str, secondary_axis: str) -> Matrix:
    """Return the 4×4 bone-correction matrix for import.

    Converts from game-engine Y-up bone space (Y forward, X secondary) to the
    target Blender orientation defined by *primary_axis* and *secondary_axis*.
    Returns the identity matrix when no conversion is needed (Y/X).
    """
    if (primary_axis, secondary_axis) == ('Y', 'X'):
        return Matrix.Identity(4)
    return _bpy_axis_conversion(
        from_up='Y', from_forward='X',
        to_up=primary_axis, to_forward=secondary_axis,
    ).to_4x4()


def get_export_correction_matrix(primary_axis: str, secondary_axis: str) -> Matrix:
    """Return the 4×4 bone-correction matrix for export.

    Converts from the Blender orientation (primary_axis/secondary_axis) back to
    game-engine Y-up bone space (Y forward, X secondary).
    Returns the identity matrix when no conversion is needed (Y/X).
    """
    if (primary_axis, secondary_axis) == ('Y', 'X'):
        return Matrix.Identity(4)
    return _bpy_axis_conversion(
        from_up=primary_axis, from_forward=secondary_axis,
        to_up='Y', to_forward='X',
    ).to_4x4()


# ---------------------------------------------------------------------------
# Armature bone-axis helpers
# ---------------------------------------------------------------------------

def apply_bone_axis_to_armature(
    armature: bpy.types.Object,
    primary_axis: str,
    secondary_axis: str,
) -> None:
    """Apply import axis correction to every edit bone in *armature*.

    Converts bones from Y-up game-engine space to the specified Blender
    orientation.  This is the standard step performed after importing a
    character model from FFXIV / similar game engines.

    Switches to EDIT mode internally and restores the previous mode when done.
    Is a no-op when (primary_axis, secondary_axis) == ('Y', 'X').
    """
    if not armature or armature.type != 'ARMATURE':
        return
    if (primary_axis, secondary_axis) == ('Y', 'X'):
        return

    correction = get_import_correction_matrix(primary_axis, secondary_axis)
    previous_mode = armature.mode

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    try:
        for bone in armature.data.edit_bones:
            bone.matrix = bone.matrix @ correction
    finally:
        bpy.ops.object.mode_set(mode=previous_mode)


def revert_bone_axis_on_armature(
    armature: bpy.types.Object,
    primary_axis: str,
    secondary_axis: str,
) -> None:
    """Revert import axis correction from every edit bone in *armature*.

    Converts bones back from the Blender orientation to Y-up game-engine space.
    Used before applying C+ transforms, which are expressed in the original
    game-engine bone space.

    Switches to EDIT mode internally and restores the previous mode when done.
    Is a no-op when (primary_axis, secondary_axis) == ('Y', 'X').
    """
    if not armature or armature.type != 'ARMATURE':
        return
    if (primary_axis, secondary_axis) == ('Y', 'X'):
        return

    correction = get_import_correction_matrix(primary_axis, secondary_axis)
    previous_mode = armature.mode

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    try:
        for bone in armature.data.edit_bones:
            bone.matrix = bone.matrix @ correction.inverted()
    finally:
        bpy.ops.object.mode_set(mode=previous_mode)



