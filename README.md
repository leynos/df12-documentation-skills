# df12 documentation skills

*Reusable Codex skills for df12 documentation, review, planning and prose
workflows.*

This repository packages small, focused skills that make documentation work
repeatable: commit messages, pull request descriptions, README files, technical
terms of reference, design documents, roadmaps, df12 copy and en-GB Oxford
English.

______________________________________________________________________

## Why df12-documentation-skills?

Documentation quality depends on repeatable judgement. These skills collect
the house rules in a form Codex can load at the right moment:

- **Consistent workflow artefacts**: Commit messages, draft pull requests,
  README files, terms of reference, roadmaps, and design documents follow
  durable structures.
- **df12 voice in one place**: Public-facing prose can use the same compressed,
  precise, dry, grounded and playful register across projects.
- **British Oxford spelling by default**: The language rule is explicit, so
  documentation does not drift between spelling variants.
- **Small packages**: Each skill stays narrow enough to load only the guidance
  needed for the task.

______________________________________________________________________

## Quick start

### Installation

From this repository, install all bundled skills into the default Codex skill
directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/* "${CODEX_HOME:-$HOME/.codex}/skills/"
```

To install one skill, copy only its folder:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/pr-creation "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Some skills have companion-skill dependencies. For example,
[`roadmap-grooming`](skills/roadmap-grooming/SKILL.md) requires
[`roadmap-doc`](skills/roadmap-doc/SKILL.md) and
[`roadmap-doc/references/conventions.md`](skills/roadmap-doc/references/conventions.md)
because it delegates the roadmap grammar and formatting rules to that skill.
Install both folders for that workflow:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/roadmap-doc skills/roadmap-grooming \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
```

### Basic usage

Reference a skill by name in a Codex request:

```text
$df12-readme
```

For example:

```text
Please create a README for this repository using $df12-readme.
```

______________________________________________________________________

## Skills

- [`changelog`](skills/changelog/SKILL.md) drafts and curates `CHANGELOG.md`
  in the Common Changelog style, with consumer-focused entries, ISO 8601
  dates, breaking-change prefixes and linked references.
- [`commit-message`](skills/commit-message/SKILL.md) writes file-backed Git
  commit messages and forbids inline `git commit -m` messages.
- [`df12-copy`](skills/df12-copy/SKILL.md) applies the df12 Productions copy
  voice for public-facing prose, with detailed references in
  [`voice-and-copy-style-guide.md`](skills/df12-copy/references/voice-and-copy-style-guide.md)
  and
  [`logisphere-expert-profiles.md`](skills/df12-copy/references/logisphere-expert-profiles.md).
- [`df12-readme`](skills/df12-readme/SKILL.md) creates README files in the df12
  house style.
- [`en-gb-oxendict-style`](skills/en-gb-oxendict/SKILL.md) enforces British
  English with Oxford spelling conventions.
- [`pr-creation`](skills/pr-creation/SKILL.md) creates draft pull requests with
  branch-wide descriptions, issue and roadmap references, execplan links, and
  reviewer entrypoints.
- [`roadmap-doc`](skills/roadmap-doc/SKILL.md) turns design documents,
  Requests for Comments (RFCs) and Architectural Decision Records (ADRs) into
  outcome-oriented roadmaps, using
  [`conventions.md`](skills/roadmap-doc/references/conventions.md) for the
  detailed format.
- [`roadmap-grooming`](skills/roadmap-grooming/SKILL.md) maintains living GIST
  (Goals, Ideas, Steps, Tasks) roadmaps during execution, routing new findings,
  refactoring fragments and feature ideas into coherent phases. It requires
  [`roadmap-doc`](skills/roadmap-doc/SKILL.md) as a companion skill.
- [`tech-design-doc`](skills/tech-design-doc/SKILL.md) produces rigorous
  technical design documents, supported by
  [`document-anatomy.md`](skills/tech-design-doc/references/document-anatomy.md),
  [`editing-checklist.md`](skills/tech-design-doc/references/editing-checklist.md)
  and
  [`research-protocol.md`](skills/tech-design-doc/references/research-protocol.md).
- [`terms-of-reference-doc`](skills/terms-of-reference-doc/SKILL.md) produces
  upstream problem-space documents that establish domain, market, users,
  job-to-be-done, scope, constraints and open questions before solution work
  begins.

______________________________________________________________________

## Learn more

- [Users' Guide](docs/users-guide.md) — how documentation practitioners combine
  the workflow skills.
- [Developers' Guide](docs/developers-guide.md) — validation gates and
  repository maintenance expectations.

______________________________________________________________________

## Maintaining skills

Keep each skill focused on the information another Codex instance needs at the
moment it triggers. Prefer a concise `SKILL.md`, and add `references/` files
only when the detail would otherwise bloat the main skill.

Validate edited skills before committing:

```bash
SKILL_CREATOR="${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator"
uv run --with pyyaml python \
  "$SKILL_CREATOR/scripts/quick_validate.py" \
  skills/<skill-name>
git diff --check
markdownlint-cli2 README.md skills/<skill-name>/SKILL.md
```

______________________________________________________________________

## Licence

ISC Licence — see [LICENSE](LICENSE) for details.

______________________________________________________________________

## Contributing

Keep additions small, evidence-backed and linked to files that exist in the
repository. When adding or changing a skill, validate it, run Markdown linting,
check the diff for whitespace errors, then commit the change with the
`commit-message` skill.
