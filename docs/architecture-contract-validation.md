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
reviewer compared the artefacts with the oracle. Two campaigns have run. The
first, on 19 November 2026, evaluated skill tree
`fffbba004a77cd117a54f73b0ca9172861bf3bd5`. The second, on 21 November 2026,
reran the same twelve scenarios on tree
`2f1864f8d9f089d57cd6125d943d052b91668e33` after the elicitation reference was
corrected.

### Campaign of 19 November 2026

C3 has two runs, one at `271b0f8` and one at `29cd658`; every other scenario
has one.

The first C3 input conflicts with itself: it permits three skill directories
and then forbids reading anything under `/home/leynos/.lody/repos`, which
contains two of them. The input is published verbatim, because it is what the
run received. A replay correction at
[`replay-corrections/c3-271b0f8.md`](validation/2026-11-19-agent-scenarios/replay-corrections/c3-271b0f8.md)
supplies a reconciled isolation rule for the same scenario, and the second C3
prompt already states the rule without the contradiction.

Every run in this campaign used the same configuration: a Claude Code subagent
of the `general-purpose` type, model `deepseek-v4.1-flash-1017`. The evaluated
skill text is identified by content rather than by head, because the commits
that followed changed only this document and its evidence. The skills tree was
`fffbba004a77cd117a54f73b0ca9172861bf3bd5` (`git rev-parse <revision>:skills`)
at every run revision, and the installed `execplans` skill was at content hash
`4fdba07976ac6a6f3b93bae5aa750230a0149379`. The run commits are `2cb36b6` for
C1, C2, and C4 to S2. A later correction to the elicitation reference changed
the shipped tree, so the revalidation below evaluated different skill text;
neither campaign's verdicts are carried into the other. Each run's exact input
is published in [`inputs/`](validation/2026-11-19-agent-scenarios/inputs/),
named for its scenario and, for C3, for the run commit.

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

| Scenario | Result               | Artefacts                    | Evidence recorded by the reviewer                                                                                                                                                                                                                                                           |
| -------- | -------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C1       | pass                 | `c1/`                        | Surface classified application-private; atomic caller update with ordinary validation; no alias, deprecation wrapper, or dual path.                                                                                                                                                         |
| C2       | pass                 | `c2/`                        | Suggested shim recorded as a conflict and rejected; test callers migrated; per-test dispositions preserve assertions rather than old signatures.                                                                                                                                            |
| C3       | pass                 | `c3-271b0f8/`, `c3-29cd658/` | Policy/RFC conflict escalated to the decision authority; RFC retained; the executing plan records the proposed deviation and enters `BLOCKED`.                                                                                                                                              |
| C4       | pass with limitation | `c4/`                        | No alias for the unreleased addition; release baseline recorded and distinguished from released APIs in the same package. The run then records that a discovered consumer triggers escalation and the released-surface compatibility rules apply instead, which the policy does not permit. |
| C5       | pass                 | `c5/`                        | Released contract recognised despite the branch being ahead of the tag; obligation named with a justified compatibility approach.                                                                                                                                                           |
| C6       | pass                 | `c6/`                        | No source-API shim; persisted-data obligation recorded separately with conversion, recovery, and evidence.                                                                                                                                                                                  |
| E1       | pass                 | `e1/`                        | Approved intent and contradictory observation kept as separate records; gap opened and deviation routed for acceptance; plan `BLOCKED`.                                                                                                                                                     |
| E2       | pass                 | `e2/`                        | Vacuous pass rejected as evidence; witnesses or iteration evidence, controls, and the original acceptance threshold required; claim not marked proven.                                                                                                                                      |
| E3       | pass                 | `e3/`                        | Only the satisfied implementation blocker proposed for conditional retirement; deployment-evidence blocker retained; summary not treated as authority.                                                                                                                                      |
| E4       | pass                 | `e4/`                        | Affected evidence marked stale, axiom and verification obligation revisited, dead assertion not preserved to keep milestones ticked.                                                                                                                                                        |
| S1       | pass                 | `s1/`                        | Proportionate records; no invented legacy migration, stakeholder board, scenario catalogue, or numerical non-goal quota.                                                                                                                                                                    |
| S2       | pass                 | `s2/`                        | No self-approval of expanded scope; `COMPLETE` withheld until the accepted design change and its links are reconciled.                                                                                                                                                                      |

