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

- Create new pull requests as draft by default, but preserve the current
  draft/ready state when editing an existing pull request.
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

## Draft state rules

- When creating a new pull request, create it as a draft unless the user
  explicitly asks for a ready-for-review PR.
- When updating, revising, or refreshing an existing pull request, preserve
  the pull request's current draft/ready state.
- Do not convert an existing ready-for-review pull request back to draft
  unless the user explicitly asks for that transition.
- Do not mark an existing draft pull request ready for review unless the
  user explicitly asks for that transition.
- If the current draft state cannot be read, update only the
  title/body/metadata requested and leave review readiness unchanged.

## Gather required context

Before opening or revising the pull request, identify:

- whether an existing pull request already exists for the branch;
- if an existing pull request exists, whether it is currently draft or
  ready for review;
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
cleanup_pr_body() {
  if [ -e "$PR_BODY_DIR/body.md" ] || [ -L "$PR_BODY_DIR/body.md" ]; then
    unlink "$PR_BODY_DIR/body.md"
  fi
  rmdir "$PR_BODY_DIR"
}
trap cleanup_pr_body EXIT

cat > "$PR_BODY_DIR/body.md" << 'ENDOFPR'
## Summary

This branch ...

## Review walkthrough

- Start with [path/to/file.ext](...) to see ...

## Validation

- `command`: result
ENDOFPR

gh pr create --draft --title "<title>" --body-file "$PR_BODY_DIR/body.md"
trap - EXIT
cleanup_pr_body
```

The quoted `ENDOFPR` marker is mandatory. It prevents shell expansion from
dumping variables, command output, backticked code spans, or escape sequences
into the pull request description.

## File links

Use GFM-style Markdown file links, not bare paths, for every file mentioned in
the pull request description. Point each file link at the relevant lines with
a GFM line anchor, and use a branch ref so the link remains available after the
pull request merges.

Do not use a commit SHA for a file link merely because the commit is already
pushed. Link to a specific commit SHA only when the description references an
issue in that exact commit.

```markdown
[docs/execplans/example.md](https://github.com/OWNER/REPO/blob/BRANCH/docs/execplans/example.md#L12)
```

## Final check

Before creating the draft pull request, verify that:

- for a newly created pull request, the pull request is marked as draft
  unless explicitly requested otherwise;
- for an existing pull request, the previous draft/ready state has been
  preserved unless the user explicitly requested a state change;
- the title includes every required roadmap or issue reference;
- the execplan is linked, and its implementation status is clear;
- `Closes #123` appears when an issue is being closed;
- the opening paragraph states what changed and why;
- the walkthrough gives reviewers purpose-first entrypoints;
- validation commands and results are recorded as code blocks or log links,
  including skill validation, lint or lint-staged output, and diff checks;
- every file reference is a GFM Markdown link to a branch ref with a line
  anchor, except for a specific-commit issue reference; and
- the prose uses third-person en-GB Oxford English.
