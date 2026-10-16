---
title: Rig Edit
group: Development
order: 240
sub: true
---
# Operators: Rig Edit

Back to [[Operators]].

**Where:** AetherBlend tab → Generate → *Rig Manipulation* panel.  
**Common requirements:** the active armature has a generated rig (`aether_rig.rigified`).

## `aether.rig_edit_set_inherit_scale`

**Label:** Set Inherit Scale

Sets how the `LINK` bones inherit scale from their parents. These bones connect the generated rig to the original game skeleton.

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `inherit_scale` | enum | stored value | `FULL`, `FIX_SHEAR` (Aligned), `AVERAGE`, `NONE`, `NONE_LEGACY` (None, legacy) |

**What it does:** requires the `LINK` bone collection, stores the choice on the rig so a regenerate keeps it, and applies it to every bone in the collection. Reports how many bones changed. In the panel it is a drop-down.

```python
bpy.ops.aether.rig_edit_set_inherit_scale(inherit_scale="FIX_SHEAR")
```

## `aether.rig_edit_delete_no_anim`

**Label:** Delete NoAnim

Removes every bone whose name contains `noanim`. These helper bones are not needed for animation and are removed to keep the export clean.

**Parameters:** none. Needs an armature. The original mode is restored afterwards.

## `aether.rig_edit_remove_game_support`

**Label:** Remove Game Support (button text: Convert)

Converts the generated rig into a standalone Rigify rig without the game skeleton. **This cannot be undone**, so a confirmation dialog appears.

**Parameters:** none.

### What it does

1. Finds which deform bone corresponds to which Rigify bone through the `AB-LINK` Copy Transforms constraints.
2. Renames the meshes' vertex groups to the Rigify DEF bone names.
3. In Edit mode deletes the original bones and their `LINK-` bones.
4. Re-parents any remaining deform children.
5. Sets `converted` on the rig.

Use it when you only want to animate in Blender and do not need to export back to the game. Export a `.blend` copy first.
