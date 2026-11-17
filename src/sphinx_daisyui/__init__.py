"""A Sphinx theme drawn with daisyUI, configured with the options of Furo and pydata-sphinx-theme."""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup
from markupsafe import Markup
from sphinx.application import Sphinx
from sphinx.util import logging

__version__ = "0.1.0.dev0"

THEME_PATH = Path(__file__).parent / "theme" / "daisyui"
LOGGER = logging.getLogger(__name__)

# Every theme daisyUI 5 ships. The picker offers these unless `theme_picker` names others.
DAISYUI_THEMES = [
    "light", "dark", "cupcake", "bumblebee", "emerald", "corporate", "synthwave", "retro",
    "cyberpunk", "valentine", "halloween", "garden", "forest", "aqua", "lofi", "pastel",
    "fantasy", "wireframe", "black", "luxury", "dracula", "cmyk", "autumn", "business",
    "acid", "lemonade", "night", "coffee", "winter", "dim", "nord", "sunset", "caramellatte",
    "abyss", "silk",
]

# Font Awesome names that pydata-sphinx-theme configurations use, mapped to bundled icons.
FONT_AWESOME = {
    "github": "github", "square-github": "github", "gitlab": "gitlab", "square-gitlab": "gitlab",
    "bitbucket": "bitbucket", "twitter": "x-twitter", "x-twitter": "x-twitter",
    "square-x-twitter": "x-twitter", "square-twitter": "x-twitter", "mastodon": "mastodon", "discord": "discord", "python": "python",
    "pypi": "pypi", "youtube": "youtube", "discourse": "discourse", "stack-overflow": "stackoverflow",
    "bluesky": "bluesky", "docker": "docker", "npm": "npm", "orcid": "orcid", "book": "book-open",
    "book-open": "book-open", "link": "link", "comments": "discourse", "conda": "condaforge",
    "anaconda": "anaconda", "jupyter": "jupyter",
}


@cache
def icons() -> dict[str, str]:
    return json.loads((Path(__file__).parent / "icons.json").read_text())


def icon(name: str, css: str = "size-5") -> Markup:
    """Return an inline SVG icon by its bundled name, sized by Tailwind classes."""
    svg = icons().get(name) or icons()["link"]
    return Markup(svg.replace("<svg ", f'<svg class="{css}" aria-hidden="true" focusable="false" ', 1))


def fa_icon(spec: str) -> str:
    """Pick the bundled icon for a Font Awesome class string such as 'fa-brands fa-github'."""
    for part in spec.replace(",", " ").split():
        key = part.removeprefix("fa-")
        if key in FONT_AWESOME:
            return FONT_AWESOME[key]
    return "link"


def as_list(value: Any) -> list:
    """Read a theme option that pydata-sphinx-theme accepts as a list or a comma-separated string."""
    if value in (None, "", False):
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return list(value)


def as_bool(value: Any, default: bool = False) -> bool:
    if value in (None, ""):
        return default
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "on"}
    return bool(value)


def as_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def as_dict(value: Any) -> dict:
    if not value:
        return {}
    if isinstance(value, str):
        try:
            return json.loads(value)
        except ValueError:
            return {}
    return dict(value)


def template_names(value: Any) -> list[str]:
    """Turn component names ('navbar-logo') into the template files that draw them."""
    names = []
    for name in as_list(value):
        names.append(name if name.endswith(".html") else f"{name}.html")
    return names


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------


