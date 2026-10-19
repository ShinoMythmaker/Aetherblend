---
title: Development Guide
group: Development
order: 100
summary: A quick setup guide to help you start contributing.
aliases: Contributing
---
# Development Guide

Use this checklist for a code change. For Doc and site work, see the
[Documenting Guide](Documenting-Guide); code conventions are in the
[Style Guide](Style-Guide).

## Set up

Install Git, Python 3.13+, Blender {{blender_min}}+ and
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

In VS Code, select `.venv` with **Python: Select Interpreter**. For Blender
integration, install the [Blender Development extension](https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development)
and use **Blender: Build and Start** to launch the add-on.

## Make and validate a change

1. Read the relevant [Style Guide](Style-Guide) rules and make one focused
   change in the owning feature.
2. Run checks from the repository root:

### Check for issues
```powershell
.venv\Scripts\python.exe -m ruff check .
```
### Apply fixes Ruff can make automatically
```powershell
.venv\Scripts\python.exe -m ruff check --fix path\to\file.py
```
### Format a file
```powershell
.venv\Scripts\python.exe -m ruff format path\to\file.py
```
### Check formatting without changing files
```powershell
.venv\Scripts\python.exe -m ruff format --check .
```

Instead of using `path\to\file.py` u can always use ` . ` to target the whole repository.