<!-- AI/agent note: Rules are numbered (R-x.y) and use MUST / MUST NOT / SHOULD. Cite rule IDs in reviews. Section 12 is a checklist for new code. -->
# AetherBlend Style Guide

These are conventions, not a map of the repository. The add-on is in beta and its structure changes often. The rules below describe how code is written and organised, and they should stay true when folders move or features are added. If a rule needs an edit because a file moved, the rule is too specific.

Python target and lint rules live in `ruff.toml`. Run `ruff check .` before every change.

## 1. Structure

- R-1.1 A feature MUST be a self-contained package. It owns its operators, panels, properties and helpers. Removing the package and its registry entry MUST leave the rest of the add-on working.
- R-1.2 A feature MUST NOT import another feature except through that feature's `__all__`.
- R-1.3 Code needed by 2+ features MUST move to the shared packages. Group shared helpers by what they act on (armatures, objects, collections), not by who calls them.
- R-1.4 Every package `__init__.py` MUST have a one-line docstring. A feature's `__init__.py` MUST also define `__all__` (its public API), `register()` and `unregister()`.
- R-1.5 Put each kind of code in a file named after it: `operators`, `panels`, `properties`. The name states the type, so file names MUST NOT carry `_ot`, `_pt` or `_prop` suffixes.
- R-1.6 Files SHOULD stay under ~300 lines. Split an oversized `operators` file into an `operators` package with one operator per file.
- R-1.7 Files and names that are not public API start with `_`.
- R-1.8 Data-driven content (templates, presets, definitions) SHOULD be editable data, not logic buried in operators.

## 2. Registration and Cleanup

- R-2.1 A feature's `register()` and `unregister()` MUST go through one ordered tuple of modules: register in order, unregister in reverse.
- R-2.2 `unregister()` MUST remove everything the feature added: operators, panels, menus, property groups, `Scene`/`Object`/`Armature` pointer properties, handlers, timers, keymaps and icons.
- R-2.3 `register()` and `unregister()` MUST be idempotent. Calling either twice MUST NOT raise.
- R-2.4 Imports MUST be side-effect free. Nothing registers or runs Blender code at import time.
- R-2.5 Data a feature stores in `.blend` files MUST survive an unregister and register. Unregistering MUST NOT delete user data.
- R-2.6 Disabling and re-enabling the add-on in Blender MUST be tested before merging.
- R-2.7 Every Blender class MUST be registered with an explicit `bpy.utils.register_class(...)` in the `register()` of the file that defines it, and removed in that file's `unregister()` in reverse order. Auto-discovery of Blender classes is forbidden.
- R-2.8 Within a feature, register property groups first, then operators, then panels. Unregister in reverse.

## 3. Naming

| Item | Convention | Example |
|------|-----------|---------|
| Operator `bl_idname` | `aether.<feature>_<action>` | `aether.example_do_thing` |
| Operator class | `AETHER_OT_<feature>_<action>` | `AETHER_OT_example_do_thing` |
| Panel class and `bl_idname` | `AETHER_PT_<feature>_<name>` | `AETHER_PT_example_main` |
| Menu class and `bl_idname` | `AETHER_MT_<feature>_<name>` | `AETHER_MT_example_presets` |
| Property group class | `AETHER_PG_<feature>_<name>` | `AETHER_PG_example_settings` |
| Scene/Object/Armature property | `aether_<name>` | `object.aether_rig` |
| Function, variable | `lower_snake_case` | `get_bone_chain` |
| Constant | `ALL_CAPS` | `DEFAULT_BONE_SIZE` |
| Private helper | leading `_` | `_collect_bones` |

- R-3.1 `<feature>` in IDs and class names MUST equal the feature's package name.
- R-3.2 `bl_idname` MUST be lowercase with exactly one dot.
- R-3.3 A panel's `bl_idname` MUST equal its class name.
- R-3.4 Blender class names follow the table, not CapWords. Ruff ignores N801 for that reason.
- R-3.5 Operator IDs are public API for users' scripts. Renaming one MUST be listed in the changelog.

## 4. Operators

- R-4.1 An operator MUST define `bl_idname`, `bl_label` and `bl_description`. It MUST NOT have a docstring.
- R-4.2 An operator MUST only contain `poll`, `invoke`/`execute`/`modal`, `draw` and user reporting. Logic MUST live in helpers or the feature's own modules.
- R-4.3 MUST report through `self.report` with a clear, actionable message.
- R-4.4 Operators that change data SHOULD include `"UNDO"` in `bl_options`.
- R-4.5 Every operator property MUST have `name` and `description`. Hidden helper properties (for example `filter_glob`) are exempt.
- R-4.6 An operator that changes mode, selection, cursor or the active object MUST restore it on exit, including on error.