def navigation_markup(toctree_html: str, show_nav_level: int, section_only: bool) -> Markup:
    """Redraw Sphinx's toctree as a daisyUI menu whose branches open and close.

    A branch is open when it holds the page being read, or when it sits above
    `show_nav_level`. With `section_only`, only the current top-level section is kept,
    as pydata-sphinx-theme does when its header carries the top-level links.
    """
    soup = BeautifulSoup(toctree_html, "html.parser")
    lists = soup.find_all("ul", recursive=False)
    if section_only:
        current = soup.select_one("ul > li.current")
        inner = current.find("ul", recursive=False) if current else None
        if inner is None:
            return Markup("")
        lists = [inner]

    def walk(ul, depth: int) -> None:
        ul["class"] = ["daisy-nav-list"]
        for li in ul.find_all("li", recursive=False):
            classes = set(li.get("class", []))
            link = li.find("a", recursive=False)
            child = li.find("ul", recursive=False)
            li["class"] = ["daisy-nav-item"]
            if link is not None:
                link["class"] = ["daisy-nav-link"]
                if "current" in classes and (child is None or not child.select("li.current")):
                    link["class"].append("menu-active")
                    link["aria-current"] = "page"
                elif "current" in classes:
                    link["class"].append("daisy-on-path")
                if link.get("href", "").startswith(("http://", "https://")):
                    link["class"].append("daisy-external")
                    link.append(BeautifulSoup(str(icon("external-link", "size-3.5 opacity-60 shrink-0")), "html.parser"))
            if child is not None:
                is_open = "current" in classes or depth < show_nav_level - 1
                li["class"].append("daisy-nav-branch")
                row = soup.new_tag("div", attrs={"class": "daisy-nav-row"})
                link.wrap(row) if link is not None else None
                button = soup.new_tag(
                    "button",
                    attrs={
                        "type": "button",
                        "class": "daisy-nav-toggle btn btn-ghost btn-xs btn-square",
                        "aria-expanded": "true" if is_open else "false",
                        "aria-label": f"Show the pages in {link.get_text(strip=True) if link else ''}",
                    },
                )
                button.append(BeautifulSoup(str(icon("chevron-right", "size-4")), "html.parser"))
                (row if link is not None else li).append(button)
                if not is_open:
                    child["hidden"] = ""
                walk(child, depth + 1)

    for ul in lists:
        walk(ul, 0)
    captions = soup.find_all("p", class_="caption")
    for caption in captions:
        caption["class"] = ["daisy-nav-caption"]
    if section_only:
        return Markup("".join(str(ul) for ul in lists))
    return Markup(str(soup))


def header_links(toctree_html: str) -> list[dict]:
    """The top-level pages, as pydata-sphinx-theme puts them in its header."""
    soup = BeautifulSoup(toctree_html, "html.parser")
    links = []
    for li in soup.select("ul > li.toctree-l1"):
        a = li.find("a")
        if a is None:
            continue
        links.append(
            {
                "title": a.get_text(strip=True),
                "href": a.get("href", "#"),
                "current": "current" in li.get("class", []),
                "external": a.get("href", "").startswith(("http://", "https://")),
            }
        )
    return links


def page_toc(toc_html: str) -> tuple[Markup, int]:
    """The page's own headings, without the page title Sphinx puts at the top of `toc`."""
    soup = BeautifulSoup(toc_html or "", "html.parser")
    top = soup.find("li")
    inner = top.find("ul") if top else None
    if inner is None:
        return Markup(""), 0
    count = len(inner.find_all("li"))
    for ul in [inner, *inner.find_all("ul")]:
        ul["class"] = ["daisy-toc-list"]
    for a in inner.find_all("a"):
        a["class"] = ["daisy-toc-link"]
    return Markup(str(inner)), count


def rewrite_body(markup: str) -> str:
    """Add to a page's body what CSS cannot.

    - Every outermost table is wrapped in a named region that takes keyboard focus,
      so a table wider than the page scrolls sideways on its own, also for a reader
      with no pointer. The region is named by the table's caption, or "Table".
    - An equation on its own line has its notation wrapped the same way, after its
      number, so a wide equation scrolls.
    - Every heading link is named for a screen reader by the text it belongs to.
    """
    if "<table" not in markup and 'class="math' not in markup and "headerlink" not in markup:
        return markup
    soup = BeautifulSoup(markup, "html.parser")
    for table in soup.find_all("table"):
        if table.find_parent("table") is not None:
            continue
        caption = table.find("caption")
        label = caption.get_text(" ", strip=True).rstrip("¶#").strip() if caption else "Table"
        wrapper = soup.new_tag("div", attrs={"class": "daisy-sphinx-scroll", "role": "region", "tabindex": "0", "aria-label": label})
        table.wrap(wrapper)
    for block in soup.select("div.math"):
        number = block.find("span", class_="eqno", recursive=False)
        label = "Equation " + number.get_text(" ", strip=True).strip("()¶# ") if number else "Equation"
        wrapper = soup.new_tag("div", attrs={"class": "daisy-sphinx-scroll", "role": "region", "tabindex": "0", "aria-label": label.strip()})
        for child in [c for c in block.contents if c is not number]:
            wrapper.append(child.extract())
        block.append(wrapper)
    for link in soup.select("a.headerlink"):
        holder = link.parent
        text = ""
        if holder is not None:
            if holder.name == "dt" and holder.find(class_="sig-name"):
                text = "".join(el.get_text() for el in holder.select(".sig-prename, .sig-name"))
            else:
                text = "".join(s for s in holder.find_all(string=True) if s.parent is not link).strip()
        title = link.get("title", "")
        link["aria-label"] = f"{title}: {text}" if title and text else (text or title)
    return str(soup)


