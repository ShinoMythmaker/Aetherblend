"""Build the static documentation site.

Reads Markdown from ``docs/src`` and writes plain HTML pages into ``docs``.
Run from anywhere with ``python docs/build.py``. Requires the ``markdown`` and ``pygments`` packages.
"""

import html
import json
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import markdown
from pygments.formatters import HtmlFormatter

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parent
SRC = DOCS / "src"

REPO_URL = "https://github.com/ShinoMythmaker/Aetherblend"
WIKI_URL_PREFIX = f"{REPO_URL}/wiki/"


@dataclass(frozen=True)
class Page:
    """One documentation page, described by the frontmatter of a Markdown file under ``docs/src``."""

    name: str
    title: str
    group: str
    order: int
    path: Path
    sub: bool = False
    summary: str = ""
    aliases: tuple[str, ...] = ()

    @property
    def slug(self) -> str:
        """Return the output file stem."""
        return self.name.lower()


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Split an optional ``---`` delimited ``key: value`` block from the top of the Markdown."""
    match = re.match(r"---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not match:
        return {}, text
    meta = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        if key.strip():
            meta[key.strip().lower()] = value.strip()
    return meta, text[match.end() :]


def load_pages() -> tuple[Page, ...]:
    """Discover navigation pages: every Markdown file under ``docs/src`` with a ``group`` in its frontmatter.

    Page names (file stems) must be unique across folders; the output stays flat.
    """
    pages = []
    names: dict[str, Path] = {}
    for path in sorted(SRC.rglob("*.md")):
        meta, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        if "group" not in meta:
            continue
        if path.stem in names:
            raise SystemExit(f"Duplicate page name '{path.stem}': {names[path.stem]} and {path}")
        names[path.stem] = path
        pages.append(
            Page(
                name=path.stem,
                title=meta.get("title", path.stem.replace("-", " ")),
                group=meta["group"],
                order=int(meta.get("order", 1000)),
                path=path,
                sub=meta.get("sub", "").lower() == "true",
                summary=meta.get("summary", ""),
                aliases=tuple(a.strip() for a in meta.get("aliases", "").split(",") if a.strip()),
            )
        )
    return tuple(sorted(pages, key=lambda page: (page.order, page.name)))


def read_manifest() -> dict[str, str]:
    """Read the simple ``key = "value"`` pairs from ``blender_manifest.toml``."""
    text = (ROOT / "blender_manifest.toml").read_text(encoding="utf-8")
    return dict(re.findall(r'^(\w+)\s*=\s*"([^"]*)"', text, re.M))


MANIFEST = read_manifest()
VERSION = MANIFEST["version"]
BLENDER_MIN = ".".join(MANIFEST["blender_version_min"].split(".")[:2])
MASTER_REPO_JSON = "https://raw.githubusercontent.com/ShinoMythmaker/FFXIV-Blender-Plugins/refs/heads/main/repo.json"


def version_key(version: str) -> tuple[int, ...]:
    """Turn ``1.2.3`` into a sortable tuple."""
    return tuple(int(part) for part in re.findall(r"\d+", version))


def drag_link(archive_url: str, blender_min: str) -> str:
    """Build a link Blender accepts by drag and drop: the zip plus the repository it belongs to."""
    repository = urllib.parse.quote(MASTER_REPO_JSON, safe="")
    return f"{archive_url}?repository={repository}&blender_version_min={blender_min}"


def release_facts() -> dict[str, str]:
    """Read the newest Blender-compatible releases from the shared repository."""
    try:
        with urllib.request.urlopen(MASTER_REPO_JSON, timeout=15) as response:  # noqa: S310
            entries = json.load(response)["data"]
        if not isinstance(entries, list):
            raise ValueError("Repository data must be a list.")
        facts: dict[str, str] = {}
        ours = version_key(MANIFEST["blender_version_min"])
        for plugin_id, prefix in (("AetherBlend", ""), ("meddle_tools", "meddle_"), ("FFGear", "ffgear_")):
            usable = []
            for entry in entries:
                if not isinstance(entry, dict):
                    raise ValueError("Repository entries must be objects.")
                if entry.get("id") != plugin_id:
                    continue
                for field in ("version", "website", "archive_url", "blender_version_min"):
                    if not isinstance(entry.get(field), str) or not entry[field]:
                        raise ValueError(f"{plugin_id}: missing or invalid {field}.")
                if version_key(entry["blender_version_min"]) > ours:
                    continue
                maximum = entry.get("blender_version_max")
                if maximum and ours >= version_key(maximum):
                    continue
                usable.append(entry)
            if not usable:
                raise ValueError(f"No compatible release found for {plugin_id}.")
            best = max(usable, key=lambda entry: version_key(entry["version"]))
            facts[f"{prefix}latest_zip" if prefix else "latest_release_zip"] = best["archive_url"]
            facts[f"{prefix}latest_repo" if prefix else "latest_release_repo"] = drag_link(
                best["archive_url"], best["blender_version_min"]
            )
            if prefix:
                facts[f"{prefix}version"] = best["version"]
                facts[f"{prefix}github"] = best["website"].rstrip("/")
        return facts
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise SystemExit(f"[AetherBlend] Could not load release metadata: {error}") from error


FACTS = {
    "ab_version": VERSION,
    "blender_min": BLENDER_MIN,
    "ab_github": REPO_URL,
    **release_facts(),
}
PAGES = load_pages()
GROUPS: dict[str, tuple[Page, ...]] = {}
for _page in PAGES:
    GROUPS[_page.group] = (*GROUPS.get(_page.group, ()), _page)
SLUGS = {page.name.lower(): page.slug for page in PAGES}
SLUGS["home"] = "index"
for _page in PAGES:
    SLUGS.update({alias.lower(): _page.slug for alias in _page.aliases})


def apply_facts(text: str) -> str:
    """Replace author placeholders with manifest and release metadata."""
    rendered = re.sub(r"\{\{\s*(\w+)\s*\}\}", lambda m: FACTS.get(m.group(1), m.group(0)), text)
    return rendered.replace(r"\{\{", "{{")


def resolve_link(href: str) -> str | None:
    """Map a wiki-style link to a local page file, or return None to keep it unchanged."""
    if href.startswith(WIKI_URL_PREFIX):
        target = href[len(WIKI_URL_PREFIX) :]
    elif re.match(r"^([a-z][a-z0-9+.-]*:|#|/)", href, re.I):
        return None
    else:
        target = href
    name, _, anchor = target.partition("#")
    name = name.rsplit("/", 1)[-1]
    slug = SLUGS.get(name.removesuffix(".md").lower())
    if slug is None:
        return None
    return f"{slug}.html" + (f"#{anchor}" if anchor else "")


def render_markdown(text: str) -> tuple[str, str]:
    """Convert Markdown to HTML and return ``(body_html, toc_html)``."""
    text = apply_facts(text)
    text = re.sub(r"\[\[([^\]]+)\]\]", lambda m: f"[{m.group(1)}]({m.group(1).strip().replace(' ', '-')})", text)
    text = re.sub(r"^&nbsp;\s*$", "", text, flags=re.M)
    md = markdown.Markdown(
        extensions=["fenced_code", "tables", "toc", "attr_list", "md_in_html", "codehilite"],
        extension_configs={
            "toc": {"toc_depth": "2-3", "permalink": "#"},
            "codehilite": {"guess_lang": False, "css_class": "codehilite"},
        },
    )
    body = md.convert(text)
    body = re.sub(
        r'href="([^"]+)"',
        lambda m: f'href="{resolve_link(html.unescape(m.group(1))) or m.group(1)}"',
        body,
    )
    body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    toc = md.toc if len(md.toc_tokens) > 1 else ""  # type: ignore[attr-defined]
    return body, toc


def split_title(text: str, fallback: str) -> tuple[str, str]:
    """Remove a leading heading from the Markdown and return ``(title, rest)``."""
    match = re.match(r"\s*(<!--.*?-->\s*)?#\s+(.+?)\s*\n", text, re.S)
    if not match:
        return fallback, text
    return match.group(2).strip(), text[match.end() :]


def header_html(prefix: str = "") -> str:
    """Return the shared top bar; one link per navigation group."""
    links = "\n    ".join(f'<a href="{pages[0].slug}.html">{html.escape(group)}</a>' for group, pages in GROUPS.items())
    return f"""<header class="site-header">
  <button class="menu-btn" aria-label="Toggle navigation">&#9776;</button>
  <a class="brand" href="{prefix}index.html"><img src="assets/img/logo.png" alt="AetherBlend"></a>
  <nav class="header-links">
    {links}
    <a href="{REPO_URL}">GitHub</a>
    <a href="{prefix}index.html#support-project">Support</a>
    <a href="https://mythmaker-studio.com/">Studio</a>
    <a class="cta" href="{REPO_URL}/releases/latest">Download</a>
  </nav>
