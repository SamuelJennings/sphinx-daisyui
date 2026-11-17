import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

project = "Body"
html_theme = "daisyui"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.mathjax", "sphinx.ext.todo"]
todo_include_todos = True