# ---------------------------------------------------------------------------
# Options read the way Furo and pydata-sphinx-theme read them
# ---------------------------------------------------------------------------


def static_url(context: dict, path: str) -> str:
    if not path:
        return ""
    if "://" in path or path.startswith("//") or path.startswith("data:"):
        return path
    pathto = context["pathto"]
    if path.startswith("_static/"):
        return pathto(path, 1)
    return pathto(f"_static/{path}", 1)


def brand(context: dict, opt) -> dict:
    logo = as_dict(opt("logo"))
    sphinx_logo = context.get("logo_url") or ""
    light = logo.get("image_light") or opt("light_logo") or ""
    dark = logo.get("image_dark") or opt("dark_logo") or ""
    light_src = static_url(context, light) if light else sphinx_logo
    dark_src = static_url(context, dark) if dark else light_src
    text = logo.get("text")
    if text is None:
        text = context.get("docstitle") or context.get("project") or ""
        # A logo that already carries the name is drawn without the text, as both themes allow.
        if as_bool(opt("sidebar_hide_name")) or (light_src and "text" not in logo and logo):
            text = ""
    href = logo.get("link") or opt("logo_link") or context["pathto"](context.get("root_doc", "index"))
    return {
        "text": text,
        "light": light_src,
        "dark": dark_src,
        "alt": logo.get("alt_text") or context.get("project") or "",
        "href": href,
    }


def icon_links(opt) -> list[dict]:
    links = []
    for key, name, glyph in (
        ("github_url", "GitHub", "github"),
        ("gitlab_url", "GitLab", "gitlab"),
        ("bitbucket_url", "Bitbucket", "bitbucket"),
        ("twitter_url", "X", "x-twitter"),
    ):
        if opt(key):
            links.append({"name": name, "url": opt(key), "svg": icon(glyph)})
    for item in as_list(opt("icon_links")):
        item = dict(item)
        kind = item.get("type", "fontawesome")
        spec = item.get("icon", "")
        if kind == "url":
            svg = Markup(f'<img src="{spec}" alt="" class="size-5 rounded-sm">')
        elif kind == "local":
            svg = Markup(f'<img src="{spec}" alt="" class="size-5 rounded-sm">')
        elif spec in icons():
            svg = icon(spec)
        else:
            svg = icon(fa_icon(spec))
        links.append({"name": item.get("name", ""), "url": item.get("url", "#"), "svg": svg})
    return links


def footer_icons(opt) -> list[dict]:
    """Furo's footer_icons: each carries its own SVG markup."""
    out = []
    for item in as_list(opt("footer_icons")):
        item = dict(item)
        out.append({"name": item.get("name", ""), "url": item.get("url", "#"), "svg": Markup(item.get("html", ""))})
    return out


