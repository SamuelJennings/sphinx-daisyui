# Research: 005-links-and-compatibility

## Assumptions checked

Run on 2026-11-17 against the `prototype-theme` branch.

- **The prototype's source links assume GitHub's address form for every host.** `source_links`
  builds `{repo}/edit/{branch}/{path}` and `{repo}/blob/{branch}/{path}` from `source_repository`
  whatever the host. GitLab and Bitbucket use other forms, so FR-008 is new work, not a port.
- **The prototype's `url` and `local` icon links are identical** and build an `<img>` tag with an
  f-string, with the `local` path not resolved against `_static`.
- **The surfaces this feature extends are not on `main` yet.** Component lists, the icon set, the
  square icon button, the message catalogue and the static-path method come with the page frame
  (#4, draft pull request 12), and the breadcrumbs with #5. Nothing here can be run on `main` until
  they merge, which is why the issue depends on them.