## 5. Type Hints

- R-5.1 Every function MUST type all arguments and the return value.
- R-5.2 MUST use Blender types (`bpy.types.Object`, `bpy.types.Context`, ...). `Any` only when no better type exists.
- R-5.3 `execute`, `invoke` and `modal` return `set[str]`. `poll` returns `bool` (wrap truthy values in `bool()`).

## 6. Documentation in Code

- R-6.1 Each module MUST start with a one-line docstring.
- R-6.2 Each public function MUST have a one-line imperative docstring:
  ```python
  def exist(armature: bpy.types.Object, name: str) -> bool:
      """Return True if the armature has a bone with this name."""
  ```
- R-6.3 `Args:`, `Returns:`, `Raises:` sections are only allowed when name and types do not explain the function.
- R-6.4 Private `_helpers` need no docstring when name and types are clear.
- R-6.5 Properties MUST have `description=`. Operators use `bl_description`. These are the UI tooltips.
- R-6.6 Explanations longer than a few lines MUST go on the wiki, not in code.
- R-6.7 Comments explain *why*, never *what*.

## 7. Utilities

- R-7.1 Name functions without the module name: `armature.get_pose_bone()`, not `armature.armature_get_pose_bone()`.
- R-7.2 Utilities that change mode MUST restore the original mode on exit, including on error.

## 8. Imports

- R-8.1 Order: standard library, third party (`bpy`, `mathutils`), local.
- R-8.2 MUST import modules, not names: `from . import bone`. A wildcard import is only allowed from a module that defines `__all__`, so it brings in exactly the public API.
- R-8.3 Inside a feature use relative imports. Another feature is reached only through its `__all__` (R-1.2).
- R-8.4 Import at the top of the file. Do not import inside functions unless it avoids a circular import, and then say so in a comment.

## 9. Console and Errors

- R-9.1 Console output MUST start with `[AetherBlend]`.
- R-9.2 Operators use `self.report`. Utilities use `print`.
- R-9.3 MUST NOT use a bare `except:`. Catch the specific exceptions.

## 10. Wiki Documentation

- R-10.1 The wiki is the user documentation. Its pages are kept in `docs/wiki/` with the exact wiki page names and are copied to the wiki repository.
- R-10.2 Every operator MUST be documented in the operator reference. An entry gives: ID, label, what it does, where it appears, requirements, parameters, errors and a Python call example.
- R-10.3 When an operator is added, renamed, removed or gets a new parameter, its wiki entry MUST change in the same change.
- R-10.4 Changes to this style guide are made in `docs/wiki/Style-Guide.md`.

## 11. Rig Modules

Rig module authoring has its own page: [Writing Rig Modules](Writing-Rig-Modules).

## 12. Checklist for New or Changed Code

- [ ] Lives in the right feature, with no cross-feature imports (R-1.2)
- [ ] `register()`/`unregister()` removes everything (R-2.2) and the add-on was toggled off and on (R-2.6)
- [ ] IDs and class names follow section 3
- [ ] Operators have `bl_label`, `bl_description` and described properties (R-4.1, R-4.5)
- [ ] Types on all functions (R-5.1); one-line docstrings on public ones (R-6.2)
- [ ] Wiki operator reference updated (R-10.3)
- [ ] `ruff check .` and `ruff format --check .` pass

## 13. Example

An operator, in a feature's operators file:

```python
"""Operators that do example things."""

import bpy

from ...utils import armature as armature_utils


class AETHER_OT_example_do_thing(bpy.types.Operator):
    bl_idname = "aether.example_do_thing"
    bl_label = "Do Thing"
    bl_description = "Hide every bone in the active armature that matches the prefix"
    bl_options = {"REGISTER", "UNDO"}

    prefix: bpy.props.StringProperty(
        name="Prefix",
        description="Bones whose name starts with this text are hidden",
        default="tmp_",
    )  # type: ignore

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        obj = context.active_object
        return obj is not None and obj.type == "ARMATURE"

    def execute(self, context: bpy.types.Context) -> set[str]:
        armature = context.active_object
        count = armature_utils.hide_bones_with_prefix(armature, self.prefix)
        if count == 0:
            self.report({"WARNING"}, f"No bones start with '{self.prefix}'")
            return {"CANCELLED"}
        self.report({"INFO"}, f"Hid {count} bones")
        return {"FINISHED"}


def register() -> None:
    """Register this module's classes."""
    bpy.utils.register_class(AETHER_OT_example_do_thing)


def unregister() -> None:
    """Unregister this module's classes."""
    bpy.utils.unregister_class(AETHER_OT_example_do_thing)
```
