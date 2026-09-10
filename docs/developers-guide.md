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
make skill-manifest-check
make markdownlint
make nixie
git diff --check
```

`quick_validate.py` checks skill frontmatter and required skill-file structure.
`make skill-manifest-check` enforces the Agent Skills manifest schema over every
shipped skill; see [Skill manifest validation](#skill-manifest-validation).
`make markdownlint` applies the repository Markdown style from
`.markdownlint-cli2.jsonc` to changed Markdown files against `origin/main`,
including 80-column prose wrapping, ordered-list style, tab handling, and
node/cache ignore paths. `git diff --check` catches trailing whitespace and
other patch hygiene defects.

Run the gates sequentially. The repository `Makefile` is the documented build
driver, so automation can invoke the same targets as local development.

______________________________________________________________________

## Skill manifest validation

Each skill directory under [`skills/`](../skills) carries a `SKILL.md` whose
YAML frontmatter is an Agent Skills manifest. Three Makefile targets enforce
that contract:

- `make skill-manifest-check`
  - Aggregate target; runs both targets below, and is wired into `make lint`.
  - All three manifest targets read `SKILL_DIRS`, which defaults to every
    `skills/*/SKILL.md` directory and can be overridden (for example
    `make skill-manifest-check SKILL_DIRS=skills/changelog/`) to check a
    single skill or a test fixture; the test suite relies on this.
- `make skill-frontmatter-lint`
  - Extracts the YAML frontmatter block of each `SKILL.md` with `awk` and
    pipes it to `yamllint` using the inline `SKILL_YAMLLINT_CONFIG` (default
    rules with `line-length` disabled). The recipe runs under `pipefail`, so a
    manifest that cannot be read fails the target rather than being skipped.
- `make skill-manifest-validate`
  - Runs `skills-ref validate` over each skill directory to enforce the Agent
    Skills manifest schema, which includes the rule that the directory name
    matches the manifest `name`.

`tests/test_skill_manifests.py` asserts that every shipped manifest satisfies
the contract, and that `make lint` still fails on a malformed fixture, so the
wiring is covered rather than assumed.

`quick_validate.py` and the manifest targets check different contracts: the
skill-creator script checks the structure a Codex install expects, while
`skills-ref` checks the Agent Skills schema. Both run for a skill change.

### Skill manifest tooling dependencies

`skills-ref` and `yamllint` are development-only dependencies in the
`[dependency-groups] dev` array of `pyproject.toml`. Neither is a runtime
dependency of any skill.

- `skills-ref` is pinned by git URL to a specific commit, subdirectory
  `skills-ref`; it provides the `skills-ref validate` command. Invoke it via
  `uv run --group dev skills-ref`.
- `yamllint` is invoked via `uv run --group dev yamllint`. It is declared
  explicitly rather than called as a bare binary, so the gate depends on the
  declared environment rather than on whatever the host image happens to ship.

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
