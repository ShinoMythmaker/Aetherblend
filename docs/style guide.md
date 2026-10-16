<!-- AI/agent note: Rules are numbered (R-x.y) and use MUST / MUST NOT / SHOULD. Cite rule IDs in reviews. Section 13 is a checklist for new code. -->
# AetherBlend Style Guide

Scope: all Python in this add-on. Python target: see `ruff.toml`. Linter: `ruff`.

## 1. Layout

```
AetherBlend/
  __init__.py            # register()/unregister() for the whole add-on
  preferences.py         # add-on preferences + feature toggles
  ui/                    # shared UI: tabs.py (active tab state), visibility.py, info panel
  utils/                 # helpers shared by 2+ features, grouped by what they act on
  features/
    __init__.py          # registry of features
    <feature>/
      __init__.py        # docstring, __all__ (public API), register(), unregister()
      operators.py       # operators (or operators/<action>.py when large)
      panels.py          # panels and menus
      properties.py      # property groups
    rig_generator/
      definitions.py     # RigModule, Template, UILink
      generator.py       # the generation pipeline
      instructions/      # functions a rig module calls to build the rig
      library/           # modules/, templates/, colorsets/, ui_links.py
      rigify/            # rigify settings (collections, colorsets)
```

Features: `import_export` (import characters, export poses and animations), `shaders`, `rig_generator` (build a rig), `rig_edit` (convert and clean up a generated rig), `rig_ui` (use a generated rig: layers, rig UI, eyelid editing).

- R-1.1 A feature MUST be a self-contained package under `features/`.
- R-1.2 A feature MAY import `utils/`, `ui/` and `preferences`. A feature MUST NOT import another feature except through the names in that feature's `__all__` (for example `from ..rig_generator import instructions`).
- R-1.3 Code needed by 2+ features MUST move to `utils/` or `ui/`.
- R-1.4 Every feature `__init__.py` MUST have a one-line docstring and an `__all__`.
- R-1.5 Files SHOULD stay under ~300 lines. Split when longer.
- R-1.6 Operator IDs follow `aether.<feature>_<action>` (section 3), so the ID tells which feature owns the operator.
- R-1.7 Files that are not part of the public API (for example `_viera.py`) start with `_`.

## 2. Registration and Cleanup

- R-2.1 Each feature's `__init__.py` MUST define `register() -> None` and `unregister() -> None`. They go through a `modules` tuple: register in order, unregister in reverse.
- R-2.2 `unregister()` MUST remove everything the feature added: operators, panels, menus, property groups, `Scene`/`Object`/`Armature` pointer properties, handlers, timers, keymaps and icons.
- R-2.3 `register()` and `unregister()` MUST be idempotent. Calling either twice MUST NOT raise.
- R-2.4 Imports MUST be side-effect free. Nothing registers or runs Blender code at import time.
- R-2.5 Feature sets in `preferences.py` only drive dependency checks. They do not enable or disable a feature at runtime.
- R-2.6 Data a feature stores in `.blend` files MUST survive an unregister and register. Unregistering MUST NOT delete user data.
- R-2.7 Disabling and re-enabling the add-on in Blender MUST be tested before merging.


## 3. Naming

| Item | Convention | Example |
|------|-----------|---------|
| Operator `bl_idname` | `aether.<feature>_<action>` | `aether.rig_edit_set_inherit_scale` |
| Operator class | `AETHER_OT_<feature>_<action>` | `AETHER_OT_rig_edit_set_inherit_scale` |
| Panel class and id | `AETHER_PT_<feature>_<name>` | `AETHER_PT_rig_ui_layers` |
| Menu class and id | `AETHER_MT_<feature>_<name>` | `AETHER_MT_shaders_presets` |
| Property group class | `AETHER_PG_<feature>_<name>` | `AETHER_PG_rig_generator_rig` |
| Scene/Object/Armature property | `aether_<name>` | `object.aether_rig`, `scene.aether_tabs` |
| Rig module class | `Module` in a file named after the variant | `modules/arms/ffxiv_default.py` |
| Function, variable | `lower_snake_case` | `get_bone_chain` |
| Constant | `ALL_CAPS` | `DEFAULT_BONE_SIZE` |
| Private helper | leading `_` | `_collect_bones` |

- R-3.1 File names MUST NOT use `_ot`, `_pt` or `_prop` suffixes. The folder states the type.
- R-3.2 `<feature>` in IDs and class names MUST equal the feature folder name. `ui/` and `preferences.py` use `ui` and `preferences`.
- R-3.3 `bl_idname` MUST be lowercase with exactly one dot.
- R-3.4 A panel's `bl_idname` MUST equal its class name.
- R-3.5 Class names follow this table, not CapWords. Ruff ignores N801 for that reason.

## 4. Operators

- R-4.1 Operators of one feature live in the feature's `operators.py`. When that file passes ~300 lines, split it into `operators/<action>.py`, one operator per file.
- R-4.2 MUST define `bl_idname`, `bl_label`, `bl_description`. MUST NOT have a docstring.
- R-4.3 An operator MUST only contain `poll`, `invoke`/`execute`/`modal` and user reporting. Logic MUST live in `utils/` or in the feature's own modules.
- R-4.4 MUST report through `self.report`, with a clear, actionable message.
- R-4.5 Operators that change data SHOULD include `"UNDO"` in `bl_options`.

## 5. Registration

- R-5.1 Every Blender class MUST be registered with an explicit `bpy.utils.register_class(...)` call in the `register()` of the file that defines it, and removed in that file's `unregister()` in reverse order. Auto-discovery of Blender classes is forbidden.
- R-5.2 Rig modules are the exception: `library/modules/<name>/__init__.py` lists the variants, and `library/modules/__init__.py` collects the packages.
- R-5.3 A feature's `modules` tuple registers property groups first, then operators, then panels. `unregister()` reverses it.