### Revalidation of 21 November 2026

The 19 November review found that
`skills/terms-of-reference-doc/references/elicitation-protocol.md` required
goals and non-goals lists to be "roughly comparable", while the same skill's
`SKILL.md` prohibits inventing non-goals to meet a numerical quota. The
reference now says the count is not the test and asks the user to cut goals or
name exclusions a reasonable reader would assume are in scope. The reference is
part of the evaluated skill text, so the twelve scenarios were rerun rather
than carried forward.

The configuration matched the first campaign: a Claude Code subagent of the
`general-purpose` type, model `deepseek-v4.1-flash-1017`, with `execplans` at
content hash `4fdba07976ac6a6f3b93bae5aa750230a0149379`. The skills tree was
`2f1864f8d9f089d57cd6125d943d052b91668e33`. Inputs and artefacts are published
under
[`validation/2026-11-21-agent-scenarios/`](validation/2026-11-21-agent-scenarios/),
with a digest for every file. Eleven prompts are byte-identical to the 19
November inputs apart from the output directory; the C3 prompt is the earlier
campaign's second C3 run, which states the isolation rule without the first
run's contradiction.

The `Defects` column counts the confirmed findings recorded
[below](#defects-recorded-in-the-output). It does not change the result, which
records the position the artefact took on its oracle, not the soundness of
every sentence it contains.

| Scenario | Result | Artefacts | Evidence recorded by the reviewer                                                                                                                                                                           | Defects |
| -------- | ------ | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| C1       | pass   | `c1/`     | Surface classified as an application-internal public declaration, so a private API; no alias, deprecated entrypoint, wrapper, or dual path; the signature and all three callers change atomically.          | none    |
| C2       | pass   | `c2/`     | Suggested shim recorded as `TOR-CONFLICT-001` and rejected; every test caller migrates; no old interface, alias, or dual path survives.                                                                     | none    |
| C3       | pass   | `c3/`     | Policy/RFC conflict escalated to the decision authority; RFC not rewritten, deleted, or retro-edited; the plan record sets `BLOCKED` with a proposed deviation entry and names the upstream resolution.     | 1       |
| C4       | pass   | `c4/`     | Release baseline recorded and left `[OPEN]` for the unnamed tag; no alias for the unreleased export; a development-branch consumer creates no obligation.                                                   | 3       |
| C5       | pass   | `c5/`     | Released 2.1 contract recognised despite the branch being ahead of the tag; compatibility or a deliberate migration stated as required and permitted; new entry point, deprecation, and consumer migration. | none    |
| C6       | pass   | `c6/`     | No source-API shim; persisted records handled as a separate deployed-data obligation with a v2 format, read path, and migration.                                                                            | 2       |
| E1       | pass   | `e1/`     | Promise and probe kept as separate records; gap and affected properties scoped; deviation `D1` routed for acceptance; plan `BLOCKED`.                                                                       | 2       |
| E2       | pass   | `e2/`     | Passing results rejected as evidence for both claims; witnesses, iteration evidence, a negative control, and the original threshold required; claims recorded as unproven.                                  | none    |
| E3       | pass   | `e3/`     | Only the implementation-scoped blocker conditionally retired; deployment blocker retained; daily summary treated as a lead, not authority; external state unchanged.                                        | none    |
| E4       | pass   | `e4/`     | Revision-A evidence marked stale; the dependency axiom revisited as `AXIOM-DEP-B`; the unreachable failure obligation replaced; plan `BLOCKED`.                                                             | 3       |
| S1       | pass   | `s1/`     | Proportionate records; explicit no-baseline; material gaps marked `[OPEN]`; no invented migration, stakeholder board, catalogue, or numerical non-goal quota.                                               | 1       |
| S2       | pass   | `s2/`     | Recommendation not self-approved; the architectural change recorded as claimed-unverified; `COMPLETE` withheld; plan `BLOCKED` pending reconciliation.                                                      | 1       |

The mechanical boundary checks stay scoped to the 19 November artefacts,
because their phrase patterns were calibrated against that wording. Run over
the new C3 and C5 records, `scripts/check_workflow_boundary.py` reports phrase
mismatches rather than boundary violations: the C3 record states its status as
"Status to record:" and its Decision log proposal is not keyed to a `D<n>`
identifier, and the C5 design states the permission as "is therefore both
required and permitted". The verdict table above records the required positions
in both. The checker remains conservative, reporting a boundary it cannot read
rather than passing it, and the CI scope was not widened to fit the new wording.

## Defects recorded in the output

### Campaign of 19 November 2026

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

None of these defects contradicts its scenario's oracle. The 19 November
verdict table above therefore still records what the artefact shows about the
guidance: each run took the required position on the compatibility question,
the deviation route, and the closure condition, even where its plan for getting
there is unsound. C4 is the qualification to that claim. It rejects the alias
for the unreleased addition, then records an escalation rule under which a
discovered consumer would hand the question to the released-surface
compatibility rules, which the policy does not permit. Its row therefore reads
"pass with limitation", with the initial rejection and the later exception
distinguished in the C4 row above. The artefacts are not edited to remove any
of this, because they were produced under the isolation rule and a correction
here would no longer be the run's output. The line-level findings remain on the
review threads attached to those files.

### Revalidation of 21 November 2026

A second review compared the revalidation artefacts with the same oracles and
recorded thirteen defects in seven of the twelve runs. Each cited line was read
before it was accepted, and two reviewer claims were not sustained: that S1 had
to record acceptance criteria it could not derive from the supplied statement,
and that E3 had to perform a reconciliation its input supplied no evidence for.
Both withholdals are what the no-invention rule requires, and the 19 November
S1 run recorded the same `[OPEN]` criteria. The confirmed defects fall into
four groups.

- An absence asserted rather than inspected. C4 states that no persisted data
  or wire format is involved, and classifies the persisted-data obligation as
  "not applicable to a source-symbol rename", although its input names no
  encoding and its own evidence basis marks the surface's lineage `[ASSUMED]`;
  the same lineage appears as fact in the stakeholder table at
  `terms-of-reference.md:116`. S1 states that no `docs/context.md`, technical
  design, roadmap, or ADR exists, then records at `terms-of-reference.md:22`
  that no repository artefact was inspected and, in its intake note, that the
  existence of those files is unknown. The 19 November S1 said explicitly that
  its silence was not a claim that none exists, so this is a regression. C6
  records the data owner as "represented by the sponsor" without evidence while
  `TOR-OPEN-003` still requires the data owner's approval of the field mapping.
  E1 labels `PROV-TOR-SUCCESS-001` "accepted upstream intent" while its
  companion record says the approval state was not verified.
- A check whose recorded evidence does not reach its claim. C4's `INV-LINEAGE`
  requires the old name to be absent from every formal release tag, and its
  discharge records export inspection at the latest tag alone
  (`execplan.md:364` against `:457`), which does not establish absence from
  earlier tags. E1's `git diff --numstat` command is the only counting rule
  offered for the separate code, configuration, and documentation budgets, and
  the plan does not say how a changed path is assigned to a category.
- Proposal text written in the accomplished past tense. C3's record is an edit
  pack that says the plan was not inspected, yet its progress entries and
  revision note state that the status was set to `BLOCKED` and the conflict
  recorded. S2 calls itself a "ready-to-apply amendment" with an unknown plan
  path, then ticks "Set the plan to `BLOCKED` and stopped implementation" and
  repeats the state as fact in its change-control record. E4's decision request
  states "Plan status: BLOCKED" unconditionally although its own §6 retains
  `DRAFT` for an unapproved plan, and its `D-R1` asserts that the plan does not
  record a dependency authorization the run never read. E4 also records as
  completed that it "stopped before further implementation edits", which
  presumes implementation was under way.
- A completion claim that outruns the plan's own state. C6 says the plan
  "resolves the gaps listed in `Conformance basis`" while every named gap is
  blocked pending its first milestone.

None of these defects contradicts its scenario's oracle either, and no row's
result is downgraded for them. Two reviewer limitations are not defects. C3's
record is necessarily a proposal, because the isolation rule did not admit the
executing plan; its recorded defect is the tense, not the deferral. E3
conditions removal on evidence it could not read, which is the correct response
to an input that supplies none. The 21 November C4 run also removes the 19
November limitation: a development-branch consumer creates no exception, and a
function later found in a release tag falsifies the classification and sends
the question back through the released-contract rules rather than around them.
The artefacts are again published unedited.
