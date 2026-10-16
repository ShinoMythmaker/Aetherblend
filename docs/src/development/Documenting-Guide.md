---
title: Documenting Guide
group: Development
order: 110
summary: Edit the documentation, build the site and preview it in VS Code.
aliases: Working-On-The-Docs
---
# Documenting Guide

Write only useful task guides for AetherBlend users and practical setup or
quickstart pages for contributors. Put user workflows in **Guides** and
contributor workflows or conventions in **Development**. Keep API details in
the code rather than maintaining operator, ABI or rig-module catalogs.

The site is built from Markdown in `docs/src/`; `docs/build.py` generates the
HTML served from `docs/`. The generated pages are committed, so rebuild after
editing Markdown.

## Setup

Use the virtual environment from [Development Guide](Development-Guide). Its setup command already installs the two packages the build needs. If you set up the environment another way, install them:

```powershell
.venv\Scripts\python.exe -m pip install markdown pygments
```

## Choose and Edit a Page

First update an existing guide if it covers the workflow. Add a page only for
a distinct user task or contributor workflow. Keep navigable sources in
`guides/` or `development/`; `Home.md` is the landing page. Every Markdown
source with a `group` frontmatter value appears in navigation, so use only
`Guides` or `Development`.

```markdown
---
title: My Page
group: Development
order: 220
sub: true
summary: One line shown on the landing page card.
---
# My Page

Content here.
```

| Key | Meaning |
|-----|---------|
| `title` | Name in the navigation. Defaults to the file name |
| `group` | Navigation section, for example `Guides` or `Development` |
| `order` | Sort position. Lower comes first |
| `sub` | `true` shows the page indented under the previous one |
| `summary` | Short text for the landing page card |
| `aliases` | Comma-separated names that resolve source links to this page; they do not create HTML redirects |

- File names must be unique across all folders. The output is flat, so `Style-Guide.md` becomes `style-guide.html`.
- Link to other pages by file name without extension, like `[Style Guide](Style-Guide)`. The build turns it into the right HTML link.
- Code blocks with a language (` ```python `) are syntax highlighted.
- Code blocks wrap on narrow screens and have a **Copy** button; keep examples
  focused and ensure they copy as intended.
- A user guide should state prerequisites, give short numbered steps and say
  what success looks like. A development page should help a contributor finish
  one practical setup or workflow.
- Keep pages concise and low-maintenance. Include verified details needed for
  the task; avoid API inventories, implementation tours and duplicated
  instructions. Use a link to an existing guide or a short inline fact when
  useful.

## Build the Site

From the repository root:

```powershell
.venv\Scripts\python.exe docs\build.py
```

The builder reads version and minimum Blender facts from
`blender_manifest.toml`, renders Markdown to HTML and fetches the master
`repo.json` for dependency links. If that request fails, it warns and uses
release-page fallbacks.

Inspect the build output and `git status`. Confirm the changed page, navigation
and links look right, and check generated diffs for unrelated changes.

## Preview in VS Code

The pages use relative links, so serve the `docs` folder with a small local web server:

1. Open a terminal in VS Code and run:

   ```powershell
   .venv\Scripts\python.exe -m http.server 8000 --directory docs
   ```

2. Open the Command Palette (`Ctrl+Shift+P`), run **Simple Browser: Show** and enter `http://localhost:8000`.
3. Edit Markdown, run the build again and refresh the preview (the server keeps running).
4. Stop the server with `Ctrl+C` when you are done.

You can also open `docs\index.html` directly in a normal browser, but a server matches how GitHub Pages serves the site.


## Before You Finish

- Rebuild so generated HTML matches the Markdown.
- Preview the changed page and check its navigation and local links.
- Include the Markdown source and generated HTML in the change.
