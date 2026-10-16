# Operators: Rig Generator

Back to [[Operators]].

**Where:** AetherBlend tab → Generate → *Create Rig* panel.  
**Common requirements:** a visible armature (or its meta rig) with a rig template assigned. The **Rigify** add-on must be enabled for the generate operators.

The generated rig keeps the original armature intact. The original bones are kept in the `Original` bone collection and Rigify bones are added next to them.

## `aether.rig_generator_generate_full`

**Label:** Generate Full Rig (the button reads *Generate Rig*, or *Regenerate* once a rig exists)

Builds the meta rig from the character template and then generates the final Rigify rig.

**Parameters:** none.

### What it does

1. If a meta rig is selected, switches to the source armature it belongs to.
2. Looks up the generator for the armature's template.
3. Builds the meta rig. Any existing generated rig is removed first (see `reset`).
4. Runs Rigify to generate the final rig.
5. Switches to the Rig Layers tab (if *Auto navigate tabs* is on), selects only the armature and enters Pose mode.

**Errors:** Rigify not enabled; no template; a rig module fails (the message names the module).

```python
bpy.ops.aether.rig_generator_generate_full()
```

## `aether.rig_generator_generate_meta`

**Label:** Generate Meta Rig

Builds only the meta rig and reveals it so you can adjust bones and Rigify settings before generating. Run `generate_full` afterwards to finish.

**Parameters:** none. Same requirements and errors as `generate_full`.

## `aether.rig_generator_clean_up`

**Label:** Remove Rigify Rig

Removes everything Rigify and AetherBlend added and returns the armature to its imported state.

**Parameters:** none. Does nothing if there is no `Original` collection.

### What it does

1. Deletes the meta rig and the generated rig UI script.
2. Removes the Rigify ID and drivers.
3. In Edit mode deletes every bone that is not in `Original`.
4. Removes bone collections that are no longer used.
5. Resets the `rigified` flag and clears Rigify types and constraints on the original bones.

Animation data is kept. Use `reset` to clear it too.

## `aether.rig_generator_reset`

**Label:** Reset Original Rig

Same as `clean_up`, then also clears animation data and returns to Object mode. Use it for a completely fresh start.

**Parameters:** none.

## Related Data

The `aether_rig` property on armatures stores: `template`, `rigified`, `converted`, `selected_colorset`, `link_inherit_scale`, `ui_flags` and `eye_lid_edit_mode`. See [[Writing Rig Modules]] for how templates are built.
