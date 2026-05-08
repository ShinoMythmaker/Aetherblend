## How To Help
The best way to help AetherBlend right now is by sharing feedback and reporting bugs.

- Submit feedback or bug reports on GitHub.
- Share feedback or report bugs in our Discord community.

Developers are also welcome to contribute directly by opening a pull request.

## Dependency Sync Workflow
To make a fresh fork/clone work locally, contributors must run the dependency bundling script from the repository root.

This is required because the [wheels](wheels) folder is not committed to the repository.

Run this from the repository root:

```bash
python get_dependencies.py
```

What this does:
- Downloads the currently selected dependency wheels into [wheels](wheels)
- Rebuilds the `wheels` list in [blender_manifest.toml](blender_manifest.toml)

When to run it:
- Immediately after cloning/forking the project
- Any time [wheels](wheels) is missing or stale
- After changing `dependencies` in [blender_manifest.toml](blender_manifest.toml)

This helps ensure local testing uses the same bundled artifacts as the release package.

## Direct Support
You can directly support Mythmaker Studio on Patreon.
Supporters in the highest tier (`Mythmaker`) are listed below.

## Mythmaker Supporters
- Zed
- PancakePapi
- Pizzadabbin

## Acknowledgements
💖 A heartfelt thank you to [Oats](https://github.com/ExplosiveOats), my official Co-Dev. Working with her on developing and maintaining AetherBlend has been an absolute privilege. She played a crucial role in getting our beta release across the finish line and continues to go above and beyond helping our community members on Discord every single day. I genuinely couldn't have done this without her, and I'm incredibly excited for everything we'll accomplish together!

💖 [Zed](https://x.com/RoseHikari24) and [CC](https://x.com/CC_VibesXIV), two of my very closest friends that let me yap for countless hours about issues with this project and kept motivating me to go on. Really without them I think I wouldnt have finished it, thank you!

💖 [PassiveModding](https://github.com/PassiveModding) - Thanks for [Meddle](https://github.com/PassiveModding/Meddle), and [Meddle Tools](https://github.com/PassiveModding/MeddleTools), while not being a requirement, these tools brought me back to actually bringing my characters into Blender and making me want to create a better Animation solution. 

💖 [sleepybunny](https://github.com/sleepybnuuy) for providing an excellent base for the C+ application with [bustomize](https://github.com/sleepybnuuy/bustomize)

💖 Ofcourse everyone that showed interest in not only AetherBlend but also [Mektools](https://github.com/MekuMaki/Mektools) and [Mythtools](https://github.com/ShinoMythmaker/Myth-Tools) aswell as all my supporters on Patreon. I have pushed content creation away just to work on these other tools, yet you kept supporting me and im more then thankfull for that!