def source_links(context: dict, opt) -> dict:
    """Edit and view URLs, from Furo's source_* options or pydata-sphinx-theme's html_context."""
    page = context.get("pagename", "")
    if not context.get("sourcename"):
        # Generated pages such as the index and search have no source to edit.
        return {"edit": "", "view": "", "source": ""}
    suffix = context.get("page_source_suffix") or ".rst"
    filename = f"{page}{suffix}"
    edit = view = ""
    if opt("source_edit_link"):
        edit = opt("source_edit_link").format(filename=filename)
    if opt("source_view_link"):
        view = opt("source_view_link").format(filename=filename)
    repo = (opt("source_repository") or "").rstrip("/")
    if repo and not (edit and view):
        branch = opt("source_branch") or "main"
        directory = (opt("source_directory") or "").strip("/")
        path = f"{directory}/{filename}" if directory else filename
        edit = edit or f"{repo}/edit/{branch}/{path}"
        view = view or f"{repo}/blob/{branch}/{path}"
    if not edit:
        hosts = (
            ("github_user", "github_repo", "github_version", "https://github.com", "edit"),
            ("gitlab_user", "gitlab_repo", "gitlab_version", "https://gitlab.com", "-/edit"),
            ("bitbucket_user", "bitbucket_repo", "bitbucket_version", "https://bitbucket.org", "src"),
        )
        for user_key, repo_key, version_key, host, verb in hosts:
            if context.get(user_key) and context.get(repo_key):
                version = context.get(version_key) or "main"
                doc_path = (context.get("doc_path") or "").strip("/")
                path = f"{doc_path}/{filename}" if doc_path else filename
                base = f"{host}/{context[user_key]}/{context[repo_key]}"
                edit = f"{base}/{verb}/{version}/{path}"
                view = view or f"{base}/blob/{version}/{path}"
                break
    if context.get("show_source") and context.get("has_source") and context.get("sourcename"):
        source = context["pathto"]("_sources/" + context["sourcename"], 1)
    else:
        source = ""
    return {"edit": edit, "view": view, "source": source}


def css_variables(opt) -> Markup:
    """Furo's light_css_variables and dark_css_variables, mapped onto daisyUI's tokens."""
    mapping = {
        "color-brand-primary": "--color-primary",
        "color-brand-content": "--daisy-sphinx-link-override",
        "color-background-primary": "--color-base-100",
        "color-background-secondary": "--color-base-200",
        "color-foreground-primary": "--color-base-content",
        "font-stack": "--font-sans",
        "font-stack--monospace": "--font-mono",
        "font-stack--headings": "--font-headings",
    }
    rules = []
    for option, selector in (("light_css_variables", '[data-mode="light"]'), ("dark_css_variables", '[data-mode="dark"]')):
        values = as_dict(opt(option))
        if not values:
            continue
        decls = []
        for name, value in values.items():
            name = name.removeprefix("--")
            target = mapping.get(name) or ("--" + name)
            decls.append(f"{target}: {value};")
        rules.append(f":root{selector} {{ {' '.join(decls)} }}")
    return Markup("\n".join(rules))