</header>"""


def shell(title: str, content: str, description: str = "") -> str:
    """Wrap page content in the HTML document skeleton."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="icon" href="assets/img/logo.png">
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="assets/pygments.css">
</head>
<body>
{content}
<script src="assets/site.js"></script>
</body>
</html>
"""


def sidebar_html(current: Page) -> str:
    """Return the left navigation with the current page highlighted."""
    parts = []
    for group, pages in GROUPS.items():
        parts.append(f"<h4>{html.escape(group)}</h4>")
        for page in pages:
            classes = " ".join(c for c in ("sub" if page.sub else "", "active" if page == current else "") if c)
            parts.append(f'<a href="{page.slug}.html" class="{classes}">{html.escape(page.title)}</a>')
    return '<aside class="sidebar">' + "\n".join(parts) + "</aside>"


def build_page(page: Page) -> str:
    """Render one documentation page."""
    _, source = split_frontmatter(page.path.read_text(encoding="utf-8"))
    title, text = split_title(source, page.title)
    body, toc = render_markdown(text)
    index = PAGES.index(page)
    prev_link = next_link = ""
    if index > 0:
        prev = PAGES[index - 1]
        prev_link = f'<a class="prev" href="{prev.slug}.html"><small>Previous</small>{html.escape(prev.title)}</a>'
    if index < len(PAGES) - 1:
        nxt = PAGES[index + 1]
        next_link = f'<a class="next" href="{nxt.slug}.html"><small>Next</small>{html.escape(nxt.title)}</a>'
    toc_col = f'<aside class="toc-col"><h4>On this page</h4>{toc}</aside>' if toc else '<aside class="toc-col"></aside>'
    content = f"""{header_html()}
