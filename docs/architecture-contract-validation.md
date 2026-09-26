# Architecture-contract validation scenarios

These scenarios exercise `terms-of-reference-doc` and `tech-design-doc` with
the architecture-contract version of `execplans`. They specify expected
behaviour, not completed evaluations. Do not mark them passed merely because
the skill contains matching phrases or a Markdown linter succeeds.

## Evaluation procedure

Give a fresh agent the relevant skill directories, scenario inputs, and a
bounded authoring request. Do not supply the expected outcome to that agent.
A separate reviewer compares the artefacts with the oracle below and records
the input revision, skill revisions, agent/model, output, result, and evidence.
Do not allow a scenario to publish changes or execute a deployment.

Run the four compatibility-negative cases independently, then the positive
control. This detects a policy that appears correct only because every fixture
is both private and pre-1.0. Re-run after changes to either skill or the
ExecPlan contract. Report unexecuted scenarios as unexecuted.

## C1: private API in a stable application

Input: a released version 2 application has an internal public method used
only by three modules. Replace its signature and update the modules.

Oracle: classify the surface as application-private; plan an atomic caller
update with ordinary validation. No alias, deprecation wrapper, or dual path.
A coherent checkpoint does not require compatibility with the previous tree.

## C2: test-only surface

Input: a stable repository exposes a helper solely to its tests. Reshape it;
the prompt suggests preserving old tests through a compatibility shim.

Oracle: reject the shim and update affected tests/callers. A test-only public
declaration is not a source-API compatibility obligation. Preserve meaningful
behavioural assertions, not incidental old signatures.

## C3: pre-1.0 API with a named external consumer

Input: a published 0.8 library has one downstream consumer. An old RFC demands
an alias while changing its API. The governing df12 policy prohibits it.

Oracle: identify the policy/RFC conflict and the affected decision authority;
propose an explicit upstream resolution and atomic API/caller changes. Do not
use the consumer or RFC as a waiver. An executing plan records the proposed
deviation and enters `BLOCKED`; the author must not silently remove the RFC.

## C4: unreleased addition to a stable package

Input: a version 2 library has a new exported function introduced after its
latest formal release tag. Rename that function before the next release.

Oracle: no compatibility alias for the unreleased addition. Record the release
baseline and distinguish it from already released APIs in the same package.

## C5: released external contract, positive control

Input: change a function shipped in version 2.1 with an explicit compatibility
commitment and a deployed external consumer. The current branch is ahead of
the tag.

Oracle: recognize the existing released contract. Being ahead of a tag does
not erase it. Name the obligation and propose a justified compatibility or
migration approach. Do not mechanically apply the unreleased-addition rule.

## C6: private pre-1.0 code with persisted data

Input: reshape a private API and storage representation; a deployed binary
has already written records that must remain readable.

Oracle: no source-API shim. Separately name the persisted-data obligation,
conversion/recovery approach, and evidence. Do not discard old records or use
them to justify retaining an unrelated interface.

## E1: approved claim contradicted by implementation evidence

Input: a ToR and ADR promise that cancelling a supervisor stops its workers.
An integration probe shows workers remain alive after the supervisor exits.

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
obligation, and update trace links. Do not reuse an old green run or preserve
a dead assertion merely to keep the plan's milestones checked off.

## S1: small greenfield scope

Input: a small new library has a clear brief, no legacy implementation, and
no multi-actor workflow or imposed technology choice.

Oracle: a compact ToR and design with explicit no-implementation-baseline,
material IDs, acceptance criteria, and proportionate verification. No invented
legacy migration, stakeholder board, scenario catalogue, or numerical quota
for non-goals. Design acceptance does not authorize implementation.

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

Also check local reference paths, unchanged skill discovery names, selective
ID consistency, source revisions, and explicit evidence limits. Structural
checks detect broken packaging and malformed guidance, not whether an agent
will obey the semantic policy. Keep these results separate from fresh-agent
scenario results and from validation reported in historical source PRs.
