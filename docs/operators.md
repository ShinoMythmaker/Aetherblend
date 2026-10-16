# Operators

Every AetherBlend operator is called as `bpy.ops.aether.<feature>_<action>()`.
Update this file whenever an operator is added, renamed or removed.

## import_export

| Operator | Label | What it does | UI location |
|---|---|---|---|
| `aether.import_export_import_character` | Import Character | Imports a character model (glTF/FBX) and optionally merges meshes, packs images and applies Meddle or FFGear shaders. | 3D View > AetherBlend > Import |
| `aether.import_export_export_pose` | Export to Pose File | Writes the current armature pose to a `.pose` file, optionally with a preview image. | 3D View > AetherBlend > Export |
| `aether.import_export_export_anim` | Export Animation | Exports an action of the armature as an animation with axis conversion. | 3D View > AetherBlend > Export |

## rig_generator

| Operator | Label | What it does | UI location |
|---|---|---|---|
| `aether.rig_generator_generate_full` | Generate Full Rig | Generates the meta rig, the Rigify rig and links them in one step. | AetherBlend > Create Rig |
| `aether.rig_generator_generate_meta` | Generate Meta Rig | Generates only the meta rig, without running Rigify. | AetherBlend > Create Rig |
| `aether.rig_generator_clean_up` | Remove Rigify Rig | Removes the Rigify control bones and keeps the original animation data. | AetherBlend > Create Rig |
| `aether.rig_generator_reset` | Reset Original Rig | Resets the armature to its original state and removes animation data. | AetherBlend > Create Rig |

## rig_edit

Requires an armature with a generated rig.

| Operator | Label | What it does | UI location |
|---|---|---|---|
| `aether.rig_edit_set_inherit_scale` | Set Inherit Scale | Sets inherit scale on the bones in the LINK collection. | AetherBlend > Rig Manipulation |
| `aether.rig_edit_delete_no_anim` | Delete NoAnim | Deletes all bones carrying the `noanim` flag. | AetherBlend > Rig Manipulation |
| `aether.rig_edit_remove_game_support` | Remove Game Support | Strips game-specific data from the rig so it no longer works with the game or engine. | AetherBlend > Rig Manipulation |

## rig_ui

| Operator | Label | What it does | UI location |
|---|---|---|---|
| `aether.rig_ui_solo_collections` | Solo Selected | Toggles solo for the selected bone collections. | Rig Layers |
| `aether.rig_ui_eyelid_edit_start` | Start Editing Eye Lid Offset | Starts interactive editing of the eyelid control offset by dragging in the 3D view. | Rig UI |
| `aether.rig_ui_eyelid_edit_end` | End Editing Eye Lid Offset | Finishes eyelid editing and applies the changes. | Rig UI |

## shaders

| Operator | Label | What it does | UI location |
|---|---|---|---|
| `aether.shaders_iris` | Set Up Iris | Applies the Iris node group to iris materials. | Shaders > Node Trees |
| `aether.shaders_limbal` | Set Up Limbal Rings | Applies the Limbal Rings node group to iris materials. | Shaders > Node Trees |
| `aether.shaders_ffgear` | Set Up FFGEAR | Runs the FFGear shader import on meshes bound to the selected armature. | Shaders > Materials |
| `aether.shaders_meddle` | Set Up Meddle | Runs the Meddle shader import on meshes bound to the selected armature. | Shaders > Materials |

## Preferences

| Operator | Label | What it does | UI location |
|---|---|---|---|
| `aether.preferences_toggle_feature_set` | Toggle Feature Set | Enables or disables one feature set. | Add-on preferences |
