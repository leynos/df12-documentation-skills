# Agent scenario artefacts, 21 November 2026

These are the artefacts produced by the revalidation of the twelve agent
scenarios that exercise `terms-of-reference-doc` and `tech-design-doc` with the
architecture-contract version of `execplans`. The verdicts are recorded in
[the validation document](../../architecture-contract-validation.md#run-records).

The revalidation ran because the evaluated skill text changed: the non-goal
guidance in `terms-of-reference-doc/references/elicitation-protocol.md`
prescribed a list-length target ("until the lists are roughly comparable") while
`SKILL.md` prohibits inventing non-goals to meet a numerical quota. The
reference was corrected, so the earlier campaign's verdicts no longer applied
to the shipped text. That campaign remains published under
[`2026-11-19-agent-scenarios/`](../2026-11-19-agent-scenarios/README.md) as the
record of the text those runs read.

## Status of this evidence

These verdicts are manual evidence, not CI results. `make test` does not run
the scenarios, no file here is an independent human review, and the verdicts in
the validation document are a reviewer's comparison of these artefacts with its
oracles. Ten of the twelve runs carry confirmed defects, catalogued in the same
document, so a verdict records the position a run took, not the soundness of
every sentence in its output. The mechanical boundary checks in
`tests/test_workflow_boundary_contract.py` remain scoped to the 19 November
artefacts, whose phrasing they were calibrated against; their behaviour on this
campaign is recorded in the validation document rather than used as a gate.

## Run configuration

- Agent: Claude Code subagent, `general-purpose` type, model
  `deepseek-v4.1-flash-1017`.
- Skill tree: `2f1864f8d9f089d57cd6125d943d052b91668e33`, the value of
  `git rev-parse <revision>:skills` after the elicitation correction. The 19
  November campaign ran on `fffbba004a77cd117a54f73b0ca9172861bf3bd5`.
- Installed `execplans` skill: content hash
  `4fdba07976ac6a6f3b93bae5aa750230a0149379`.
- Run date: 21 November 2026. Each prompt names its own output directory under
  `/tmp/val2-<scenario>`.

## Run inputs

`inputs/` holds the exact text sent to each run. The eleven prompts that the
earlier campaign also used are byte-identical to those inputs apart from the
output directory. The C3 prompt is the earlier campaign's second C3 run, with
the output directory changed: it states the isolation rule without the first
run's contradiction and names the three artefacts explicitly.

| File            | Scenario |
| --------------- | -------- |
| `inputs/c1.txt` | C1       |
| `inputs/c2.txt` | C2       |
| `inputs/c3.txt` | C3       |
| `inputs/c4.txt` | C4       |
| `inputs/c5.txt` | C5       |
| `inputs/c6.txt` | C6       |
| `inputs/e1.txt` | E1       |
| `inputs/e2.txt` | E2       |
| `inputs/e3.txt` | E3       |
| `inputs/e4.txt` | E4       |
| `inputs/s1.txt` | S1       |
| `inputs/s2.txt` | S2       |

The prompts name the skill directories, the installed `execplans` skill, and an
output directory. They contain no oracle and no statement of the expected
verdict; the review in
[the validation document](../../architecture-contract-validation.md#run-records)
is what supplies that comparison.

## Conventions

Markdown outputs are stored as `.md.txt`. They are evidence, so they are kept
verbatim rather than reformatted by the repository's Markdown gates; the suffix
keeps them out of those gates without an exclusion rule. `SHA256SUMS` records
the digest of every file, so a later edit to any artefact is detectable. The
README digest is recorded first, and the remaining paths follow in `LC_ALL=C`
order, as in the earlier campaign.

## Contents

| Scenario | Directory | Files                                                                                                                                              |
| -------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| C1       | `c1/`     | `api-surface-compatibility-assessment.md.txt`, `execplan-replace-internal-method-signature.md.txt`                                                 |
| C2       | `c2/`     | `execplan.md.txt`, `tech-design.md.txt`, `tech-design-outline.md.txt`, `terms-of-reference.md.txt`                                                 |
| C3       | `c3/`     | `execplan-record.md.txt`, `tech-design.md.txt`, `terms-of-reference.md.txt`                                                                        |
| C4       | `c4/`     | `execplan.md.txt`, `tech-design.md.txt`, `terms-of-reference.md.txt`                                                                               |
| C5       | `c5/`     | `00-intake-and-elicitation.md.txt`, `01-terms-of-reference-constraint-record.md.txt`, `02-technical-design.md.txt`, `03-execplan.md.txt`           |
| C6       | `c6/`     | `execplan.md.txt`, `record-format-v2.md.txt`, `tech-design.md.txt`, `terms-of-reference.md.txt`, `working-notes.md.txt`                            |
| E1       | `e1/`     | `01-terms-of-reference-feedback.md.txt`, `02-technical-design-and-adr-impact.md.txt`, `03-execplan-supervisor-worker-shutdown.md.txt`              |
| E2       | `e2/`     | `execplan-chunk-and-benchmark-evidence.md.txt`, `tech-design-verification-update.md.txt`                                                           |
| E3       | `e3/`     | `01-status-reconciliation.md.txt`, `02-tracker-correction-proposal.md.txt`, `03-evidence-request-and-handoff.md.txt`                               |
| E4       | `e4/`     | `00-contract-revision-impact.md.txt`, `01-execplan-revision.md.txt`, `02-upstream-change-feedback.md.txt`, `03-decision-request.md.txt`            |
| S1       | `s1/`     | `intake-note.md.txt`, `technical-design-intake-and-outline.md.txt`, `terms-of-reference.md.txt`                                                    |
| S2       | `s2/`     | `change-control-record.md.txt`, `design-adr-amendment-request.md.txt`, `execplan-deviation-entry.md.txt`, `hardening-recommendation-triage.md.txt` |
