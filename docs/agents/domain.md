# Domain Docs

How an agent should read this repo's domain documentation before working on the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root: the vocabulary this repository uses, and the words it
  deliberately avoids.
- **`GOALS.md`**, when it exists: what the package works toward.
- **`docs/adr/`**, when it exists: the decisions that touch the area you are about to work in.

If any of these files don't exist, proceed silently. Don't flag their absence, and don't suggest
creating them upfront.

## File structure

Single-context repo:

```
/
├── CONTEXT.md
├── CONSTITUTION.md
├── docs/adr/        (created when the first decision is recorded)
└── src/sphinx_daisyui/
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, say, or a test name), use the term as
defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids. Three are worth
repeating:

- An **admonition** is named after its directive. Never call it a notice or a callout.
- A **daisyUI theme** is one of daisyUI's colour sets. "Theme" on its own is this package.
- A **borrowed option** keeps the name and meaning Furo or pydata-sphinx-theme gave it.

## The prototype is the look

The branch `prototype-theme` is the accepted prototype of the whole theme. Port its templates,
components and styles to `main` rather than drawing them again, and compare what you build with
the prototype's pages side by side.

## Flag conflicts with a recorded decision

If your output contradicts a decision in `docs/adr/`, surface it explicitly rather than silently
overriding it.
