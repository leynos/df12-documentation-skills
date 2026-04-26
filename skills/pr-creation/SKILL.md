---
name: pr-creation
description: >
  Create GitHub pull requests (PRs) with complete draft PR metadata,
  reviewer-focused descriptions, roadmap and issue references, execplan
  identification, and en-GB Oxford English. Use whenever Codex opens, drafts,
  revises, or prepares a pull request description or title for a branch.
---

# Pull request creation

Use this skill when creating or revising a pull request title or description.
Treat these requirements as mandatory.

## Non-negotiable requirements

- Create every pull request as a draft.
- Prefer the GitHub app or connector when available. Use GitHub CLI only when
  the app is unavailable or cannot perform the required operation.
- When using GitHub CLI, pass `--draft`. When using the GitHub app, a
  connector, or an API, set the draft field explicitly.
- Cover the full branch in the pull request description, not only the most
  recent commits.
- State what changed and why at the start of the description.
- Provide a purpose-first walkthrough of the changes, with clear reviewer
  entrypoints.
- Use third-person en-GB Oxford English in the title and description. Follow
  `$en-gb-oxendict-style`.
- Link every referenced file with a Markdown link to the relevant commit or,
  when a commit-specific reference is not yet stable, the branch ref.

## Gather required context

Before opening or revising the pull request, identify:

- the branch head and base branch;
- the full branch diff from merge base to head;
- whether the branch follows a roadmap task;
- whether the branch follows an issue;
- whether an execplan exists and whether it is pre-implementation; and
- the best commit or branch ref for file links.

Inspect the whole branch before writing the description. Do not rely only on
the latest commit message or the working tree diff.

## Title rules

Include all applicable references in the title:

- Roadmap task references must appear as `(1.2.3)`.
- Issue references must appear as `(#123)`.
- If both apply, include both references.

Use imperative mood for the action in the title.

For pre-implementation execplan pull requests, describe the action being
planned in the imperative mood. Do not use titles such as `Plan implementation
of foo`, `Add plan for foo`, or similar meta-descriptions. Put the
pre-implementation status in the description instead.

Examples:

- `Implement hosted worker registry filtering (1.2.3)`
- `Harden startup recovery (#123)`
- `Replace local cache invalidation (1.2.3) (#123)`

## Issue-linked pull requests

When the branch follows an issue:

- include the issue reference in the title as `(#123)`;
- include `Closes #123` in the description;
- identify the issue early in the description; and
- explain clearly when an alternative solution was used, when part of the
  issue was obviated, or when part of the issue was unimplementable.

Do not imply full issue completion if the branch only resolves part of the
issue. State the remaining scope explicitly.

## Roadmap-linked pull requests

When the branch follows a roadmap task:

- include the task reference in the title as `(1.2.3)`;
- identify the roadmap task early in the description; and
- explain how the branch satisfies the task's acceptance criteria or narrows
  the implementation scope.

## Execplan requirements

Identify the execplan clearly in the description by linking its file.

If the execplan is pre-implementation:

- say that the pull request carries the pre-implementation plan;
- title the pull request as the action being planned; and
- make clear what future implementation work the plan authorizes.

If the pull request implements an execplan:

- link the execplan;
- state which planned work landed in the branch; and
- call out deliberate deviations, newly discovered constraints, or deferred
  follow-up work.

## Description structure

Use this order unless repository-specific guidance overrides it:

```markdown
## Summary

This branch ...

Closes #123.

Roadmap task: (1.2.3)
Execplan: [docs/execplans/example.md](...)

## Review walkthrough

- Start with [path/to/file.ext](...) to see ...
- Then review [path/to/other.ext](...) for ...
- Finish with [path/to/test.ext](...) for ...

## Validation

- `command`: result

## Notes

...
```

Adapt headings to local conventions, but keep the same information order:
summary first, reviewer entrypoints next, validation evidence after that, and
notes or caveats last.

## Body file creation

Write pull request descriptions to a temporary file with an inert
single-quoted heredoc delimiter, then pass that file to the pull request tool.
Do not pass long descriptions as shell arguments.

Prefer creating the pull request through the GitHub app when it is available.
Use the body file contents as the app or connector body input. Fall back to
GitHub CLI only when the app is unavailable or cannot perform the required
operation.

```bash
PR_BODY_DIR=$(mktemp -d)
cat > "$PR_BODY_DIR/body.md" << 'ENDOFPR'
## Summary

This branch ...

## Review walkthrough

- Start with [path/to/file.ext](...) to see ...

## Validation

- `command`: result
ENDOFPR

gh pr create --draft --title "<title>" --body-file "$PR_BODY_DIR/body.md"
rm -rf "$PR_BODY_DIR"
```

The quoted `ENDOFPR` marker is mandatory. It prevents shell expansion from
dumping variables, command output, backticked code spans, or escape sequences
into the pull request description.

## File links

Use Markdown file links, not bare paths, for every file mentioned in the pull
request description.

Prefer commit-specific links when the commit is already pushed and stable:

```markdown
[docs/execplans/example.md](https://github.com/OWNER/REPO/blob/COMMIT/docs/execplans/example.md)
```

Use branch-ref links when the commit may still change before review:

```markdown
[docs/execplans/example.md](https://github.com/OWNER/REPO/blob/BRANCH/docs/execplans/example.md)
```

Add line anchors when they help reviewers land directly on the relevant
context:

```markdown
[docs/execplans/example.md](https://github.com/OWNER/REPO/blob/COMMIT/docs/execplans/example.md#L12)
```

## Final check

Before creating the draft pull request, verify that:

- the pull request is marked as draft;
- the title includes every required roadmap or issue reference;
- the execplan is linked, and its implementation status is clear;
- `Closes #123` appears when an issue is being closed;
- the opening paragraph states what changed and why;
- the walkthrough gives reviewers purpose-first entrypoints;
- every file reference is a Markdown link to a commit or branch ref; and
- the prose uses third-person en-GB Oxford English.
