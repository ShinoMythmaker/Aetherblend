---
title: Shaders
group: Development
order: 270
sub: true
---
# Operators: Shaders

Back to [[Operators]].

**Where:** AetherBlend tab → Generate → *Shaders* panel (*Materials* and *Node Trees* sub-panels).

## `aether.shaders_iris`

**Label:** Set Up Iris (button text: AB Iris Shader)

Adds eye scaling to the character's iris materials.

**Parameters:** none. **Requirements:** armature whose meshes use an `iris.shpk` material (a Meddle import).

1. Adds the custom properties *Eye Scale X*, *Eye Scale Y* and *Pupil Scale* to the objects.
2. Appends the `[AetherBlend] Eye Scaling` node group.
3. Connects the group to the material and links the properties.

## `aether.shaders_limbal`

**Label:** Set Up Limbal Rings (button text: AB Limbal Shader)

Adds limbal rings to the iris. Same requirements as the iris shader. Appends `[AetherBlend] Limbal Rings`, replaces an existing group, and maps left/right ring intensity from the iris color alpha.

**Parameters:** none.

## `aether.shaders_meddle`

**Label:** Set Up Meddle  
**Requirements:** Meddle Tools add-on enabled.

| Name | Type | Description |
|------|------|-------------|
| `filepath` | string | Folder or file from the Meddle export |

Applies Meddle shaders to the materials of the armature's meshes. Opens a file dialog at the *Default Meddle import path*.

## `aether.shaders_ffgear`

**Label:** Set Up FFGEAR  
**Requirements:** FFGear add-on enabled.

| Name | Type | Description |
|------|------|-------------|
| `filepath` | string | Folder or file from the export |

Applies FFGear gear shaders to the armature's meshes. Opens a file dialog like the Meddle operator.

Both operators reselect only the armature afterwards.