## 6. Type Hints

- R-6.1 Every function MUST type all arguments and the return value.
- R-6.2 MUST use Blender types (`bpy.types.Object`, `bpy.types.Context`, ...). `Any` only when no better type exists.
- R-6.3 Operator `execute` returns `set[str]`.

## 7. Documentation

- R-7.1 Each module MUST start with a one-line docstring.
- R-7.2 Each public function MUST have a one-line imperative docstring:
  ```python
  def exist(armature: bpy.types.Object, name: str) -> bool:
      """Return True if the armature has a bone with this name."""
  ```
- R-7.3 `Args:`, `Returns:`, `Raises:` sections are only allowed when name and types do not explain the function.
- R-7.4 Private `_helpers` need no docstring when name and types are clear.
- R-7.5 Properties MUST have `description=`. Operators use `bl_description`. These are the UI tooltips.
- R-7.6 Explanations longer than a few lines MUST go in `docs/`, not in code.
- R-7.7 Comments explain *why*, never *what*.

## 8. Utilities

- R-8.1 Name functions without the module name: `armature.get_pose_bone()`, not `armature.armature_get_pose_bone()`.
- R-8.2 Utilities that change mode MUST restore the original mode on exit, including on error.

## 9. Imports

- R-9.1 Order: standard library, third party (`bpy`, `mathutils`), local.
- R-9.2 MUST import modules, not names: `from . import bone`. A wildcard import is only allowed from a module that defines `__all__`, so the star import brings in exactly the public API (for example `from ....instructions import *` in rig modules).
- R-9.3 Inside a feature use relative imports. Shared code: `from ...utils import armature as armature_utils`. Another feature: `from ..rig_generator import instructions` (R-1.2).
- R-9.4 Import `bpy` and `bpy.types` names at the top of the file. Do not import inside functions unless it avoids a circular import, and then say so in a comment.

## 10. Console and Errors

- R-10.1 Console output MUST start with `[AetherBlend]`.
- R-10.2 Operators use `self.report`. Utilities use `print`.
- R-10.3 MUST NOT use a bare `except:`. Catch the specific exceptions.

## 11. Documentation Files

- R-11.1 `docs/operators.md` MUST list every operator with: `bl_idname` | Label | Description | UI location | Requirements. The wiki operator reference is copied from it.
- R-11.2 When an operator is added, renamed or removed, `docs/operators.md` MUST change in the same change.

## 12. Rig Modules

Rig modules live in `features/rig_generator/library/modules/<part>/<variant>.py`. Copy `modules/demo_module/` to start one.

- R-12.1 A variant defines `class Module(RigModule)` with `name`, `requires` and `ui_collections`.
- R-12.2 Build steps are the methods `meta_edit`, `meta_pose`, `final_edit`, `final_pose`. Delete the ones you do not need.
- R-12.3 Steps only call functions from `instructions`, imported with `from ....instructions import *`. A step MUST NOT use `bpy.ops` directly.
- R-12.4 Register a variant in its package `__init__.py` as `from .<variant> import Module as <variant>` and add it to `__all__`. Add the package to `modules/__init__.py` when it is new.
- R-12.5 Shared helpers for variants of one part go in a file that starts with `_` (for example `_viera.py`).

## 13. Checklist for New or Changed Code

- [ ] Lives in the correct feature, with no cross-feature imports (R-1.2)
- [ ] `register()`/`unregister()` removes everything (R-2.2) and the add-on was toggled off and on (R-2.7)
- [ ] IDs and class names follow section 3
- [ ] Operators have `bl_label` and `bl_description` (R-4.2)
- [ ] Types on all functions (R-6.1); one-line docstrings on public ones (R-7.2)
- [ ] `docs/operators.md` updated (R-11.2)
- [ ] `ruff check .` passes

## 14. Examples

Operator (`features/rig_edit/operators.py`):

```python
"""Operators that convert and clean up a generated rig."""

import bpy


class AETHER_OT_rig_edit_set_inherit_scale(bpy.types.Operator):
    bl_idname = "aether.rig_edit_set_inherit_scale"
    bl_label = "Set Inherit Scale"
    bl_description = "Set inherit scale for bones in the LINK collection"
    bl_options = {"REGISTER", "UNDO"}

    inherit_scale: bpy.props.EnumProperty(
        name="Inherit Scale",
        description="Inherit scale mode applied to the LINK bones",
        items=[("FULL", "Full", "Full inherit scale"), ("NONE", "None", "No scale inheritance")],
        default="FULL",
    )  # type: ignore

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        obj = context.active_object
        return obj is not None and obj.type == "ARMATURE"

    def execute(self, context: bpy.types.Context) -> set[str]:
        armature = context.active_object
        if armature.data.collections.get("LINK") is None:
            self.report({"ERROR"}, "LINK collection not found")
            return {"CANCELLED"}
        for pose_bone in armature.pose.bones:
            if pose_bone.bone.collections.get("LINK"):
                pose_bone.bone.inherit_scale = self.inherit_scale
        return {"FINISHED"}


def register() -> None:
    bpy.utils.register_class(AETHER_OT_rig_edit_set_inherit_scale)


def unregister() -> None:
    bpy.utils.unregister_class(AETHER_OT_rig_edit_set_inherit_scale)
```

Rig module (`features/rig_generator/library/modules/demo_module/demo_module.py`):

```python
"""Demo module: copy this folder to start a new rig module."""

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

Tooling: `ruff check .` enforces naming (N), type hints (ANN), docstrings (D) and imports (I) from `ruff.toml`.
