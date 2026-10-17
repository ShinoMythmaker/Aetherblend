---
title: Style Guide
group: Development
order: 120
summary: A few conventions to help your code feel at home.
---
# Style Guide

Welcome! Keep changes focused and code easy to read. These are the essentials;
Ruff handles the formatting details.

## 1. Feature layout

**R-1.1** Keep each feature self-contained. A typical feature looks like this;
only add files you need:

```text
features/my_feature/
    __init__.py     # Public exports, register() and unregister()
    operators.py   # Blender actions and user reporting
    panels.py      # UI layout
    properties.py  # Blender property definitions
```

**R-1.2** Keep feature logic beside these files in purpose-named modules.
Code needed by multiple features goes in `utils/` or `ui/`.
**R-1.3** Prefer module imports and relative imports within a feature.
**R-1.4** Use another feature only through its `__all__` public API.

## Naming

**R-2.1** Use the feature's package name in Blender IDs and class names:

| Kind | Example |
|------|---------|
| Operator ID | `aether.my_feature_do_thing` |
| Operator class | `AETHER_OT_my_feature_do_thing` |
| Panel / menu / property group | `AETHER_PT_…` / `AETHER_MT_…` / `AETHER_PG_…` |
| Function or variable | `lower_snake_case` |
| Constant / private helper | `ALL_CAPS` / `_helper` |

**R-2.2** A panel's `bl_idname` matches its class name.
**R-2.3** Ask before renaming public IDs or saved properties; existing files and scripts rely on them.

## Errors and output

**R-3.1** Start console messages with `[AetherBlend]`.
**R-3.2** Use `self.report({"ERROR"}, "What went wrong and what to do next")`
in operators and `print("[AetherBlend] ...")` in utilities.
**R-3.3** Catch specific exceptions and make failures visible rather than silently continuing.


Follow the [Development Guide](Development-Guide) for checks and Blender testing.
