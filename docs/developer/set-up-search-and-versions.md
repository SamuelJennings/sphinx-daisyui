# Set up search and versions

The theme draws a search button in the header and a search dialog on every page. The dialog lists
pages, the sections inside them and API names such as functions and classes, from the index Sphinx
already writes.

## Search a site

1. Press {kbd}`Ctrl+K`, {kbd}`⌘K` or {kbd}`/` anywhere on a page, or choose the search button in
   the header.
2. Type what you are looking for. Results appear as you type.
3. Use {kbd}`↑` and {kbd}`↓` to move through them and {kbd}`Enter` to open one.

Enter with nothing chosen opens Sphinx's full search page with the words typed. {kbd}`Esc` closes
the dialog.

## Place the search button

1. Name `search-button-field` in the component list where it should sit. It is in
   `navbar_persistent` by default; to move it to the start of the header, write:

   ```python
   html_theme_options = {
       "navbar_persistent": [],
       "navbar_start": ["navbar-logo", "search-button-field"],
   }
   ```

The button now sits in that list, and the dialog is still written once on every page.
[Components](../reference/components.md) describes the button.

## Word the search button

1. Set `search_bar_text` in `html_theme_options`:

   ```python
   html_theme_options = {
       "search_bar_text": "Find in the manual",
   }
   ```

The button and the dialog's field now show those words. Left empty, they show Search the docs in
the language the site is built in.

## Stop results as you type

1. Set `search_as_you_type` to `False`:

   ```python
   html_theme_options = {
       "search_as_you_type": False,
   }
   ```

Typing in the dialog now lists nothing, and Enter opens the full search page with the words typed.

## Turn search off

1. Set `disable_search` to `True`:

   ```python
   html_theme_options = {
       "disable_search": True,
   }
   ```

No page now carries the button or the dialog, and the shortcuts do nothing. Sphinx's own search
page is still built. [Options](../reference/options.md) lists the three options with their
defaults.

## Why search stays in the reader's browser

Search reads the index Sphinx writes with the site, so it works on any static host. It sends
nothing anywhere: the words a reader types never leave their browser.
