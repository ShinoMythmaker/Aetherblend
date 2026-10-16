---
title: Contributing
group: Development
order: 190
summary: Setup, guidelines and release in one short page.
---
# Contributing

Everything you need to work on AetherBlend on one page. Docs work has its own page: [Working on the Docs](Working-On-The-Docs).

## Setup

You need Blender 5.2+, Git, Python 3.11+ and [VS Code](https://code.visualstudio.com/) with the Python extension.

```powershell
git clone https://github.com/ShinoMythmaker/Aetherblend.git
cd Aetherblend
```

Use your fork's URL if you work from a fork. Then, from the repository root:

```powershell
python -m venv .venv; .venv\Scripts\python.exe -m pip install --upgrade pip ruff tomli-w markdown pygments fake-bpy-module; .venv\Scripts\python.exe get_dependencies.py
```

This creates the virtual environment, installs the tools and downloads the bundled wheels into `wheels/` (not committed). Run `get_dependencies.py` again if `wheels/` is missing or you change `dependencies` in `blender_manifest.toml`.

In VS Code:

1. Run **Python: Select Interpreter** and pick `.venv`.
2. `fake-bpy-module` gives you `bpy` autocompletion. If it doesn't match your Blender, install the matching version, for example `fake-bpy-module-5.2`.
3. Install the [Blender Development](https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development) extension. Run **Blender: Build and Start** to open Blender with the add-on loaded, and **Blender: Reload Addon** after changes. You can attach the debugger to that session.

## Guidelines

These are guidelines, not hard rules. A pull request that doesn't follow all of them can still be accepted, but it is more likely to be if it does.

- **New features are standalone** and can be enabled and disabled in the add-on preferences. They don't import other features. Shared code goes in `utils/` or `ui/`.
- **Edited features keep working** and can still be enabled and disabled.
- **Follow the [Style Guide](Style-Guide)** as well as you can.
- Keep pull requests small and focused. Keep operators thin.
- Don't rename operator IDs, `.blend` property names, preference keys or the template format without asking. User data depends on them.
- Changed an operator? Update its page in `docs/src/operators/` and rebuild the docs.

Before you open the pull request:

```powershell
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe -m compileall -q .
```

Then test in Blender: run what you changed, toggle the feature off and on in preferences, and check the console for errors. Mention in the pull request how you tested.

## Release

Only the maintainer releases the main repository. This is for forks.

1. Update `blender_manifest.toml`: set the new `version` and, if needed, `blender_version_min`.
2. Optionally run `docs\build.py` to update the docs now. It also runs automatically after the release.
3. Push the change, then create and push a version tag like `v0.3.8` on the default branch.
4. The `draft-release-with-zip` workflow runs on the tag. It downloads the wheels, zips the repository and creates a draft GitHub release.
5. Review and publish the release. The `Update repo.json on Release` workflow then rewrites `repo.json` to point at the new release and its hash, and pushes it to the default branch. (`Manual Update repo.json` does the same on demand.)
6. When that finishes, the `Rebuild docs after release` workflow runs `docs/build.py` and pushes the updated `README.md` and `docs/`. It also runs daily to pick up new Meddle Tools and FFGear releases.

Don't edit `repo.json` by hand.

Files listed in `release_ignore` are left out of the zip (dot files, `docs/`, repository text files, tooling and `__pycache__`). It holds one `zip` pattern per line and no comments. `wheels/` is kept on purpose, because the manifest needs it.

Forks must change `REPO_URL` and `MASTER_REPO_JSON` in `docs/build.py`, and the URLs in `repo.json` and `blender_manifest.toml`.
