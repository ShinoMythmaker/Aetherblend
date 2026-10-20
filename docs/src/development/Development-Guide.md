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

```sh
git clone https://github.com/ShinoMythmaker/Aetherblend.git
cd Aetherblend
git switch -c my-change
```

Use your fork URL when appropriate.

### 1. Create the virtual environment

From the repository root:

```sh
python -m venv .venv
```

On Linux/macOS, use `python3` if `python` isn't available:

```sh
python3 -m venv .venv
```

### 2. Select it in VS Code

1. Open the Command Palette with **Ctrl+Shift+P** / **Cmd+Shift+P**.
2. Run **Python: Select Interpreter**.
3. Select the interpreter inside `.venv`.
4. Run **Terminal: Create New Terminal**. With automatic environment activation
   enabled, VS Code activates `.venv` in that new terminal.

Verify that the terminal uses the environment:

```sh
python -c "import sys; print(sys.executable)"
```

The printed path should point inside `.venv`.

Selecting the interpreter doesn't necessarily activate an already-open
terminal - open a new one afterward.

### 3. Install dependencies

In that activated terminal:

```sh
python -m pip install --upgrade pip ruff tomli-w markdown pygments fake-bpy-module
python get_dependencies.py
```

The final command downloads the add-on's dependency wheels.

For Blender integration, install the [Blender Development extension](https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development)
and use **Blender: Build and Start** to launch the add-on.

## Make and validate a change

1. Read the relevant [Style Guide](Style-Guide) rules and make one focused
   change in the owning feature.
2. Run checks from the repository root in the activated terminal:

### Check for issues
```sh
python -m ruff check .
```
### Apply fixes Ruff can make automatically
```sh
python -m ruff check --fix path/to/file.py
```
### Format a file
```sh
python -m ruff format path/to/file.py
```
### Check formatting without changing files
```sh
python -m ruff format --check .
```

Instead of using `path/to/file.py`, you can use `.` to target the whole repository.