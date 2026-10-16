# Writing Rig Modules

A rig module describes how one part of a character (arms, eyes, hair, ...) is turned into a Rigify rig. Modules are small classes that run a list of instructions.

Where modules live and which one to copy as a starting point can change, so look for the demo module in the rig generator's library.

## Rules

- R-M.1 A module variant defines `class Module(RigModule)` with `name`, `requires` and `ui_collections`.
- R-M.2 Build steps are the methods `meta_edit`, `meta_pose`, `final_edit` and `final_pose`. Define only the ones you need.
- R-M.3 Steps only call functions from the instruction set. A step MUST NOT use `bpy.ops` directly.
- R-M.4 A variant is exposed from its package `__init__.py` and listed in `__all__`. A new part package is added to the modules package.
- R-M.5 Helpers shared by variants of one part go in a file whose name starts with `_`.

## Build Steps

| Step | Runs on | Typical use |
|------|---------|-------------|
| `meta_edit` | meta rig, edit mode | create, connect, align and parent bones |
| `meta_pose` | meta rig, pose mode | assign Rigify types, bone collections |
| `final_edit` | generated rig, edit mode | adjust bones after Rigify ran |
| `final_pose` | generated rig, pose mode | constraints, drivers, locks |

## `requires`

A tuple of bone names that must exist in the source armature. If any is missing, the module is skipped, so a character without that part still generates.

## Example

```python
"""Demo module: copy this to start a new rig module."""

import bpy

from ....definitions import RigModule
from ....instructions import *
from ....rigify.settings import BoneCollection, UI_Collections


class Module(RigModule):
    name = "Demo"
    requires = ("j_example_bone",)
    ui_collections = UI_Collections(
        [
            BoneCollection(name="Demo (IK)", ui=True, color_set="IK_Left", row_index=1, title="Demo IK"),
        ]
    )

    def meta_edit(self, rig: bpy.types.Object) -> None:
        connect(rig, "demo_bone", "j_example_bone", "j_example_bone", end_point="tail", parent="Spine.001")

    def meta_pose(self, rig: bpy.types.Object) -> None:
        rigify.basic_super_copy(rig, "demo_bone")
        collection(rig, ["demo_bone"], "Demo (IK)")
```
