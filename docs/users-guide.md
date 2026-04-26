# Users' Guide

*How to use df12 documentation workflow skills together.*

This guide is for documentation practitioners using the skills in this
repository to prepare branch hand-offs, commit history and pull request review
surfaces. It gives the operating flow; each skill file remains the authority
for detailed rules.

______________________________________________________________________

## Workflow overview

Use the skills as a sequence rather than isolated snippets:

1. Draft or update the documentation artefact in the target repository.
2. Validate the edited files with the repository's documented gates.
3. Use [`commit-message`](../skills/commit-message/SKILL.md) to write a
   file-backed Git commit message.
4. Use [`pr-creation`](../skills/pr-creation/SKILL.md) to prepare the pull
   request title and description from the full branch diff.

This keeps the branch narrative consistent from local commit to pull request
review.

______________________________________________________________________

## Commit messages

Use [`commit-message`](../skills/commit-message/SKILL.md) when staging or
committing documentation changes.

The skill requires a temporary message file and `git commit -F`. This avoids
inline shell quoting problems, accidental command substitution and unreadable
multi-line `git commit -m` invocations.

A good commit message states the behavioural or documentation effect first,
then explains why the change was needed when that is not obvious from the
summary.

______________________________________________________________________

## Pull request descriptions

Use [`pr-creation`](../skills/pr-creation/SKILL.md) when opening or revising a
pull request.

The skill requires pull requests to be created as drafts and the description to
cover the full branch, not only the latest commit. Start with what changed and
why, then give reviewers purpose-first entrypoints into the files they should
read.

Write the pull request body to a temporary Markdown file with a single-quoted
heredoc delimiter before passing it to GitHub tooling. This protects the
description from shell expansion of variables, command output, backticked code
spans and escape sequences.

______________________________________________________________________

## Review references

When a branch follows an issue, include the issue reference in the pull request
title and add the required closure text in the description. When a branch
follows a roadmap task, include the task reference in the title and explain how
the branch satisfies the task.

If an execplan exists, link it from the pull request description and state
whether the branch implements it or carries a pre-implementation plan.

Use Markdown links for every file mentioned in the pull request description.
Prefer commit-specific links after the branch has been pushed.

______________________________________________________________________

## Validation evidence

Record validation commands in the pull request description after the review
walkthrough. For skill documentation changes, the usual focused checks are:

```bash
SKILL_CREATOR="${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator"
uv run --with pyyaml python \
  "$SKILL_CREATOR/scripts/quick_validate.py" \
  skills/<skill-name>
markdownlint-cli2 README.md skills/<skill-name>/SKILL.md
git diff --check
```

Run broader repository gates when the project defines them. If a broader gate
fails on pre-existing files outside the branch scope, report that clearly and
keep the focused evidence for touched files visible.
