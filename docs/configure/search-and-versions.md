# Search and versions

## Search

Press {kbd}`Ctrl+K`, {kbd}`⌘K` or {kbd}`/` anywhere. Results appear as you type: pages, the
sections inside them, and API names such as functions and classes. Use {kbd}`↑` and {kbd}`↓` to
move, {kbd}`Enter` to open. Enter with nothing chosen opens Sphinx's full search page.

Search reads the index Sphinx already writes, so it works on any static host and sends nothing
anywhere. Set `disable_search` to `True` to leave it out.

## Versions

The version menu reads the same `switcher.json` as pydata-sphinx-theme:

```json
[
  {"name": "1.2 (stable)", "version": "1.2", "url": "https://example.org/1.2/", "preferred": true},
  {"name": "1.3 (dev)", "version": "dev", "url": "https://example.org/dev/"}
]
```

```python
html_theme_options = {
    "switcher": {"json_url": "https://example.org/switcher.json", "version_match": "1.2"},
}
```

Choosing a version opens the page you are on in that version when it exists there, and the
version's home page when it doesn't. Try it in the navbar of this site: the other two entries
are this documentation built with a Furo configuration and a pydata-sphinx-theme configuration.
