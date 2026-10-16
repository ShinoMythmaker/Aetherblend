---
title: Working on the Docs
group: Development
order: 195
summary: Edit the documentation, build the site and preview it in VS Code.
---
# Working on the Docs

The website is generated. You edit Markdown in `docs/src/`, run `build.py`, and it writes plain HTML pages into `docs/`, which GitHub Pages serves. The HTML files are committed, so always rebuild before you commit documentation changes.

## Setup

Use the virtual environment from [Contributing](Contributing). Its setup command already installs the two packages the build needs. If you set up the environment another way, install them:

```powershell
.venv\Scripts\python.exe -m pip install markdown pygments
```

## Where Things Live

| Path | Content |
|------|---------|
| `docs/src/guides/` | User guides (installation, getting started, ...) |
| `docs/src/operators/` | One page per operator group |
| `docs/src/development/` | Contributor pages like this one |
| `docs/src/Home.md` | Text used by the landing page |
| `README.md` | Landing page intro, goal and acknowledgements |
| `docs/assets/` | Stylesheet, scripts and images |
| `docs/*.html` | Generated output. Do not edit by hand |

## Adding or Editing a Page

Every Markdown file under `docs/src/` that has a `group` in its frontmatter becomes a page in the navigation:

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
| `aliases` | Comma separated extra names that link to this page |

Rules to keep in mind:

- File names must be unique across all folders. The output is flat, so `Style-Guide.md` becomes `style-guide.html`.
- Link to other pages by file name without extension, like `[Style Guide](Style-Guide)`. The build turns it into the right HTML link.
- Code blocks with a language (` ```python `) are syntax highlighted.
- Operator pages must list the ID, label, parameters, behavior, UI location and requirements.

## Build the Site

From the repository root:

```powershell
.venv\Scripts\python.exe docs\build.py
```

What it does:

- Reads the version and minimum Blender version from `blender_manifest.toml` and fills them into the pages.
- Renders every Markdown page and the landing page, then rewrites the HTML files in `docs/`.
- Updates the drag-and-drop download link in `README.md`.
- Reads the master `repo.json` online to build the Meddle Tools and FFGear links. Without a connection it prints a warning and falls back to the plain release page links.

Check `git status` afterwards. You should see your Markdown change plus the regenerated HTML files.

## Preview in VS Code

The pages use relative links, so serve the `docs` folder with a small local web server:

1. Open a terminal in VS Code and run:

   ```powershell
   Set-Location docs
   ..\.venv\Scripts\python.exe -m http.server 8000
   ```

2. Open the Command Palette (`Ctrl+Shift+P`), run **Simple Browser: Show** and enter `http://localhost:8000`.
3. Edit Markdown, run the build again and refresh the preview (the server keeps running).
4. Stop the server with `Ctrl+C` when you are done.

You can also open `docs\index.html` directly in a normal browser, but a server matches how GitHub Pages serves the site.

### Automate the rebuild (optional)

To rebuild with one keystroke, add a task in `.vscode/tasks.json` (the `.vscode` folder is ignored by git, so this stays local):

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Build docs",
      "type": "shell",
      "command": "${workspaceFolder}\\.venv\\Scripts\\python.exe docs\\build.py",
      "group": "build"
    },
    {
      "label": "Serve docs",
      "type": "shell",
      "command": "${workspaceFolder}\\.venv\\Scripts\\python.exe -m http.server 8000",
      "options": { "cwd": "${workspaceFolder}/docs" },
      "isBackground": true
    }
  ]
}
```

Run them with **Terminal > Run Task**.

## Before You Commit

- Rebuild with `docs\build.py` so the HTML matches the Markdown.
- Click through the changed pages in the preview, including navigation and links.
- Commit the Markdown and the generated HTML together.
