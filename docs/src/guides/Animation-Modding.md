---
title: Animation Modding
group: Guides
order: 40
summary: Take an animation from Blender into the game.
---
## Intro to Modding Animations using Aetherblend

This section of the wiki will serve to introduce you to the basic components of modding animations. You can find a video version of this guide [here.](https://www.youtube.com/watch?v=lNv0DwsQhmk)
I haven't had time to add images. Patience, friends.

### You will need the following game plug-ins:
* [Meddle](https://github.com/PassiveModding/Meddle)
* [VFX Editor](https://github.com/0ceal0t/Dalamud-VFXEditor)

### You will need the following Blender add-ons:
* [Aetherblend](https://github.com/ShinoMythmaker/Aetherblend)
* [Meddletools](https://github.com/PassiveModding/MeddleTools)
* Rigify (Included with Blender by default)

&nbsp;

Once you have all of the above installed and enabled, you will have to decide which armature you want to animate with. Most animations in Final Fantasy 14 use the Male Midlander armature (ID: c0101), so it is recommended to animate using it to avoid issues between races. However, it is ultimately up to you. This guide will be using the Female Miqo'te armature (ID: c0801), but the principle remains the same across all armatures and it is entirely viable to retarget your animations from your preferred armature to others.

To quickly find out which armature an animation uses, open VFX Editor and navigate to the 'pap' tab. Load an animation of your choice and open the parameters menu. Here you will find the model ID. In this case, it reads '801'. This corresponds to the Female Miqo'te armature (c0801). You can use this information to decide which armature you'd like to animate on.

### Exporting your model with Meddle

**It is recommended you choose to animate using a simple character model. Good choices would include plain clothing without excess cloth/armour, or simply using a nude model. Should you want to animate cloaks/capes/skirts/etc., make sure to use clothing that can give you a visual reference.**

This step should be quick and straightforward. Open Meddle and select your character, then select 'Export all Models'. Since you're animating, you do not need to use 'Reference Pose with Scale' or 'Pose'. Instead, make sure you use 'Reference Pose'. This option does not export any bone location, rotation or scale data. 

### Importing to Blender

Open the N-panel and navigate to Aetherblend. Select the 'Import Character' option, head to your Meddle export's file directory and select the relevant .gltf file. Since scaling is irrelevant, untick the 'Apply Pose Track' option from the import settings to the right of the file browser.

Once the importing process is complete, select the base armature. In Aetherblend's N-panel, generate your rig using the indicated button. You should now be able to animate your character in any way you want.

**If you want to find helpful resources on animating, a link will be provided at the bottom of this page.**

&nbsp;

### Getting your Animation into the Game

Once you are done with your animation and want to export, head to File > Export > FF14 Animation [.glb] or use the provided button in the N-panel. Ensure that your armature is the active object in your scene when doing this.

Head back into the game and open VFX Editor. In the 'pap' tab, select the animation you want to modify for both available fields. For example:
* Loaded Pap: Miqote F (Idle)
* Pap being Replaced: Miqote F (Idle)

Below, open the 'animation' tab and select the animation track. Some .pap files may have multiple tracks, so ensure you have selected the correct one. Now head into the 'motion' tab, select the option to replace the animation and import your custom one. This will open a small menu with a few options. It is a good idea to create an exclusion list here, the option of which is enabled by checking the 'Exclude Bones' box. 

In principle, exclusion lists prevent specified bones from having their animation data overwritten during this process.  
This is useful in cases where you have animated — for example — ear wiggle. You don't want to include this when replacing the animation of a Midlander and therefore add the ear bones to the exclusion list. If you do not know the exact names of the bones you're trying to exclude, you can use the 'Skip Bones Unanimated in Original Motion' option. The bones affected by this are marked in red.

**Keep in mind that this option references the currently loaded animation. If you have already imported an animation before, this option would not exclude the ear bones in the example above.**  

**It is generally a good idea to include n_root and n_throw in your exclusion list to prevent issues down the line.**

Once you are happy, proceed with the import. If done correctly, the change should reflect itself in the motion viewer. Lastly, make sure you have updated the .pap.

In the example case, the Miqo'te idle animation now uses the newly created animation.

### Completing your Animation Mod

Export your changes as a Penumbra mod file by selecting Export > Penumbra and then picking the files you have changed, i.e. Pap. Give your mod a name, author and version and you're done.

**This concludes the basic guide to animation modding using Aetherblend. There's obviously a lot more to this beyond what is covered here, but this guide only serves to teach you the basics. More advanced topics will be covered in separate tutorials down the line.**

**Thank you for taking the time to read this short guide. We hope it's been helpful! Feel free to let us know what kind of things you would like to see tutorials for in our [Discord](https://discord.gg/mythmaker) and share your creations! We look forward to seeing what you make.**

&nbsp;

* Helpful Resources for animating can be found here: [Fioh's Animation Station](https://discord.com/invite/H3pdmHAtrv)






