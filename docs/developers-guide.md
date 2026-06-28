# Developers' Guide

*Repository maintenance gates for df12 documentation skills.*

This guide covers repository-local validation and file hygiene. The
[Users' Guide](users-guide.md) remains the workflow guide for applying the
skills in downstream projects.

______________________________________________________________________

## Validation gates

Run focused gates for every skill documentation change before committing:

```bash
SKILL_CREATOR="${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator"
uv run --with pyyaml python \
  "$SKILL_CREATOR/scripts/quick_validate.py" \
  skills/<skill-name>
make markdownlint
make nixie
git diff --check
```

`quick_validate.py` checks skill frontmatter and required skill-file structure.
`make markdownlint` applies the repository Markdown style from
`.markdownlint-cli2.jsonc` to changed Markdown files against `origin/main`,
including 80-column prose wrapping, ordered-list style, tab handling, and
node/cache ignore paths. `git diff --check` catches trailing whitespace and
other patch hygiene defects.

Run the gates sequentially. The repository `Makefile` is the documented build
driver, so automation can invoke the same targets as local development.

______________________________________________________________________

## Markdown linting

The repository uses `markdownlint-cli2`, configured by
[`.markdownlint-cli2.jsonc`](../.markdownlint-cli2.jsonc). Keep new Markdown
files within the configured wrapping rules unless the content is a table or
code block covered by the config exceptions.

When adding a new skill with reference documents, `make markdownlint` includes
changed main `SKILL.md` and `references/*.md` files. This avoids shipping
reference-only lint failures.

______________________________________________________________________

## Mermaid validation

The `make nixie` target runs `nixie` against changed Markdown files to validate
Mermaid diagrams. Keep Mermaid diagrams inside Markdown code fences so the
validator can discover them.

______________________________________________________________________

## Ignore rules

The root [`.gitignore`](../.gitignore) intentionally excludes local tool
caches, Python virtual environments, build outputs, Rust targets, and agent
workspace metadata. Skill source, Markdown references, docs, and validation
configuration should remain tracked.

Do not add ignore rules for generated documentation unless the generator output
is reproducible and explicitly outside the published skill package.
