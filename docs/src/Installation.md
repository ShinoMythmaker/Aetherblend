---
title: Installation
group: Guides
order: 10
summary: Requirements and how to install the add-on.
---
## Requirements 
- Blender {{blender_min}} or newer
- [Meddle](https://github.com/PassiveModding/Meddle) and [MeddleTools](https://github.com/PassiveModding/MeddleTools)
- Rigify
&nbsp;

**Note: Rigify ships with Blender but may need to be enabled manually**

## Installation
You can install AetherBlend with drag and drop, manually, or with Blender's repository feature:

### Drag and drop
The quickest way. Drag a button below into an open Blender window.

1. Drag the **AetherBlend** button into Blender. The first time, Blender asks to add the AetherBlend repository, confirm it.
2. Drag the **same button a second time** to install the add-on from that repository.
3. Meddle Tools and FFGear come from the same repository, so once it is added they need only **one drop each**.

<div class="drop-stack">
  <div class="drop-row required">
    <span class="tag">Required</span>
    <a class="drop-link large" href="{{aetherblend_link}}" draggable="true">Drag AetherBlend into Blender</a>
    <p>The add-on itself. Drop it <strong>twice</strong>: first to add the repository, then to install.</p>
  </div>
  <div class="drop-row recommended">
    <span class="tag">Recommended</span>
    <a class="drop-link subtle" href="{{meddle_link}}" draggable="true">Drag Meddle Tools into Blender</a>
    <p>Needed to import characters with their materials and shaders. You can skip it if you only use AetherBlend's rigging tools.</p>
  </div>
  <div class="drop-row optional">
    <span class="tag">Optional</span>
    <a class="drop-link subtle" href="{{ffgear_link}}" draggable="true">Drag FFGear into Blender</a>
    <p>Extra gear shaders. Not needed for AetherBlend to work.</p>
  </div>
</div>

All three buttons use the shared [FFXIV Blender Plugins](https://github.com/ShinoMythmaker/FFXIV-Blender-Plugins) repository. Because it is a repository, Blender keeps the installed add-ons updated afterwards.

If dragging does nothing, use one of the methods below.

### Repository feature
1. In Blender's preferences menu, select the "Get Extensions" tab
2. Select the repositories drop-down-menu in the top right of the window
3. Select "Add Remote Repository"
4. Paste the following URL into the required repository field:

    ```
    https://raw.githubusercontent.com/ShinoMythmaker/FFXIV-Blender-Plugins/refs/heads/main/repo.json
    ```

5. Select **Check for Updates on Startup**.
6. Select **Create**.
7. Find AetherBlend in the list of available add-ons and install it

Using this feature will allow Blender to automatically keep AetherBlend up to date.

<img width="532" height="286" alt="image" src="https://github.com/user-attachments/assets/84ce6f77-33b8-4cec-a68f-30572fd5bc90" />

### Manual
1. Download the newest .zip from the releases [page](https://github.com/ShinoMythmaker/Aetherblend/releases)
2. Open your preferences menu in Blender and navigate to the add-ons section
3. From the dropdown in the top right of the window, select "Install from Disk" and navigate to your downloaded release of AetherBlend

&nbsp;