def on_page_context(app: Sphinx, pagename: str, templatename: str, context: dict, doctree) -> None:
    if app.config.html_theme != "daisyui":
        return

    def opt(name: str, default: Any = None) -> Any:
        value = context.get(f"theme_{name}")
        return default if value in (None, "") else value

    toctree = context.get("toctree")
    navbar_center = template_names(opt("navbar_center", ""))
    sectioned = "navbar-nav.html" in navbar_center
    depth = as_int(opt("navigation_depth"), 4)
    collapse = as_bool(opt("collapse_navigation"))
    includehidden = as_bool(opt("sidebar_includehidden"), True)
    nav_html = ""
    top_html = ""
    if toctree is not None:
        nav_html = toctree(maxdepth=depth, collapse=collapse, includehidden=includehidden, titles_only=True)
        top_html = toctree(maxdepth=1, collapse=False, includehidden=includehidden, titles_only=True)
    toc_markup, toc_count = page_toc(context.get("toc", ""))

    links = header_links(top_html)
    externals = [
        {"title": item.get("name", ""), "href": item.get("url", "#"), "current": False, "external": True}
        for item in as_list(opt("external_links"))
    ]
    cut = as_int(opt("header_links_before_dropdown"), 5)
    all_links = links + externals

    secondary = template_names(opt("secondary_sidebar_items", "page-toc"))
    top_buttons = as_list(opt("top_of_page_buttons")) or as_list(opt("top_of_page_button", "edit"))
    if as_bool(opt("use_edit_page_button")) and "edit-this-page.html" not in secondary:
        secondary.append("edit-this-page.html")

    picker = opt("theme_picker", "")
    if picker in (True, "true", "True", "all"):
        picker_themes = DAISYUI_THEMES
    else:
        picker_themes = as_list(picker)

    switcher = as_dict(opt("switcher"))

    css_files = context.get("css_files", [])
    pygments_set = bool(opt("pygments_light_style") or opt("pygments_dark_style"))
    if not pygments_set:
        context["css_files"] = [c for c in css_files if not str(getattr(c, "filename", c)).endswith("pygments.css")]

    if context.get("body"):
        context["body"] = rewrite_body(context["body"])

    sources = source_links(context, opt)
    context["daisy"] = {
        "version": __version__,
        "icon": icon,
        "brand": brand(context, opt),
        "light_theme": opt("light_theme", "light"),
        "dark_theme": opt("dark_theme", "dark"),
        "default_mode": opt("default_mode", "auto"),
        "picker": picker_themes,
        "announcement": opt("announcement", ""),
        "navigation": navigation_markup(nav_html, as_int(opt("show_nav_level"), 1), sectioned) if nav_html else "",
        "header_links": all_links[:cut],
        "header_more": all_links[cut:],
        "header_more_text": opt("header_dropdown_text", "More"),
        "page_toc": toc_markup,
        "page_toc_count": toc_count,
        "show_toc_level": as_int(opt("show_toc_level"), 2),
        "icon_links": icon_links(opt),
        "footer_icons": footer_icons(opt),
        "sources": sources,
        "top_buttons": [b for b in top_buttons if (b == "edit" and sources["edit"]) or (b == "view" and sources["view"])],
        "navbar_start": template_names(opt("navbar_start", "navbar-logo")),
        "navbar_center": navbar_center,
        "navbar_end": template_names(opt("navbar_end", "version-switcher, theme-switcher, navbar-icon-links")),
        "navbar_persistent": template_names(opt("navbar_persistent", "search-button-field")),
        "article_header_start": template_names(opt("article_header_start", "breadcrumbs")),
        "article_header_end": template_names(opt("article_header_end", "")),
        "article_footer_items": template_names(opt("article_footer_items", "")),
        "content_footer_items": template_names(opt("content_footer_items", "")),
        "primary_sidebar_end": template_names(opt("primary_sidebar_end", "")),
        "secondary": secondary,
        "footer_start": template_names(opt("footer_start", "copyright, sphinx-version")),
        "footer_center": template_names(opt("footer_center", "")),
        "footer_end": template_names(opt("footer_end", "theme-version")),
        "show_prev_next": as_bool(opt("show_prev_next"), True),
        "back_to_top": as_bool(opt("back_to_top_button"), True),
        "navigation_with_keys": as_bool(opt("navigation_with_keys")),
        "search_bar_text": opt("search_bar_text", "Search the docs"),
        "switcher": switcher,
        "css_variables": css_variables(opt),
        "pygments_custom": pygments_set,
        "sectioned": sectioned,
    }


def on_builder_inited(app: Sphinx) -> None:
    """Write daisyUI-scoped Pygments styles when a pydata-style pygments option is set."""
    if app.config.html_theme != "daisyui" or app.builder.format != "html":
        return
    options = {**(app.builder.theme.get_options() if app.builder.theme else {}), **app.config.html_theme_options}
    light = options.get("pygments_light_style") or ""
    dark = options.get("pygments_dark_style") or ""
    if not (light or dark):
        return
    from pygments.formatters import HtmlFormatter

    css = []
    for style, mode in ((light, "light"), (dark, "dark")):
        if style:
            css.append(HtmlFormatter(style=style).get_style_defs(f'html[data-mode="{mode}"] .highlight'))
    out = Path(app.outdir) / "_static" / "daisy-pygments.css"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(css))
    app.add_css_file("daisy-pygments.css", priority=900)


def setup(app: Sphinx) -> dict:
    app.add_html_theme("daisyui", str(THEME_PATH))
    app.connect("builder-inited", on_builder_inited)
    app.connect("html-page-context", on_page_context)
    return {"version": __version__, "parallel_read_safe": True, "parallel_write_safe": True}
