<!-- AI/agent note: Rules are numbered (R-x.y) and use MUST / MUST NOT / SHOULD. Cite rule IDs in reviews. Section 12 is a checklist for new code. -->
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
## 2. Feature Toggle (REQUIRED)

Every feature MUST be fully enableable and disableable at runtime from preferences, with no Blender restart.

- R-2.1 Each feature's `__init__.py` MUST define:
  ```python
  FEATURE = FeatureInfo(id="spring_bones", label="Spring Bones", default_enabled=True, always_on=False)
  def register() -> None: ...
  def unregister() -> None: ...
  ```
- R-2.2 Enabled state MUST be stored in a preference property (extends the existing `enabled_feature_sets`). Toggle changes MUST call the feature's `register()` or `unregister()` through one central function in `preferences/`.
- R-2.3 `unregister()` MUST remove everything the feature added: operators, panels, menus, property groups, `Scene`/`Object`/`Armature` pointer properties, handlers, timers, keymaps, icons/preview collections and driver namespace entries. Remove in reverse order of registration.
- R-2.4 `register()` and `unregister()` MUST be idempotent. Calling either twice MUST NOT raise.
- R-2.5 A disabled feature MUST NOT register anything and MUST NOT run code at import time. Imports MUST be side-effect free.
- R-2.6 Panels in other features MUST NOT assume a feature is enabled. Check through the public API (`is_enabled()`).
- R-2.7 Data a feature stores in `.blend` files MUST survive being disabled and re-enabled. Unregistering MUST NOT delete user data.
- R-2.8 `always_on=True` is only for features the add-on cannot work without, such as preferences.
- R-2.9 `unregister()` MUST be tested by toggling off then on in Blender before merging.

## 3. Naming

| Item | Convention | Example |
|------|-----------|---------|
| Operator `bl_idname` | `aether.<feature>_<action>` | `aether.spring_bones_generate_tail` |
| Operator class | `AETHER_OT_<feature>_<action>` | `AETHER_OT_spring_bones_generate_tail` |
| Panel class and id | `AETHER_PT_<feature>_<name>` | `AETHER_PT_spring_bones_main` |
| Menu class and id | `AETHER_MT_<feature>_<name>` | `AETHER_MT_vfx_model` |
| Property group class | `AETHER_PG_<feature>_<name>` | `AETHER_PG_rigging_settings` |
| Scene/Object property | `aether_<feature>` | `scene.aether_rigging` |
| Operator file | the action | `generate_tail.py` |
| Function, variable | `lower_snake_case` | `get_bone_chain` |
| Constant | `ALL_CAPS` | `DEFAULT_BONE_SIZE` |
| Private helper | leading `_` | `_collect_bones` |

- R-3.1 File names MUST NOT use `_ot`, `_pt` or `_prop` suffixes. The folder states the type.
- R-3.2 `<feature>` in IDs MUST equal the feature folder name.
- R-3.3 `bl_idname` MUST be lowercase with exactly one dot.

## 4. Operators

- R-4.1 One operator per file; the file name is the action.
- R-4.2 MUST define `bl_idname`, `bl_label`, `bl_description`. MUST NOT have a docstring.
- R-4.3 An operator MUST only contain `poll`, `invoke`/`execute`/`modal` and user reporting. Logic MUST live in `utils/` or `shared/`.
- R-4.4 MUST report through `self.report`, with a clear, actionable message.
- R-4.5 Operators that change data SHOULD include `"UNDO"` in `bl_options`.

## 5. Registration

- R-5.1 Classes MUST be listed in explicit `CLASSES` tuples in `operators/__init__.py` and `ui/__init__.py`. Auto-discovery is forbidden.
- R-5.2 `register()` registers in order: property groups, operators, UI. `unregister()` reverses it.

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
- R-7.6 Explanations longer than a few lines MUST go in the feature `README.md` or `docs/`, not in code.
- R-7.7 Comments explain *why*, never *what*.

## 8. Utilities

- R-8.1 Name functions without the module name: `bone.exist()`, not `bone.bone_exist()`.
- R-8.2 Utilities that change mode MUST restore the original mode on exit, including on error.

## 9. Imports

- R-9.1 Order: standard library, third party (`bpy`, `mathutils`), local.
- R-9.2 MUST import modules, not names: `from . import bone`. A wildcard import is only allowed from a module that defines `__all__`, so the star import brings in exactly the public API (for example `from ....instructions import *` in rig modules).
- R-9.3 Inside a feature use relative imports. For shared code use `from ...shared.utils import bone`.

## 10. Console and Errors

- R-10.1 Console output MUST start with `[AetherBlend]`.
- R-10.2 Operators use `self.report`. Utilities use `print`.

## 11. Feature README

Each `features/<feature>/README.md` MUST contain:
1. One-paragraph description.
2. Operator table with columns: `bl_idname` | Label | Description | UI location | Requirements.
3. Public API and limitations.

The wiki operator reference is generated from these files.

## 12. Checklist for New or Changed Code

- [ ] Lives in the correct feature, with no cross-feature imports (R-1.2)
- [ ] Feature `register()`/`unregister()` cleans up everything (R-2.3) and toggles on/off (R-2.9)
- [ ] ID and class names follow section 3
- [ ] One operator per file with `bl_label` and `bl_description` (R-4.1, R-4.2)
- [ ] Types on all functions (R-6.1); one-line docstrings on public ones (R-7.2)
- [ ] Feature README operator table updated (R-11)
- [ ] `ruff check` passes

## 13. Example

```python
"""Generate spring bones for the tail chain."""

import bpy

from ...shared.utils import bone


class AETHER_OT_spring_bones_generate_tail(bpy.types.Operator):
    bl_idname = "aether.spring_bones_generate_tail"
    bl_label = "Generate Spring Tail"
    bl_description = "Create a spring bone setup for the selected tail chain"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        obj = context.active_object
        return obj is not None and obj.type == "ARMATURE"

    def execute(self, context: bpy.types.Context) -> set[str]:
        if not bone.exist(context.active_object, "n_hara"):
            self.report({"ERROR"}, "[AetherBlend] Armature has no 'n_hara' bone.")
            return {"CANCELLED"}
        return {"FINISHED"}
```
