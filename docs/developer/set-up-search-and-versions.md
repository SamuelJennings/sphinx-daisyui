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

## Show a version menu

1. Write the file that lists your versions, for example `switcher.json` in your static
   directory:

   ```json
   [
     {"name": "1.2 (stable)", "version": "1.2", "url": "https://example.org/1.2/", "preferred": true},
     {"name": "1.3 (dev)", "version": "dev", "url": "https://example.org/dev/"}
   ]
   ```

   Each entry needs a `version` and a `url`. `name` is the text in the menu and falls back to
   `version`. `preferred` marks the version to send readers to; set it on one entry.
2. Name the file and the version this build documents in `html_theme_options`:

   ```python
   html_theme_options = {
       "switcher": {
           "json_url": "https://example.org/switcher.json",
           "version_match": "1.2",
       },
   }
   ```

Every page now has a menu in the header labelled with `version_match`. The file is read when the
reader opens the page, so publishing a new version means editing the file and nothing else.
`json_url` may be a full address, a path from the server's root or a path from the site's root,
and so may each `url`. [Options](../reference/options.md) describes the three forms.

Choosing a version opens the page the reader is on in that version when it exists there, and the
version's home page when it does not.

## Warn readers of an old version

1. Set `show_version_warning_banner` to `True`:

   ```python
   html_theme_options = {
       "show_version_warning_banner": True,
   }
   ```

On any version other than the preferred one, a banner above the header now says which version
the reader is on and links to the preferred one.

## Check the file at build time

The build reads the file once at its end and warns, naming the address, when the file is missing,
unreadable, not JSON or not a list of entries with a `version` and a `url`. The build still
succeeds. To skip the check, for a file you publish after the build, set `check_switcher` to
`False`.
