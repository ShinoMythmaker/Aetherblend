---
title: Style Guide
group: Development
order: 120
summary: Readable conventions for contributing code.
---
# AetherBlend Style Guide

Use these principles to keep code readable and safe to disable. They describe
conventions, not repository layout; cite stable IDs (`R-x.y`) in reviews.
Lint settings live in `ruff.toml`; run `.venv\Scripts\python.exe -m ruff check .`.

## Structure

- **R-1.1** Features are self-contained; removing one and its registry entry
  must leave other features working.
- **R-1.2** A feature imports another only through its `__all__`.
- **R-1.3** Shared code belongs in shared packages, grouped by what it operates on.
- **R-1.4** Each package has a one-line docstring. Feature packages define
  `__all__`, `register()` and `unregister()`.

## Lifecycle and user data

- **R-2.1** Register feature modules in order and unregister them in reverse.
- **R-2.2** Cleanup removes everything the feature registers, including classes,
  properties, handlers, timers, keymaps and icons.
- **R-2.3** Registration and cleanup are idempotent.
- **R-2.4** Imports have no registration or Blender-data side effects.
- **R-2.5** Data stored in `.blend` files survives add-on disable and re-enable.
- **R-2.7** Register Blender classes explicitly in their defining module;
  unregister them there in reverse order.
- **R-2.8** Register property groups, then operators, then panels; unregister
  in reverse.

## Names and imports

- **R-3.1** Feature IDs and class names use the feature package name.
- **R-3.2** Operator IDs are lowercase with exactly one dot.
- **R-3.3** A panel's `bl_idname` matches its class name.
- **R-3.4** Blender classes use `AETHER_<TYPE>_<feature>_<name>`. Functions and
  variables use `lower_snake_case`, constants use `ALL_CAPS`, and private
  helpers start with `_`.
- **R-3.5** Operator IDs are public to scripts; list renames in the changelog.
- **R-8.1** Order imports: standard library, third party, then local.
- **R-8.2** Prefer module imports. Wildcard imports require an explicit `__all__`.
- **R-8.3** Use relative imports within a feature; follow **R-1.2** across features.
- **R-8.4** Keep imports at module scope unless a local import prevents a
  circular import; explain that exception in a comment.

## Functions and Blender interaction

- **R-4.2** Keep operators focused on Blender's operator lifecycle and reporting;
  put reusable logic in helpers or feature modules.
- **R-4.3** Operator messages are clear and actionable.
- **R-4.4** Data-changing operators should support undo.
- **R-4.5** Operator properties have a `name` and `description`.
- **R-4.6** Restore changed mode, selection, cursor and active object, including
  on errors.
- **R-5.1** Type every function argument and return value.
- **R-5.2** Prefer specific Blender types; use `Any` only when no better type fits.
- **R-5.3** Operator `execute`, `invoke` and `modal` return `set[str]`;
  `poll` returns `bool`.
- **R-6.2** Public functions have a one-line imperative docstring.
- **R-6.5** Blender properties have a user-facing description.
- **R-6.7** Comments explain why, not what.
- **R-7.2** Utilities changing mode restore the original mode, including on errors.

## Errors and output

- **R-9.1** Console output starts with `[AetherBlend]`.
- **R-9.2** Operators use `self.report`; utilities use `print`.
- **R-9.3** Never use a bare `except:`; catch specific exceptions.

## Documentation

- **R-10.1** Edit Markdown in `docs/src/`, not generated HTML. Rebuild with
  `.venv\Scripts\python.exe docs\build.py`; keep page names unique and use
  `Guides` or `Development` frontmatter. Use build placeholders for version
  and minimum Blender facts.
- **R-10.4** Keep this guide at `docs/src/development/Style-Guide.md`.
