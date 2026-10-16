"""Build the static documentation site.

Reads Markdown from ``docs/src`` and ``README.md`` and writes plain HTML pages into ``docs``.
Run from anywhere with ``python docs/build.py``. Requires the ``markdown`` and ``pygments`` packages.
"""

import html
import re
from dataclasses import dataclass
from pathlib import Path

import markdown
from pygments.formatters import HtmlFormatter

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parent
SRC = DOCS / "src"

REPO_URL = "https://github.com/ShinoMythmaker/Aetherblend"
WIKI_URL_PREFIX = f"{REPO_URL}/wiki/"
# Old wiki page names that now live under a different page.
LEGACY_PAGES = {"How-to-AetherBlend-(Alpha)": "getting-started", "Home": "index"}


@dataclass(frozen=True)
class Page:
    """One documentation page: ``name`` is the Markdown file stem in ``docs/src``."""

    name: str
    title: str
    sub: bool = False

    @property
    def slug(self) -> str:
        """Return the output file stem."""
        return self.name.lower()


NAV: tuple[tuple[str, tuple[Page, ...]], ...] = (
    (
        "Guides",
        (
            Page("Installation", "Installation"),
            Page("Getting-Started", "Getting Started"),
            Page("The-Template-System", "The Template System", sub=True),
            Page("Animation-Modding", "Animation Modding"),
        ),
    ),
    (
        "Operator Reference",
        (
            Page("Operators", "Overview"),
            Page("Operators-Import-Export", "Import / Export", sub=True),
            Page("Operators-Rig-Generator", "Rig Generator", sub=True),
            Page("Operators-Rig-Edit", "Rig Edit", sub=True),
            Page("Operators-Rig-UI", "Rig UI", sub=True),
            Page("Operators-Shaders", "Shaders", sub=True),
            Page("Operators-Preferences", "Preferences", sub=True),
        ),
    ),
    (
        "Development",
        (
            Page("Style-Guide", "Style Guide"),
            Page("Writing-Rig-Modules", "Writing Rig Modules", sub=True),
        ),
    ),
)
PAGES = tuple(page for _, pages in NAV for page in pages)
SLUGS = {page.name.lower(): page.slug for page in PAGES}
SLUGS.update({key.lower(): value for key, value in LEGACY_PAGES.items()})


def resolve_link(href: str) -> str | None:
    """Map a wiki-style link to a local page file, or return None to keep it unchanged."""
    if href.startswith(WIKI_URL_PREFIX):
        target = href[len(WIKI_URL_PREFIX) :]
    elif re.match(r"^([a-z][a-z0-9+.-]*:|#|/)", href, re.I):
        return None
    else:
        target = href
    name, _, anchor = target.partition("#")
    slug = SLUGS.get(name.removesuffix(".md").lower())
    if slug is None:
        return None
    return f"{slug}.html" + (f"#{anchor}" if anchor else "")


def render_markdown(text: str) -> tuple[str, str]:
    """Convert Markdown to HTML and return ``(body_html, toc_html)``."""
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
    """Return the shared top bar."""
    return f"""<header class="site-header">
  <button class="menu-btn" aria-label="Toggle navigation">&#9776;</button>
  <a class="brand" href="{prefix}index.html"><img src="assets/img/logo.png" alt="AetherBlend"></a>
  <nav class="header-links">
    <a href="installation.html">Docs</a>
    <a href="operators.html">Operators</a>
    <a href="style-guide.html">Style Guide</a>
    <a href="{REPO_URL}">GitHub</a>
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
    for group, pages in NAV:
        parts.append(f"<h4>{html.escape(group)}</h4>")
        for page in pages:
            classes = " ".join(c for c in ("sub" if page.sub else "", "active" if page == current else "") if c)
            parts.append(f'<a href="{page.slug}.html" class="{classes}">{html.escape(page.title)}</a>')
    return '<aside class="sidebar">' + "\n".join(parts) + "</aside>"


def build_page(page: Page) -> str:
    """Render one documentation page."""
    source = (SRC / f"{page.name}.md").read_text(encoding="utf-8")
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


def readme_section(readme: str, heading: str) -> str:
    """Return the text under a ``## heading`` of the README."""
    match = re.search(rf"^##\s+{re.escape(heading)}.*?\n(.*?)(?=^##\s|^---\s*$|\Z)", readme, re.S | re.M)
    return match.group(1).strip() if match else ""


