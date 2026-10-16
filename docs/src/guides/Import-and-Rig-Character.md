---
title: Import and Rig a Character
group: Guides
order: 20
summary: Import a character model and generate its AetherBlend rig.
---
# Import and Rig a Character

## Before you begin

- Install AetherBlend in Blender {{blender_min}} or newer.
- Enable Blender's bundled **Rigify** add-on before rig generation.
- Have a character model in `.gltf`, `.glb` or `.fbx` format. Meddle Tools and
  FFGear are optional integrations for their respective shader imports.

## Steps

1. In the 3D Viewport sidebar (`N`), open **AetherBlend → Import/Export** and
   choose **FFXIV Character**. Select the model file and import it. The imported
   armature becomes active when one is present; otherwise, select the
   character's armature in the viewport.
2. Open **AetherBlend → Generate → Create Rig**. Choose the template and
   colorset for the active armature.
3. Select **Generate Rig** and wait for generation to finish.
4. Pose the generated armature from the **Rig Layers** and **Rig UI** tabs.

## Result

The active armature is in Pose Mode with its generated rig and original source
bones retained in the `Original` collection. The import step accepts `.gltf`,
`.glb` and `.fbx`; rig generation uses the selected template and colorset.
