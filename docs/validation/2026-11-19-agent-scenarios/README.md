# Agent scenario artefacts, 19 November 2026

These are the artefacts produced by the fresh-agent evaluations of
`terms-of-reference-doc` and `tech-design-doc` whose verdicts are recorded in
[the validation document](../../architecture-contract-validation.md#run-records).
Each scenario ran in a fresh agent that was given the two skill directories,
the installed `execplans` skill, and one scenario input, and was instructed to
read nothing else, so no authoring agent saw the oracle or the rest of the
repository.

## Status of this evidence

These verdicts are manual evidence, not CI results. `make test` does not run
the scenarios, no file here is an independent human review, and the verdicts in
the validation document are a reviewer's comparison of these artefacts with its
oracles. CI reads two of the C3 artefacts through
`tests/test_workflow_boundary_contract.py`, which checks the documented
`BLOCKED`/`COMPLETE` and handoff rules against the recorded output; that check
decides a boundary of the recorded artefacts, not whether an agent obeys the
skill.

## Run configuration

- Agent: Claude Code subagent, `general-purpose` type, model
  `deepseek-v4.1-flash-1017`.
- Skill tree: `fffbba004a77cd117a54f73b0ca9172861bf3bd5`, the value of
  `git rev-parse <revision>:skills` at every run.
- Installed `execplans` skill: content hash
  `4fdba07976ac6a6f3b93bae5aa750230a0149379`.
- Run commits: `2cb36b6` for C1, C2, and C4 to S2; `271b0f8` for the first C3
  run; `29cd658` for the second C3 run, which also produced a design.

## Run inputs

`inputs/` holds the exact text sent to each run, so the artefacts can be
reproduced from the same starting conditions. Each file is one prompt, recorded
verbatim from the dispatching session; nothing was paraphrased or tidied
afterwards. The two C3 prompts differ: the first asked for the artefacts the
skills call for and left the choice open, which yielded a terms of reference
and an ExecPlan; the second named the three artefacts explicitly.

| File                    | Scenario and run                 |
| ----------------------- | -------------------------------- |
| `inputs/c1.txt`         | C1                               |
| `inputs/c2.txt`         | C2                               |
| `inputs/c3-271b0f8.txt` | C3, first run, commit `271b0f8`  |
| `inputs/c3-29cd658.txt` | C3, second run, commit `29cd658` |
| `inputs/c4.txt`         | C4                               |
| `inputs/c5.txt`         | C5                               |
| `inputs/c6.txt`         | C6                               |
| `inputs/e1.txt`         | E1                               |
| `inputs/e2.txt`         | E2                               |
| `inputs/e3.txt`         | E3                               |
| `inputs/e4.txt`         | E4                               |
| `inputs/s1.txt`         | S1                               |
| `inputs/s2.txt`         | S2                               |

The prompts name the skill directories, the installed `execplans` skill, and an
output directory. They contain no oracle and no statement of the expected
verdict; the review of the output in
[the validation document](../../architecture-contract-validation.md#defects-recorded-in-the-output)
is what supplies that comparison.

The first C3 prompt carries a conflict. Its isolation rule forbids reading
anything under `/home/leynos/.lody/repos`, and two of the three skill
directories it permits lie under that path. The file is kept verbatim as the
record of what the run received; a replay correction at
[`replay-corrections/c3-271b0f8.md`](replay-corrections/c3-271b0f8.md) supplies
a reconciled isolation rule without altering the scenario.

## Replay corrections

`replay-corrections/` records corrections that make a published scenario
replayable without changing what the original run received. A correction
restates the part of a prompt that cannot be followed as written; the published
input and the artefacts stay as they were produced, and the correction is not
evidence about the behaviour of the original run.

| File                               | Run                  | Correction                                               |
| ---------------------------------- | -------------------- | -------------------------------------------------------- |
| `replay-corrections/c3-271b0f8.md` | C3, commit `271b0f8` | Isolation rule reconciled with the permitted skill paths |

## Conventions

Markdown outputs are stored as `.md.txt`. They are evidence, so they are kept
verbatim rather than reformatted by the repository's Markdown gates; the suffix
keeps them out of those gates without an exclusion rule. The JSON schema keeps
its own extension. `SHA256SUMS` records the digest of every file, so a later
edit to any artefact is detectable.

## Contents

| Scenario | Directory     | Files                                                                                                                                                                                    |
| -------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C1       | `c1/`         | `01-terms-of-reference.md.txt`, `02-technical-design.md.txt`, `03-execplan.md.txt`                                                                                                       |
| C2       | `c2/`         | `intake-note.md.txt`, `terms-of-reference.md.txt`, `tech-design.md.txt`, `execplan.md.txt`                                                                                               |
| C3       | `c3-271b0f8/` | `terms-of-reference.md.txt`, `execplan-library-api-rename.md.txt`                                                                                                                        |
| C3       | `c3-29cd658/` | `terms-of-reference.md.txt`, `tech-design.md.txt`, `execplan-record.md.txt`                                                                                                              |
| C4       | `c4/`         | `handoff.md.txt`, `execplan-rename-unreleased-export.md.txt`                                                                                                                             |
| C5       | `c5/`         | `terms-of-reference.md.txt`, `tech-design.md.txt`, `execplan.md.txt`                                                                                                                     |
| C6       | `c6/`         | `outline.md.txt`, `tech-design.md.txt`, `execplan.md.txt`, `storage-record-v2.schema.json`                                                                                               |
| E1       | `e1/`         | `tor-cancel-stops-workers-reconciliation.md.txt`, `adr-design-deviation-proposal.md.txt`, `execplan-cancel-supervisor-stops-workers.md.txt`                                              |
| E2       | `e2/`         | `capture-path-verification-amendment.md.txt`, `capture-path-evidence-execplan.md.txt`                                                                                                    |
| E3       | `e3/`         | `phase0-intake-working-note.md.txt`, `terms-of-reference-addendum-dependencies-and-evidence.md.txt`, `proposed-record-corrections.md.txt`                                                |
| E4       | `e4/`         | `evidence-freshness-recheck.md.txt`, `execplan.md.txt`                                                                                                                                   |
| S1       | `s1/`         | `intake-notes.md.txt`, `terms-of-reference.md.txt`, `design-and-execution-readiness.md.txt`                                                                                              |
| S2       | `s2/`         | `01-intake-and-disposition.md.txt`, `02-gap-register-and-design-change.md.txt`, `03-adr-candidate.md.txt`, `04-execplan-deviation-record.md.txt`, `05-handoff-and-open-questions.md.txt` |
