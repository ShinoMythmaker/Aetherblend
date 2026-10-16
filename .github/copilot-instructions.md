# AetherBlend Guidelines

Blender add-on (Python) for posing and animating FFXIV characters. Principles and workflow are in the AetherBlend Agent; this file holds the always-on basics.

## Hard Rules
- NEVER automate GitHub or git tasks unless the user explicitly asks for that specific action (commits, staging, branches, merges, pushes, issues, PRs, releases). Read-only git (`status`, `diff`, `log`) is fine. The user makes every commit.
- Follow [docs/src/Style-Guide.md](../docs/src/Style-Guide.md) and cite rule IDs (R-x.y).

## Build and Test
- Python is `.venv\Scripts\python.exe` (Windows, PowerShell).
- Lint: `.venv\Scripts\python.exe -m ruff check .` (config in `ruff.toml`).
- Compile check: `.venv\Scripts\python.exe -m compileall -q .`
- Blender cannot be run by the agent. Ask the user to test in Blender.
