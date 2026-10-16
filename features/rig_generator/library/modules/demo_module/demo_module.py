"""Demo module: copy this folder to start a new rig module.

How to use it:
1. Copy the `demo_module` folder, then rename the folder and the file inside it.
2. In the new `__init__.py`, change both names (`from .my_module import Module as my_module`).
3. Fill in `name`, `requires`, `ui_collections` and the four steps below.
4. Add the module to a template in `library/templates/`, e.g. `[my_module.my_module]`.

The generator runs the steps in this order, and each step gets the rig to work on:
    meta_edit   - meta rig, edit mode: create and parent the bones.
    meta_pose   - meta rig, pose mode: rigify types, bone collections, links.
    final_edit  - generated rig, edit mode: fix up bones after rigify ran.
    final_pose  - generated rig, pose mode: constraints and custom properties.
A step you do not need can simply be deleted.
"""

import bpy

from ....definitions import RigModule
from ....instructions import *
from ....rigify.settings import BoneCollection, UI_Collections


class Module(RigModule):
    # Shown in the log when the module is skipped.
    name = "Demo"

    # Bones that must exist in the source armature. If one is missing, the module is skipped.
    requires = ("j_example_bone",)

    # Bone collections shown in the rig UI.
    ui_collections = UI_Collections(
        [
            BoneCollection(name="Demo (IK)", ui=True, color_set="IK_Left", row_index=1, title="Demo IK"),
            BoneCollection(name="Demo (FK)", ui=True, color_set="FK_Left", row_index=2, title="Demo FK", visible=False),
        ]
    )

    def meta_edit(self, rig: bpy.types.Object) -> None:
        # Create a bone from one source bone to another.
        connect(rig, "demo_bone", "j_example_bone", "j_example_bone", end_point="tail", parent="Spine.001")
        # Create a bone that continues from a source bone.
        extend(rig, "demo_bone_tip", "j_example_bone", parent="demo_bone", connected=True)

    def meta_pose(self, rig: bpy.types.Object) -> None:
        # Give a bone a rigify type.
        rigify.basic_super_copy(rig, "demo_bone")
        # Put bones into a bone collection.
        collection(rig, ["demo_bone", "demo_bone_tip"], "Demo (IK)")
        # Make the original bone follow a bone of the generated rig.
        link(rig, "j_example_bone", "DEF-demo_bone")

    def final_edit(self, rig: bpy.types.Object) -> None:
        # Parent a bone after rigify generated the rig.
        parent(rig, "demo_bone_tip", "DEF-demo_bone")

    def final_pose(self, rig: bpy.types.Object) -> None:
        # Add a constraint and set a custom property.
        constraints.damped_track(rig, "demo_bone", target="demo_bone_tip")
        prop(rig, "demo_bone", "Demo_Property", 0)
