---
title: Getting Started
group: Guides
order: 20
summary: Import a character and generate your first rig.
aliases: How-to-AetherBlend-(Alpha)
---
## How to use Aetherblend

This section will serve as a guide to AetherBlend's basic features and their usage.

### Importing your character:

There are currently two methods to import your character (or non-player model) using AetherBlend. You can:

1. Open the N-panel and select 'Import Character', then navigate to your Meddle export and select the relevant .gltf file
2. Navigate to File > Import > FFXIV Character (Meddle), then head to your Meddle export and select the relevant .gltf file

&nbsp;

The import window will contain a couple of options you may want to enable or disable based on preference:
  
**Shaders: Import with Meddle**

This setting simply enables or disables using Meddle's shader setup for materials such as skin, hair and gear.

**Armature: Apply Pose Track**

This setting controls whether or not to apply any character customisations such as height or bust. It is **not** designed to apply your C+, it is **only** to apply your vanilla scalings if you have exported in meddle using the "Reference pose + Scale" option.

**Bone Orientation:**

This menu allows you to enable changing the primary and secondary bone axes of the armature being imported. It is automatically set to work best with AetherBlend. Change this at your own risk, it is likely to result in complete failure of rig generation.

&nbsp;

### Generating the Rig

With your armature selected, simply select the "Generate Rig" option from the N-panel. The option for a separate meta exists for debugging purposes and can be safely ignored.
The dynamic template and AetherBlend colourset will be applied.

&nbsp; 

### The N-Panel

The N-panel contains important options like file export, rig generation and individual rig control options. It is divided into four tabs:

**1. Import/Export**

Here you will find options to import and export your character and their pose/animation.

**2. Generate**

The Generate tab allows you to generate a rig for your character. A dynamic and custom template are available by default as well as a choice of coloursets. For a more detailed explanation of the template system, go [here](The-Template-System). All operators are described in the [operator reference](Operators).
 

**3. Rig Layers**

Different control layers such as the left and right arms, legs and torso can be found here.

**4. Rig UI**

Contained here are any optional settings that contextually appear depending on what control you have selected. They allow you to switch between IK and FK controls, among other things.






