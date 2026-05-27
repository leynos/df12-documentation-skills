---
name: changelog
description: >
  Write and maintain a project's `CHANGELOG.md` following the Common Changelog
  style. Use this skill whenever the user asks to create, draft, update,
  rewrite, or review a changelog; add a release entry; record notable changes
  since the last tag; cut a release; promote a prerelease; or document a yanked
  release. Trigger on phrases such as "update the changelog", "add a changelog
  entry", "what changed since v1.2.0?", "draft release notes from git history",
  or "write CHANGELOG.md".
---

# Changelog skill

Produce or update a project's `CHANGELOG.md` in the Common Changelog style:
a human-curated, ordered list of notable changes per versioned release. The
output prioritises consumer comprehension over machine parsing.

This skill is adapted from **Common Changelog** by Vincent Weevers, which is
itself a stricter subset of [Keep a Changelog](https://keepachangelog.com/).
The original specification lives at <https://common-changelog.org/> and is
licensed under MIT. Credit and substantive guidance belong to the upstream
authors; this skill packages their conventions for repeatable use.

## Guiding principles

- Changelogs are for humans, not machines.
- Communicate the **impact** of changes, not the mechanics.
- Sort content by importance; breaking changes first.
- Skip content that is not interesting to consumers of the project's
  distributed form.
- Link each change to further information (commit, pull request, issue, or
  ticket).
- Do not generate the changelog entirely from `git log`. Curate it.

## Prerequisites

- The project is under version control (git assumed).
- Each released version has a corresponding git tag (with or without a `v`
  prefix).
- The project adheres to [Semantic Versioning](https://semver.org/).

If any of these are missing, raise it with the user before drafting. A
changelog whose versions cannot be tied to tags is unreliable.

## Workflow

### 1. Gather source material

Before writing, collect inputs in this order:

- The existing `CHANGELOG.md`, if any. Match its tone and reference style.
- Git history between the last released tag and `HEAD` (or between the two
  tags being documented).
- Merged pull requests, closed issues, and external tickets referenced by the
  commits in that range.
- Any release notes, upgrade guides, or migration documents the user supplies.

Useful starting commands:

```bash
git tag --sort=-v:refname | head            # most recent tags
git log <previous-tag>..HEAD --no-merges    # raw commit list
git log <previous-tag>..HEAD --merges       # PR merges (on GitHub flows)
```

Read the diffs of unclear commits before describing them. A change you cannot
explain plainly to a reader does not belong in the changelog yet.

### 2. Draft the entry from history, then curate

Generate a rough list of candidate changes from the commit and PR titles in
range. Then **curate**: this is the step that distinguishes a changelog from a
`git log` dump.

- **Remove noise.** Exclude maintenance work that does not affect consumers of
  the distributed project: dotfile tweaks, dev-only dependency bumps, minor
  code-style adjustments, and pure formatting changes in documentation.
- **Keep meaningful refactors.** Refactorings, supported-runtime changes, and
  documentation for previously undocumented features stay in.
- **Rephrase for consistency.** Different contributors describe the same kind
  of change differently. Align wording without straying so far that authors no
  longer recognise their own work.
- **Merge related changes.** Two commits bumping the same dependency become
  one entry: `Bump \`json-parser\` from 2.x to 4.x (a, b)`. A feature plus its
  follow-up fixup becomes one entry crediting both commits.
- **Skip no-op changes.** If a commit was reverted within the same release
  range, leave both out.
- **Separate description from commit body.** Each change is one line. Long
  explanations belong in the commit, the PR, or a dedicated upgrade guide —
  not the changelog.

### 3. Structure the entry

Follow the file and release formats in [Format](#format) below. Then sort
within each change group:

1. Breaking changes first (prefixed `**Breaking:**`).
2. Then by importance, at the writer's discretion.
3. Then latest-first by commit date for ties.

### 4. Review and tighten

Before delivering, check for these failure modes:

- **Verbatim copying.** Did entries get pasted from commit subjects or PR
  titles without rephrasing? Rewrite.
- **Conventional Commit residue.** Are entries prefixed with `feat:`,
  `fix:`, `chore:`, `docs:`, or scoped variants like `feat(api):`? Strip
  them. The category heading carries the type; the prefix is noise.
- **Vague entries.** "Improve performance" or "Fix bugs" are placeholders,
  not entries. Name what improved and by how much, or what bug was fixed.
- **Missing references.** Does every entry link to at least a commit?
  Prefer a PR or issue if one exists.
- **Wrong category.** Is a removal listed under `Changed`? Move it.
- **Inverted importance.** Is a breaking change buried below a refactor?
  Reorder.
- **Time-zone date confusion.** Is the date anything other than
  `YYYY-MM-DD`? Convert it.
- **Unreleased section.** Common Changelog does not use one. Remove it if
  present and roll its contents into the release being cut.

### 5. Deliver the file

Write the curated entry to `CHANGELOG.md` at the repo root, prepended above
prior releases. If creating a new `CHANGELOG.md`, start with the first-level
heading `# Changelog`. Keep reference-style links at the foot of the file.

## Format

### File header

```markdown
# Changelog
```

The file is Markdown. The first heading is exactly `# Changelog`. Subsequent
content is zero or more release entries, sorted **latest-first** by Semantic
Versioning rules (not by publication date).

### Release heading

Each release begins with a second-level heading:

```markdown
## [VERSION] - YYYY-MM-DD
```

- `VERSION` is a semver-valid version with no `v` prefix, matching a git tag
  (the tag itself may carry a `v` prefix).
- The date is ISO 8601 (`YYYY-MM-DD`). No regional formats.
- The version is a reference-style link to further information — typically a
  GitHub release page or compare view. Reference definitions sit at the foot
  of the file.

Example:

```markdown
## [1.0.1] - 2019-08-24

### Fixed

- Prevent segmentation fault on `close()` ([#42](https://github.com/owner/name/issues/42))

## [1.0.0] - 2019-08-23

_Initial release._

[1.0.1]: https://github.com/owner/name/releases/tag/v1.0.1
[1.0.0]: https://github.com/owner/name/releases/tag/v1.0.0
```

### Notice

A release may begin with a single italicised paragraph — a **notice** —
before any change groups. Use a notice to:

- Point to an upgrade guide or blog post (`_If you are upgrading: see
  [\`UPGRADING.md\`](UPGRADING.md)._`).
- Describe a first release with no prior changes (`_Initial release._`).
- Flag a yanked release (`_This release was yanked due to a regression
  ([#123](https://example/issues/123))._`).
- Note that a stable release simply promotes a prerelease (`_Stable release
  based on [3.1.0-rc.2]._`).

There is at most one notice per release. Notices do **not** replace change
groups for yanked releases that had real content; the original change list
must remain.

### Change groups

A change group is a third-level heading followed by an unordered list.
The category must be one of these, used in this order when more than one
applies:

- `### Changed` — changes in existing functionality.
- `### Added` — new functionality.
- `### Removed` — removed functionality.
- `### Fixed` — bug fixes.

There is no `Deprecated` and no `Security` category. Record deprecations
under `Changed` (`Deprecate the \`unsafe\` option`). Record security fixes
under `Fixed` with a clear note.

"Functionality" includes documentation, supported runtime environments, build
outputs, and anything else a consumer perceives.

#### Change line shape

Each list item is a single line. Optional prefixes — first `**Breaking:**`,
then a `**Subsystem:**` prefix — appear at the start of the line, immediately
before the change description. References follow the description, with
authors last:

```text
- [**Breaking:** ][**<Subsystem>:** ]<Change> (<references>) (<authors>)
```

When both prefixes apply on a single line, combine them as
`**<Subsystem> (breaking):** <Change>` rather than stacking two bold
prefixes.

Concretely:

```markdown
- Fix infinite loop in scheduler ([#194](https://github.com/owner/name/issues/194)) (Alice Meerkat)
- **Breaking:** drop support for Node.js 8 ([`53bd922`](https://github.com/owner/name/commit/53bd922))
- **UI:** tune button colours for accessibility ([#221](https://github.com/owner/name/pull/221))
```

#### Imperative mood

Write each change in the imperative mood and make it self-describing without
relying on the category heading:

| Avoid                                  | Prefer                              |
| -------------------------------------- | ----------------------------------- |
| `Support of CentOS`                    | `Support CentOS`                    |
| `\`write()\` method`                   | `Add \`write()\` method`            |
| `Documentation for the \`read()\` method` | `Document the \`read()\` method` |
| `Added support for streaming uploads`  | `Add support for streaming uploads` |

Use present-tense verbs: `Add`, `Bump`, `Document`, `Deprecate`, `Drop`,
`Fix`, `Refactor`, `Remove`, `Rename`, `Restore`, `Support`.

#### References

Every change must reference at least the commit that introduced it. Prefer a
pull request or issue when one exists. Only include the best entry point if
multiple references are available — readers should not have to follow three
links to understand one change.

Reference forms:

```markdown
([`53bd922`](https://github.com/owner/name/commit/53bd922))
([`owner/name@53bd922`](https://github.com/owner/name/commit/53bd922))
([#194](https://github.com/owner/name/issues/194))
([owner/name#194](https://github.com/owner/name/issues/194))
([JIRA-837](https://example.atlassian.net/browse/JIRA-837))
```

The owner-prefixed forms are for git submodules or for issues in external
repositories. Otherwise use the short form.

References sit in a single set of parentheses, with same-type references
comma-separated:

```markdown
- Fix infinite loop ([#194](https://example/issues/194), [#195](https://example/issues/195))
```

#### Authors

After references, list authors in parentheses, comma-separated. With both
references and authors on one entry, separate the two groups with a
semicolon. References remain Markdown links — the shorthand `#194` is only
used in this document's prose to keep examples readable; the rendered
changelog must use the linked form:

```markdown
- Fix infinite loop ([#194](https://example/issues/194), [#195](https://example/issues/195); Alice Meerkat, Milly Moose)
```

On single-contributor projects, omit authors. For bot-authored changes, list
the human who merged the pull request. Use each author's own preferred name
(typically the one they use in git).

#### Prefixes

- **Breaking:** Mark breaking changes with `**Breaking:**` at the start of
  the line. Breaking changes appear before non-breaking changes within each
  category.
- **Subsystem:** For projects with subsystems (git submodules or other
  internal units), prefix with the subsystem name: `**UI:**`,
  `**Installer:**`. A breaking change within a subsystem uses
  `**<Subsystem> (breaking):**`. Use subsystem prefixes sparingly — they
  weaken semver signalling.

### Markdown formatting

Common Changelog is not opinionated on Markdown formatting beyond the
structural rules above. Adopt whatever line wrapping, list marker, and
emphasis style the existing `CHANGELOG.md` uses, or the project's
documentation conventions.

## Antipatterns

These reliably produce changelogs that nobody reads. Avoid them.

- **Verbatim PR or commit dumps.** Lists like `docs: fix dead link
  (#296)` mixed with `feat: support streaming (#291)` are noise. Curate.
- **Conventional Commit prefixes in entries.** The categories already
  encode the kind of change; prefixes such as `feat:` and `fix(api):`
  duplicate information and add cognitive load. Strip them when lifting
  text from commits.
- **Regional dates.** `07/04/2024` is ambiguous across locales. Always
  use `YYYY-MM-DD`.
- **An `Unreleased` section.** Common Changelog drops this. Pending
  changes live in commits and pull requests until release time.
- **Multi-line entries.** A long explanation belongs in the linked
  commit, PR, or upgrade guide. The changelog stays scannable.
- **`[YANKED]` tags.** Use a notice instead: `_This release was yanked
  due to..._`.

## Promoting a prerelease

When promoting `X.Y.Z-rc.N` to `X.Y.Z`, pick one approach:

- **Copy content.** Merge and rephrase the prerelease entries into the
  stable entry as if the prereleases never existed. Best for public
  projects whose consumers ignore prereleases.
- **Skip the entry.** Acceptable only for prereleases used purely for
  internal CI testing.
- **Refer to the prerelease.** Use a notice: `_Stable release based on
  [3.1.0-rc.2]._`. Best for private projects where all stakeholders
  already know the prerelease contents.

## Yanked releases

A release that was public for more than a few hours stays in the
changelog. Add a notice explaining the yank and linking to context.
Keep the original change list:

```markdown
## [8.5.1] - 2021-05-10

_This release was never published to npm due to a security regression
([#123](https://github.com/owner/name/issues/123))._

### Fixed

- Validate URL host before redirect ([#120](https://github.com/owner/name/pull/120))
```

## Rewriting history

It is acceptable, and sometimes necessary, to rewrite past changelog
entries. A changelog is a historical record meant to answer "when did X
change?" — improving older entries serves that purpose. Note the rewrite
in the commit message that introduces it.

## Worked example

```markdown
# Changelog

## [2.0.0] - 2024-03-12

_If you are upgrading: please see [`UPGRADING.md`](UPGRADING.md)._

### Changed

- **Breaking:** emit `close` event after `end` ([#312](https://example/pull/312))
- Refactor `sort()` internals to reduce allocations on large inputs ([`a91f4c0`](https://example/commit/a91f4c0))

### Removed

- **Breaking:** drop support for Node.js 14 ([#308](https://example/pull/308))

### Added

- Support streaming uploads via `pipeTo()` ([#298](https://example/pull/298)) (Alice Meerkat)
- Document the `read()` method ([#301](https://example/pull/301))

### Fixed

- Prevent buffer overflow when input exceeds 64 KiB ([#305](https://example/pull/305)) (Henry Otter, Milly Moose)

## [1.4.2] - 2024-01-08

### Fixed

- Unpin `json-parser` having fixed alice/json-parser#38 ([#295](https://example/pull/295))

[2.0.0]: https://example/compare/v1.4.2...v2.0.0
[1.4.2]: https://example/compare/v1.4.1...v1.4.2
```

## Key constraints

- File is `CHANGELOG.md` at the repository root.
- First heading is exactly `# Changelog`.
- Releases sorted latest-first by Semantic Versioning, not by date.
- Dates in `YYYY-MM-DD` (ISO 8601).
- Categories restricted to `Changed`, `Added`, `Removed`, `Fixed`, in that
  order when more than one is present.
- Every entry is one line, imperative mood, with at least one reference.
- Breaking changes are marked `**Breaking:**` and appear first within their
  category.
- No `Unreleased`, `Deprecated`, `Security`, `[YANKED]`, or Conventional
  Commit prefixes in entries.
- British English in any prose this skill itself produces (notices, commit
  messages introducing changelog edits). Spellings inside referenced commit
  subjects are preserved verbatim.

## Source and licence

This skill is adapted from **Common Changelog** by Vincent Weevers and
contributors, available at <https://common-changelog.org/> (source:
<https://github.com/vweevers/common-changelog>). Common Changelog is itself
adapted from [Keep a Changelog](https://keepachangelog.com/) by Olivier
Lacan and contributors. Both upstream documents are licensed under MIT.
