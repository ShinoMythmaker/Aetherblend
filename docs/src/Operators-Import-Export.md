# Operators: Import / Export

Back to [[Operators]].

## `aether.import_export_import_character`

**Label:** Import Character (button text: FFXIV Character)  
**Where:** AetherBlend tab → Import / Export → *Import* panel, and File → Import menu.

Imports an FFXIV character model (exported by Meddle or similar) and prepares it for rigging. A file dialog opens first.

**Requirements:** file ending in `.gltf`, `.glb` or `.fbx`. The Meddle Tools and FFGear add-ons are optional; their shader options are switched off automatically in the dialog when those add-ons are not enabled. The dialog opens in the *Default Meddle import path* from the preferences.

### Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `filepath` | string | | Path of the model file |
| `s_pack_images` | bool | True | Pack the textures into the .blend file |
| `s_merge_vertices` | bool | False | Merge duplicate vertices on import |
| `s_import_collection` | bool | True | Put the import in a new `Model_Import` collection |
| `s_merge_skin` | bool | True | Merge meshes by the `skin` material name |
| `s_merge_by_material` | bool | True | Join meshes that share a material |
| `s_import_with_meddle_shaders` | bool | True | Apply Meddle shaders to the materials |
| `s_import_ab_iris_shader` | bool | True | Add the AetherBlend eye scaling shader (needs Meddle shaders) |
| `s_import_ab_limbal_shader` | bool | True | Add the AetherBlend limbal ring shader (needs Meddle shaders) |
| `s_import_with_ffgear_shaders` | bool | True | Apply FFGear shaders to gear materials |
| `s_disable_bone_shape` | bool | True | Hide the bone shape display |
| `s_apply_pose_track` | bool | False | Apply the pose stored in the file as the current pose |
| `use_bone_axis_conversion` | bool | True | Convert bone axes to the FFXIV convention |
| `primary_bone_axis` | enum | `X` | Bone primary axis (`X`, `Y`, `Z`, `-X`, `-Y`, `-Z`) |
| `secondary_bone_axis` | enum | `Y` | Bone secondary axis (same values) |

### What it does

1. Checks the file extension.
2. Imports the model.
3. Creates the `Model_Import` collection if requested.
4. Merges meshes by material and merges the skin.
5. Imports the Meddle and FFGear shaders if requested.
6. Finds the armature. Applies the pose track if requested, otherwise clears animation data and resets the pose.
7. Converts bone axes.
8. Puts all bones in the `Original` bone collection. The rig generator uses this collection as the source of truth.
9. Selects only the armature.
10. Runs the iris and limbal shader operators when Meddle shaders were imported.
11. Switches to the Generate tab if *Auto navigate tabs* is on.

**Errors:** unsupported file type; no armature in the imported file.

```python
bpy.ops.aether.import_export_import_character("EXEC_DEFAULT", filepath="C:/models/hyur.gltf", s_merge_vertices=True)
```

## `aether.import_export_export_pose`

**Label:** Export to Pose File  
**Where:** Import / Export tab → *Export* panel, and File → Export → AB Pose.

Writes the current pose of the active armature to a `.pose` file readable by FFXIV pose tools.

**Requirements:** active armature object with an `Original` bone collection.

### Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `filepath` | string | `.blend` name + `.pose` | Output path (set by the dialog) |
| `use_pose_axis_conversion` | bool | True | Convert axes to the FFXIV convention |
| `pose_primary_axis` | enum | `X` | Primary axis for the conversion |
| `pose_secondary_axis` | enum | `Y` | Secondary axis for the conversion |
| `pose_author` | string | | Author name stored in the file |
| `pose_description` | string | | Description stored in the file |
| `pose_version` | string | `1.0.0` | Version stored in the file |
| `pose_tags` | string | | Comma-separated tags |
| `include_preview_image` | bool | True | Embed a preview image |
| `preview_source` | enum | `AUTO_VIEWPORT` | `AUTO_VIEWPORT`, `RENDER_RESULT`, `BLENDER_IMAGE`, `EXTERNAL_FILE` |
| `preview_image_name` | string | | Blender image used for `BLENDER_IMAGE` |
| `preview_external_path` | string | | Image file used for `EXTERNAL_FILE` |

### What it does

For every bone of the `Original` collection it writes position, rotation (quaternion) and scale, computed from the bone's world matrix, the axis correction and a -90° rotation around X. The `.001` style suffixes are removed from bone names. The file is JSON containing `Author`, `Description`, `Version`, `Tags`, `FileExtension`, `TypeName` (`Aetherblend Pose`), `FileVersion` (2) and `Bones`. The preview image is embedded as Base64. If a Render Result exists, it is preselected as the preview.

**Errors:** no active armature; no `Original` collection; preview image not found.

```python
bpy.ops.aether.import_export_export_pose("EXEC_DEFAULT", filepath="C:/poses/wave.pose", pose_author="Me")
```

## `aether.import_export_export_anim`

**Label:** Export Animation  
**Where:** Import / Export tab → *Export* panel, and File → Export → AB Animation.

Exports an action of the active armature as FBX or GLB for use in the game tools.

**Requirements:** active armature object.

### Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `filepath` | string | action name | Output path (set by the dialog) |
| `export_format` | enum | `FBX` | `FBX` or `GLB` |
| `selected_action` | enum | active action | Action to export |
| `pose_primary_axis` | enum | `X` | Primary bone axis |
| `pose_secondary_axis` | enum | `Y` | Secondary bone axis |

### What it does

1. Temporarily assigns the selected action to the armature.
2. Exports FBX with baked animation, no leaf bones and deform bones only.
3. For GLB, exports a temporary FBX, imports it again and exports it as GLB (Y-up, active actions, no materials). The temporary import and file are removed.
4. Restores the original action, selection and active object.
5. Shows a success popup.

```python
bpy.ops.aether.import_export_export_anim("EXEC_DEFAULT", filepath="C:/anims/run.fbx", export_format="FBX")
```
