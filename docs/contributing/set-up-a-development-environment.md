# Set up a development environment

You need [uv](https://docs.astral.sh/uv/) and [Node.js](https://nodejs.org/) 20 or later. Node
compiles the stylesheet. Nobody who only uses the theme needs it.

1. Clone the repository:

   ```bash
   git clone https://github.com/SamuelJennings/sphinx-daisyui.git
   cd sphinx-daisyui
   ```

2. Install the Python dependencies, the documentation's and the hooks. Installing the package
   compiles the stylesheet with npm the first time:

   ```bash
   uv sync --group docs
   uv run pre-commit install
   ```

3. Serve the documentation, which is built with the theme, and rebuild it on every change:

   ```bash
   uv run sphinx-autobuild docs docs/_build/html
   ```

4. While you change templates or `assets/`, recompile the stylesheet on every change in a second
   terminal:

   ```bash
   npm run watch
   ```
