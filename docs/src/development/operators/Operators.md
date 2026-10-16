---
title: Operator Reference
group: Development
order: 100
summary: Every operator, its parameters and what it does.
---
# Operators

Every AetherBlend action is a Blender operator. You can run it from the UI or from Python.

## Calling an Operator

```python
import bpy

bpy.ops.aether.rig_generator_generate_full()
bpy.ops.aether.rig_edit_set_inherit_scale(inherit_scale="FIX_SHEAR")
```

Operator IDs follow `aether.<feature>_<action>`. Operators that open a file dialog (`INVOKE_DEFAULT`) can be run without a dialog by passing `"EXEC_DEFAULT"` and a `filepath`:

```python
bpy.ops.aether.import_export_import_character("EXEC_DEFAULT", filepath="C:/models/model.gltf")
```

An operator whose requirements are not met (see each page) raises `RuntimeError: ... poll() failed` when called from Python.

## Reference by Feature

| Feature | Page | Operators |
|---------|------|-----------|
| Import / Export | [Operators Import Export](Operators-Import-Export) | `import_character`, `export_pose`, `export_anim` |
| Rig Generator | [Operators Rig Generator](Operators-Rig-Generator) | `generate_full`, `generate_meta`, `clean_up`, `reset` |
| Rig Edit | [Operators Rig Edit](Operators-Rig-Edit) | `set_inherit_scale`, `delete_no_anim`, `remove_game_support` |
| Rig UI | [Operators Rig UI](Operators-Rig-UI) | `solo_collections`, `eyelid_edit_start`, `eyelid_edit_end` |
| Shaders | [Operators Shaders](Operators-Shaders) | `iris`, `limbal`, `ffgear`, `meddle` |
| Preferences | [Operators Preferences](Operators-Preferences) | `toggle_feature_set` |

Full IDs are `aether.<feature>_<action>`, for example `aether.shaders_iris`.

## Where to Find Them

The add-on has a sidebar tab named **AetherBlend** in the 3D Viewport (`N` panel). It shows one workflow tab at a time:

| Tab | Purpose |
|-----|---------|
| Import / Export | bring a model in, export poses and animations |
| Generate | create and edit the rig, set up shaders |
| Rig Layers | show and solo bone collections |
| Rig UI | rig-specific controls |

The same panels can also be shown in the Properties editor **Tool** tab (see [[Operators Preferences]]).

## Tips

- Most operators support Undo (`Ctrl+Z`).
- Messages appear in the status bar. Longer errors are in the Blender system console.
- Operator parameters shown in the tables are the Python keyword arguments.
