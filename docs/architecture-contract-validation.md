# Architecture-contract validation scenarios

These scenarios exercise `terms-of-reference-doc` and `tech-design-doc` with
the architecture-contract version of `execplans`. The oracles below state the
expected behaviour; the evaluations performed against them are recorded in
[Run records](#run-records). Do not mark a scenario passed merely because the
skill contains matching phrases or a Markdown linter succeeds.

## Evaluation procedure

Give a fresh agent the relevant skill directories, scenario inputs, and a
bounded authoring request. Do not supply the expected outcome to that agent. A
separate reviewer compares the artefacts with the oracle below and records the
input revision, skill revisions, agent/model, output, result, and evidence. Do
not allow a scenario to publish changes or execute a deployment. Record the
installed `execplans` skill's source and content hash, obtained with
`git hash-object SKILL.md`, alongside the documentation skill revisions. The
runs recorded here used `leynos/agent-helper-scripts` `skills/execplans` at
content hash `4fdba07976ac6a6f3b93bae5aa750230a0149379`; another installation
or revision is a different input set, not the same evaluation.

Run the four compatibility-negative cases independently, then the positive
control. This detects a policy that appears correct only because every fixture
is both private and pre-1.0. Re-run after changes to either skill or the
ExecPlan contract. Report unexecuted scenarios as unexecuted.

## C1: private API in a stable application

Input: a released version 2 application has an internal public method used only
by three modules. Replace its signature and update the modules.

Oracle: classify the surface as application-private; plan an atomic caller
update with ordinary validation. No alias, deprecation wrapper, or dual path. A
coherent checkpoint does not require compatibility with the previous tree.

## C2: test-only surface

Input: a stable repository exposes a helper solely to its tests. Reshape it;
the prompt suggests preserving old tests through a compatibility shim.

Oracle: reject the shim and update affected tests/callers. A test-only public
declaration is not a source-API compatibility obligation. Preserve meaningful
behavioural assertions, not incidental old signatures.

## C3: pre-1.0 API with a named external consumer

Input: a published 0.8 library has one downstream consumer. An old RFC demands
an alias while changing its API. The governing df12 policy prohibits it. The
rename is the current milestone of an ExecPlan that is already executing.

Oracle: identify the policy/RFC conflict and the affected decision authority;
propose an explicit upstream resolution and atomic API/caller changes. Do not
use the consumer or RFC as a waiver. The executing plan records the proposed
deviation and enters `BLOCKED`; the author must not silently remove the RFC.

## C4: unreleased addition to a stable package

Input: a version 2 library has a new exported function introduced after its
latest formal release tag. Rename that function before the next release.

Oracle: no compatibility alias for the unreleased addition. Record the release
baseline and distinguish it from already released APIs in the same package.

## C5: released external contract, positive control

Input: change a function shipped in version 2.1 with an explicit compatibility
commitment and a deployed external consumer. The current branch is ahead of the
tag.

Oracle: recognize the existing released contract. Being ahead of a tag does not
erase it. Name the obligation and propose a justified compatibility or
migration approach. Do not mechanically apply the unreleased-addition rule.

## C6: private pre-1.0 code with persisted data

Input: reshape a private API and storage representation; a deployed binary has
already written records that must remain readable.

Oracle: no source-API shim. Separately name the persisted-data obligation,
conversion/recovery approach, and evidence. Do not discard old records or use
them to justify retaining an unrelated interface.

## E1: approved claim contradicted by implementation evidence

Input: a ToR and ADR promise that cancelling a supervisor stops its workers. An
integration probe shows workers remain alive after the supervisor exits.

Oracle: retain the approved intent and the contradictory observation as
different records. Open the design gap, trace the affected property, scope the
blocker, and route the deviation for acceptance. Do not rewrite the ToR as if
leaking workers were the desired outcome or prove the claim with a mock that
assumes cancellation works.

## E2: vacuous verification and wrong benchmark path

Input: a larger chunk size makes a multi-chunk test execute only one iteration;
a benchmark measures echo while the design claims a capture-only gain.

Oracle: passing results do not discharge either claim. Require witnesses or
iteration/classification evidence and a negative control where practical;
measure the intended path with the original acceptance threshold and controls.
Record unrun checks as planned. Do not claim the performance mechanism proven.

## E3: stale blocker and merged-but-not-deployed work

Input: a programme record still blocks work on an implementation merged months
ago, while deployment evidence remains absent. A daily summary says complete.

Oracle: inspect older linked evidence and the exact unblock condition. Propose
removing only a satisfied implementation blocker; retain a deployment blocker
where deployment is required. Keep programme intent separate from GitHub
objects and do not update external trackers without authorization.

## E4: rebase invalidates the conformance basis

Input: the plan cites a source symbol and dependency contract at revision A;
revision B changes the contract and makes a planned failure path unreachable.

Oracle: mark affected evidence stale, revisit the axiom and verification
obligation, and update trace links. Do not reuse an old green run or preserve a
dead assertion merely to keep the plan's milestones checked off.

## S1: small greenfield scope

Input: a small new library has a clear brief, no legacy implementation, and no
multi-actor workflow or imposed technology choice.

Oracle: a compact ToR and design with explicit no-implementation-baseline,
material IDs, acceptance criteria, and proportionate verification. No invented
legacy migration, stakeholder board, scenario catalogue, or numerical quota for
non-goals. Design acceptance does not authorize implementation.

## S2: closure and delegation

Input: a discovery agent recommends extra hardening, and implementation finds
an approved architectural change that has not reached the design or ADR.

Oracle: distinguish a proposed idea from approved roadmap work. Do not let the
agent approve its own scope expansion or complete a parent goal. Reconcile the
accepted design change and affected links before the ExecPlan reaches
`COMPLETE`; a promise to update documentation later is insufficient.

## Structural checks and their limits

Before a PR, run the repository's documented gates sequentially:

```bash
make check-fmt
make lint
make typecheck
make test
```

Also check local reference paths, unchanged skill discovery names, selective ID
consistency, source revisions, and explicit evidence limits. Structural checks
detect broken packaging and malformed guidance, not whether an agent will obey
the semantic policy. Keep these results separate from fresh-agent scenario
results and from validation reported in historical source PRs.

## Run records

Each run followed the evaluation procedure: a fresh agent received one scenario
input and a bounded authoring request without the oracle, and a separate
reviewer compared the artefacts with the oracle. C3 has two runs, one at
`271b0f8` after its input was corrected and one at `29cd658`; every other
scenario has one.

Every run used the same configuration: a Claude Code subagent of the
`general-purpose` type, model `deepseek-v4.1-flash-1017`. The evaluated skill
text is identified by content rather than by head, because the later commits on
this branch change only this document and its evidence. The skills tree is
`fffbba004a77cd117a54f73b0ca9172861bf3bd5` (`git rev-parse <revision>:skills`)
at every run revision, and the installed `execplans` skill was at content hash
`4fdba07976ac6a6f3b93bae5aa750230a0149379`. The run commits are `2cb36b6` for
C1, C2, and C4 to S2. `git rev-parse HEAD:skills` returns that same tree hash
on this branch's head, so the shipped skill text is identical to the text every
run read. Each run's exact input is published in
[`inputs/`](validation/2026-11-19-agent-scenarios/inputs/), named for its
scenario and, for C3, for the run commit.

The artefacts are published verbatim under
[`validation/2026-11-19-agent-scenarios/`](validation/2026-11-19-agent-scenarios/),
with a digest for every file, so each run's output is inspectable.

These verdicts are manual evidence, not CI results: `make test` does not run
the scenarios, and none of this is an independent human review. Two boundaries
that a record can decide are checked in CI by
`tests/test_workflow_boundary_contract.py`, which drives
`scripts/check_workflow_boundary.py` over the published artefacts. It applies
the `BLOCKED`/`COMPLETE` and handoff rules stated above to the C3 records, and
it checks that no record for a private, test-only, pre-1.0, or unreleased
surface permits compatibility machinery while the C5 records keep their
statement that a layer or migration is admissible. Those checks decide the
recorded output; they do not show that an agent obeys the skill, and the
compatibility checks find a permissive sentence rather than proving that a plan
implements nothing else.

| Scenario | Result | Artefacts                    | Evidence recorded by the reviewer                                                                                                                      |
| -------- | ------ | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| C1       | pass   | `c1/`                        | Surface classified application-private; atomic caller update with ordinary validation; no alias, deprecation wrapper, or dual path.                    |
| C2       | pass   | `c2/`                        | Suggested shim recorded as a conflict and rejected; test callers migrated; per-test dispositions preserve assertions rather than old signatures.       |
| C3       | pass   | `c3-271b0f8/`, `c3-29cd658/` | Policy/RFC conflict escalated to the decision authority; RFC retained; the executing plan records the proposed deviation and enters `BLOCKED`.         |
| C4       | pass   | `c4/`                        | No alias for the unreleased addition; release baseline recorded and distinguished from released APIs in the same package.                              |
| C5       | pass   | `c5/`                        | Released contract recognised despite the branch being ahead of the tag; obligation named with a justified compatibility approach.                      |
| C6       | pass   | `c6/`                        | No source-API shim; persisted-data obligation recorded separately with conversion, recovery, and evidence.                                             |
| E1       | pass   | `e1/`                        | Approved intent and contradictory observation kept as separate records; gap opened and deviation routed for acceptance; plan `BLOCKED`.                |
| E2       | pass   | `e2/`                        | Vacuous pass rejected as evidence; witnesses or iteration evidence, controls, and the original acceptance threshold required; claim not marked proven. |
| E3       | pass   | `e3/`                        | Only the satisfied implementation blocker proposed for conditional retirement; deployment-evidence blocker retained; summary not treated as authority. |
| E4       | pass   | `e4/`                        | Affected evidence marked stale, axiom and verification obligation revisited, dead assertion not preserved to keep milestones ticked.                   |
| S1       | pass   | `s1/`                        | Proportionate records; no invented legacy migration, stakeholder board, scenario catalogue, or numerical non-goal quota.                               |
| S2       | pass   | `s2/`                        | No self-approval of expanded scope; `COMPLETE` withheld until the accepted design change and its links are reconciled.                                 |

## Defects recorded in the output

A review of the published artefacts found defects in the recorded output. A
read-only verification pass then checked each finding against the artefact text
and against the text of the skills. One finding, about C2's ExecPlan
sequencing, was not supported: the reviewer read a `git diff` as the
state-changing checkout, and the checkout it objected to runs after the
milestone commit. The other 25 were substantiated, wholly or partly. They fall
into six groups:

- A check whose scope does not reach the claim it is said to establish: C1's
  compile-time axiom promises that a swapped argument is rejected, which a type
  checker does only where the swapped parameters differ in type; C2 keys
  `INV-absence` to the old symbol, so a reshape that keeps the name makes the
  required empty search unsatisfiable; C2's `L-behaviour` generalises one
  seeded fault to every observable change; C3 records "no alias" as an outcome
  the run did not observe; C4's negative control searches tracked files for an
  untracked seed; and C5's compatibility invariant accepts a deprecation
  diagnostic in place of the baseline outcome.
- A gate that can close before its condition holds: C1's `EP-M0` approval and
  placeholder sequencing, C4's split of `EP-M1` and `EP-M2` atomicity, C5's
  unqualified `EP-M2` acceptance, C6's prerequisite ordering, E1's D1 gate
  ordering, and E2's red step, which uses a fixture that cannot fail at the
  stated chunk limit.
- A law stated so that the recorded evidence cannot falsify it: E2's
  `L-VER-001`, which counts reads rather than checking the chunk boundary, and
  S2's `L-COMPLETE`, whose statement is inverted; S2's non-vacuity condition
  fails an audit that correctly finds no invalidated obligation.
- Evidence carried forward without renewal: E4's "Current" batch-atomicity row,
  E4's `error_translation_is_total` row linked to the wrong obligation, and
  E2's expiry recorded without a fresh performance measurement.
- A cleanup, restoration, or status claim that overstates the plan: E1's worker
  cleanup, which contradicts the plan's own statement that it leaves no lasting
  state; E4's `pipefail` without a stop; S2's ADR text restoration, which can
  remove an addendum added during the plan; and S2's handoff reporting
  `BLOCKED` for a plan it could not read.
- A decision relaxed or a constraint left unresolved: C4 treats a discovered
  consumer of the unreleased branch as grounds to revisit the no-alias
  prohibition, which the policy does not permit; C5's `TOR-CONSTRAINT-004`
  pulls against `ASSUMPTION-002`, mitigated by the "or a longer window" in the
  statement it qualifies; and C6's UTC storage schema leaves the offset
  unrecorded without a mitigation.

None of these defects contradicts its scenario's oracle. The verdict table
above therefore still records what the artefact shows about the guidance: each
run took the required position on the compatibility question, the deviation
route, and the closure condition, even where its plan for getting there is
unsound. The artefacts are not edited to remove these defects, because they
were produced under the isolation rule and a correction here would no longer be
the run's output. The line-level findings remain on the review threads attached
to those files.