<div class="layout">
{sidebar_html(page)}
<main><article>
<h1>{html.escape(title)}</h1>
{body}
<div class="page-nav">{prev_link}{next_link}</div>
</article></main>
{toc_col}
</div>
<footer class="site-footer">AetherBlend documentation &middot; <a href="{REPO_URL}">GitHub</a></footer>"""
    return shell(f"{title} · AetherBlend", content)


def build_index() -> str:
    """Render the landing page from Home.md and the navigation metadata."""
    home = (SRC / "Home.md").read_text(encoding="utf-8")
    title, text = split_title(home, "AetherBlend")
    body, _ = render_markdown(text)
    cards = "".join(
        f'<a class="card" href="{page.slug}.html"><h3>{html.escape(page.title)}</h3>'
        f"<p>{html.escape(page.summary)}</p></a>"
        for page in PAGES
        if page.summary
    )
    body = body.replace("<!-- documentation-cards -->", f'<div class="cards">{cards}</div>')
    content = f"""{header_html()}
{body}
<footer class="site-footer">AetherBlend &middot; <a href="{REPO_URL}">GitHub</a></footer>"""
    return shell(title, content)


def main() -> None:
    """Generate every page and the code highlighting stylesheet."""
    (DOCS / "assets" / "pygments.css").write_text(
        HtmlFormatter(style="github-dark").get_style_defs(".codehilite"), encoding="utf-8"
    )
    for old in DOCS.glob("*.html"):
        old.unlink()
    (DOCS / "index.html").write_text(build_index(), encoding="utf-8")
    for page in PAGES:
        (DOCS / f"{page.slug}.html").write_text(build_page(page), encoding="utf-8")
    print(f"[AetherBlend] Built {len(PAGES) + 1} pages in {DOCS}")


if __name__ == "__main__":
    main()
