<br>
<p align="center">
  <img height="90" align="middle" alt="AetherBlend" src="assets/brand/Aether Blend Logo-min.png" />&nbsp;&nbsp;
  <a href="https://shinomythmaker.github.io/Aetherblend/"><img width="180" height="52" align="middle" alt="Visit our website" src="assets/brand/btn-website.svg" /></a>
</p>
<p align="center">
    <img src="https://img.shields.io/github/v/release/ShinoMythmaker/Aetherblend?label=Version&color=blue">
    <img src="https://img.shields.io/badge/Blender-5.2.0%2B-orange">
    <a href="https://www.paypal.com/donate/?hosted_button_id=VVSSL3GDRSBNC"><img alt="Sponsor Badge" src="https://img.shields.io/badge/MythmakerStudio-Sponsor-pink?style=flat"></a>
</p>
&nbsp;


<p align="center">
AetherBlend is a toolkit for FFXIV modding and creative work in Blender, built with game compatibility in mind.
Currently in beta; tools and workflows are still being refined.
</p>

<p align="center">
  <img width="100%" alt="AetherBlend showcase" src="assets/demo/showcase_low.jpg" />
</p>

&nbsp;

<p align="center">
  <a href="https://shinomythmaker.github.io/Aetherblend/index.html"><img width="240" alt="Installation and Guides" src="assets/brand/btn-installation.svg" /></a>&nbsp;&nbsp;&nbsp;
  <a href="https://github.com/ShinoMythmaker/Aetherblend/issues"><img width="240" alt="Report a Bug" src="assets/brand/btn-bug.svg" /></a>&nbsp;&nbsp;&nbsp;
  <a href="https://discord.gg/NEF7TdXGqH"><img width="240" alt="Discord" src="assets/brand/btn-discord.svg" /></a>
</p>
&nbsp;

## About AetherBlend

AetherBlend started as an IK rig generator and has grown into a broader toolkit for working with FFXIV in Blender. It supports both game modding and creative work in Blender, with game compatibility at the core of its design.

The add-on is still in beta, and its tools and workflows are being refined.

## A rig built around your character

AetherBlend builds on Rigify, with substantial changes for FFXIV's armature and additional controls. It generates a metarig fitted to your character's proportions and custom scaling.

Rather than replacing the game's armature, AetherBlend links its original bones to the generated control rig. This preserves game compatibility while giving you Blender controls for posing and animation.

<table>
  <tr>
    <th align="center">IK controls</th>
    <th align="center">Heel controls</th>
    <th align="center">Spline controls</th>
  </tr>
  <tr>
    <td width="32%" align="center"><img src="docs/assets/img/ik_demo.gif" width="260" alt="IK controls demonstration" /></td>
    <td width="32%" align="center"><img src="docs/assets/img/heels_demo.gif" width="260" alt="Heel controls demonstration" /></td>
    <td width="32%" align="center"><img src="docs/assets/img/spline_demo.gif" width="260" alt="Spline controls demonstration" /></td>
  </tr>
</table>

### Eye and iris controls

The gaze control moves both the eyes and surrounding facial bones for more expressive poses. Custom iris shaders bring FFXIV's iris controls into Blender.

<p align="center">
  <img src="docs/assets/img/eyes_demo.gif" width="600" alt="Gaze and iris controls demonstration" />
</p>

### Back to GPose

Export poses for use in GPose, with thumbnail support to help identify them later.

<p align="center">
  <img src="docs/assets/img/gpose_demo.gif" width="420" alt="GPose export with thumbnail support demonstration" />
</p>

## Road to 1.0

The feature scope for 1.0. Available tools are still being refined during beta.

### Available in beta

- [x] Character import
- [x] C+ application
- [x] Full rig generation
- [x] GPose export
- [x] Animation export
- [x] VFX toolkits

### Still to come

- [ ] Animation and GPose import
- [ ] Action Library
- [ ] C+ export
- [ ] AetherBridge: seamless actor streaming between FFXIV and Blender

&nbsp;


## Acknowledgements
- A special thank you to [Oats](https://github.com/ExplosiveOats), co-developer, for the care and dedication she brings to AetherBlend and its community. I'm deeply grateful she joined the team and that we get to build this project together.

- [PassiveModding](https://github.com/PassiveModding), creator of [Meddle](https://github.com/PassiveModding/Meddle) and [Meddle Tools](https://github.com/PassiveModding/MeddleTools), for tools that helped inspire AetherBlend.

- [sleepybunny](https://github.com/sleepybnuuy), whose [bustomize](https://github.com/sleepybnuuy/bustomize) provided the foundation for AetherBlend's C+ application.

- The AetherBlend, [Mektools](https://github.com/MekuMaki/Mektools) and [Mythtools](https://github.com/ShinoMythmaker/Myth-Tools) communities, and my Patreon supporters, for their continued support.

---
&nbsp; 
