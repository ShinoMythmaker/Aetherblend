---
title: Development Guide
group: Development
order: 100
summary: Set up, make a focused change, validate it and prepare a pull request.
aliases: Contributing
---
# Development Guide

Use this checklist for a code change. For Doc and site work, see the
[Documenting Guide](Documenting-Guide); code conventions are in the
[Style Guide](Style-Guide).

## Set up

Install Git, Python 3.11+, Blender {{blender_min}}+ and
[VS Code](https://code.visualstudio.com/) with the Python extension.

```powershell
git clone https://github.com/ShinoMythmaker/Aetherblend.git
cd Aetherblend
git switch -c my-change
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip ruff tomli-w markdown pygments fake-bpy-module
.venv\Scripts\python.exe get_dependencies.py
```

Use your fork URL when appropriate. The final command downloads the add-on's
bundled wheels; rerun it when the manifest dependencies change.

In VS Code, select `.venv` with **Python: Select Interpreter**. For Blender
integration, install the [Blender Development extension](https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development)
and use **Blender: Build and Start** to launch the add-on.

## Make and validate a change

1. Read the relevant [Style Guide](Style-Guide) rules and make one focused
   change in the owning feature.
2. Run checks from the repository root:

```powershell
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe -m compileall -q .
```

3. In Blender, exercise the changed workflow, toggle the owning feature off and
   on, and check the system console. Static checks do not replace this test.

## Curate rig UI layouts

Choose **UI Layout** beside **Colorset** before generating or regenerating a rig.
Layouts live in `features/rig_generator/library/ui_layouts/`: copy a preset's
`BoneCollection` list and register it in that folder's `UI_LAYOUTS` dictionary.
List order controls left-to-right order; equal `row_index` values share a row,
and skipped row numbers add spacing. Set `title`, `color_set` and `visible`
there, not in rig modules. Empty collections remain part of the layout;
modules only assign bones to collections and provide their own UI flags.
