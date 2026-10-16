---
title: Rig UI
group: Development
order: 140
sub: true
---
# Operators: Rig UI

Back to [[Operators]].

These operators help while posing a generated rig.

## `aether.rig_ui_solo_collections`

**Label:** Solo Selected (the button reads *Unsolo All* while a solo is active)  
**Where:** Rig Layers tab → *Rig Layers* panel. Pose mode only.

Shows only the bone collections that contain the selected bones.

**Parameters:** none.

- If any collection is already soloed, it unsolos all of them.
- Otherwise it solos the collections of the selected pose bones.
- Cancels if no bones are selected.

## `aether.rig_ui_eyelid_edit_start`

**Label:** Start Editing Eye Lid Offset (button text: Enter Eye Lid Edit Mode)  
**Where:** Rig UI tab, eyes section.

Unlocks the six eyelid anchor bones so you can move them to fit the character's eyes.

**Parameters:** none.

1. Sets `eye_lid_edit_mode` on the rig.
2. Unsolos all collections and solos `Eyes_Anchors`.
3. Unlocks location, rotation and scale on the `lid.anchor.B.[LR].00[123]` bones.

## `aether.rig_ui_eyelid_edit_end`

**Label:** End Editing Eye Lid Offset (button text: Exit Eye Lid Edit Mode)

Reverses the start operator: clears the mode, removes the solo and locks the anchor bones again.

**Parameters:** none.