def strip_html_tags(text: str) -> str:
    """Remove raw HTML tags and non-breaking space markers from README text."""
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"^&nbsp;\s*$", "", text, flags=re.M).strip()


def build_index() -> str:
    """Render the landing page from the README and the wiki home text."""
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    intro = re.search(r"^(AetherBlend is a plugin designed.*?)\n(Note:.*?)\n", readme, re.M)
    lead = intro.group(1) if intro else "AetherBlend is a Blender add-on for posing and animating FFXIV characters."
    note = intro.group(2) if intro else ""
    goal = render_markdown(strip_html_tags(readme_section(readme, "What is the goal")))[0]
    thanks = readme_section(readme, "Acknowledgements")
    thanks_items = [p.strip() for p in strip_html_tags(thanks).split("\n\n") if p.strip()]
    thanks_html = "".join(f"<p>{render_markdown(item)[0][3:-4]}</p>" for item in thanks_items)
    download = re.search(r'href="([^"]*releases/download[^"]*)"', readme)
    download_url = html.unescape(download.group(1)) if download else f"{REPO_URL}/releases/latest"
    discord = re.search(r"https://discord\.gg/\w+", readme)
    discord_url = discord.group(0) if discord else REPO_URL
    home = (SRC / "Home.md").read_text(encoding="utf-8") if (SRC / "Home.md").exists() else ""
    about = re.search(r"^(AetherBlend is a plugin for Blender built.*?)$", home, re.M)
    about_html = render_markdown(about.group(1))[0] if about else ""

    cards = "".join(
        f'<a class="card" href="{slug}.html"><h3>{title}</h3><p>{text}</p></a>'
        for slug, title, text in (
            ("installation", "Installation", "Requirements and how to install the add-on."),
            ("getting-started", "Getting Started", "Import a character and generate your first rig."),
            ("animation-modding", "Animation Modding", "Take an animation from Blender into the game."),
            ("the-template-system", "Template System", "Build and share your own rig templates."),
            ("operators", "Operator Reference", "Every operator, its parameters and what it does."),
            ("style-guide", "Style Guide", "Conventions for contributing code."),
        )
    )
    content = f"""{header_html()}
<section class="hero">
  <img class="logo" src="assets/img/logo.png" alt="AetherBlend">
  <div><span class="badge">Blender 5.2+ &middot; Beta</span></div>
  <p class="lead">{html.escape(lead)}</p>
  <p class="note">{html.escape(note)}</p>
  <div class="btn-row">
    <a class="btn primary" href="{html.escape(download_url)}">Download for Blender</a>
    <a class="btn" href="installation.html">Installation guide</a>
    <a class="btn" href="{REPO_URL}">View on GitHub</a>
  </div>
</section>
<div class="landing">
  <div class="showcase"><img src="assets/img/showcase.jpg" alt="AetherBlend showcase"></div>
  <section>
    <h2>What is AetherBlend?</h2>
    {about_html}
    {goal}
  </section>
  <section>
    <h2>Documentation</h2>
    <div class="cards">{cards}</div>
  </section>
  <section>
    <h2>Support &amp; Feedback</h2>
    <p>Submit <a href="{REPO_URL}/issues">issues and suggestions</a> on GitHub, browse the documentation, or join the
    <a href="{discord_url}">Discord</a> to follow development.</p>
    <div class="banner"><a href="{discord_url}">
      <img src="assets/img/discord-banner.png" alt="Join the Discord"></a></div>
  </section>
  <section>
    <h2>Acknowledgements</h2>
    <div class="thanks">{thanks_html}</div>
  </section>
</div>
<footer class="site-footer">AetherBlend &middot; <a href="{REPO_URL}">GitHub</a></footer>"""
    return shell("AetherBlend – Posing and animation for FFXIV in Blender", content, lead)


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
