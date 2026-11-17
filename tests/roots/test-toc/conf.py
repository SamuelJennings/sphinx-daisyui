from docutils import nodes

project = "Toc"
copyright = "2026, Test"
html_theme = "daisyui"


def give_non_ascii_id(app, doctree):
    """Give the heading of the unicode page an id Docutils would not write."""
    if app.env.docname != "unicode":
        return
    for section in doctree.findall(nodes.section):
        if section.next_node(nodes.title).astext() == "Café":
            section["ids"] = ["café-ünï"]


def setup(app):
    # Before the collector that reads the headings into the table of contents.
    app.connect("doctree-read", give_non_ascii_id, priority=100)
