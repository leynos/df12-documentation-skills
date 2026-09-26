# Architecture contract and execution handoff

Read this with `../SKILL.md` before intake, outlining, and handoff. Supplement
`document-anatomy.md` rather than replacing its system-specific sections.
Use `field-evidence.md` for the source rationale. This is selective adaptation
of TOGAF ideas for df12, not a claim of formal TOGAF conformance.

## Ownership and conformance basis

The ToR owns why, for whom, scope, and imposed constraints. The design owns the
chosen architecture, contracts, alternatives, and verification obligations.
The roadmap owns outcome-oriented sequencing. The ExecPlan owns the approved
implementation slice, execution tolerances, commands, milestones, and evidence.
Keep `docs/context.md` as the normative domain vocabulary and ADRs as the
records of durable decisions. Do not duplicate these sources into competing
masters or make a historical work log the current specification.

Record a `Conformance basis` containing repository-relative paths, exact
revisions, acceptance state, relevant requirement/decision IDs, and known
conflicts or missing inputs. For uncommitted input, use an honest dated draft
identifier or content hash rather than an invented commit. Read the installed
`execplans` skill and `references/execplan-template.md` at handoff, or record
that they could not be inspected. Do not silently assume the latest contract.

Approval, evidence, and delivery state are independent. An approved design can
remain unimplemented; code on a branch can remain unverified; a merged PR can
remain unreleased or undeployed. Capture the actual state relevant to each
claim. A reviewer suggestion or subordinate agent report is input, not an
approval or a licence to complete a parent goal.

A generated schema is authoritative for its approved definitions, not for
rewriting an upstream requirement. Resolve conflicts against accepted intent.
If evidence defeats that intent's feasibility, propose a deviation with the
affected IDs and impacts; do not make the contradiction disappear in prose.

## Trace only what earns a link

Reuse established IDs. Otherwise identify material requirements, design
elements, gaps, and verification obligations. For example, a chain may run
from `TOR-GOAL-004` to `TDD-REQ-012`, `TDD-COMP-queue-store`, an ExecPlan
milestone, and observed acceptance evidence. These are illustrative names.
Do not invent the milestone or evidence before the receiving plan exists.

Each applicable upstream item needs a design response or an explicit gap.
Each substantial new component needs a requirement, constraint, risk, or
accepted decision that justifies it. Mark candidates as proposals rather than
expanding scope to make the graph look complete. A trace link means the items
relate; it is not evidence that an obligation has been discharged.

Record ID, source, requirement/design response, verification obligation,
disposition, and known consumers in a compact table or prose record. Keep
one authoritative definition. On a material change, assess upstream and
downstream impacts, preserve historical meaning, and update affected links.
Do not renumber everything after moving a section.

## Baseline, target, and actionable gaps

For brownfield work, inspect the current tree, relevant released contract, and
deployed state where material. Pin the revision and cite actual symbols,
contracts, measurements, and tests. A technology-version inventory is not an
architecture baseline. An open PR is not baseline implementation.

Describe the target separately. Classify what remains, changes, appears, or
disappears, including deliberate removals. Compare requirements against both
baseline and target; do not only compare lists of components. A target may
still contain an unsolved requirement and must say so.

A useful gap record contains ID, upstream requirement, baseline evidence,
target state, missing capability or mismatch, disposition, resolution owner,
unblock condition, and verification obligation. Valid dispositions include
already satisfied, proposed work, accepted/deferred scope, blocked, and
intentionally removed. Record acceptance for deferral rather than silently
renaming incomplete work as out of scope.

A gap is not automatically a roadmap task. Distinguish capability work,
refactoring, verification debt, and operational rollout. Prefer a coherent
existing work item where one exists. Do not turn every audit suggestion into
a new strategic goal or widen a release gate without authorization.

For greenfield work, state that no implementation baseline exists and identify
only real environmental, user-workflow, or integration constraints. Do not
manufacture an empty legacy architecture or a migration programme.

## Concern-driven views, principles, and reuse

A viewpoint defines the audience, concern, and conventions of a representation;
a view applies it to this design. For each important view, name the stakeholder,
question, representation, and relevant requirement IDs. Choose prose, a table,
a contract, or a diagram according to the question. Validate diagrams with
nixie, but do not confuse syntactic validity with an answered concern.

Discover governing principles from accepted standards, ADRs, and user intent.
Record statement, rationale, implications, and source. Distinguish a decision
guide from a hard constraint. Do not invent a principle simply because a
section is available, and do not downgrade an imposed constraint to a
preference.

For each major component, record requirements satisfied, responsibility,
contracts, failure modes, and existing assets reused. Name the asset's version
and contract when relevant. Explain a custom implementation when an existing
one appears to fit. Keep capability requirements separate from the selected
library or service so that reuse does not smuggle in a new requirement.

## Verification shapes the design

Plan implementation and verification together. Identify invariants over
inputs, states, orderings, and transitions; intermediate lemmas or contracts;
and non-trivial external axioms before settling the decomposition. Make
repository-owned logic accessible to proportionate checks. A test-only
surface must not create a source-API compatibility obligation.

For each material obligation, record:

- ID and precise property, linked requirement, and applicable component;
- assumptions and evidence for the boundary on which the argument depends;
- method, intended artefact, discharge condition, and evidence state;
- bounds, abstraction/correspondence limits, and residual uncertainty; and
- a non-vacuity argument, witness, and negative control where practical.

Choose the least costly method that establishes the required claim.
Parameterized tests suit finite partitions; generated property tests suit
input and operation-sequence spaces; bounded checking explores explicit
bounds; state-machine methods suit temporal or concurrency questions; type
invariants or formal proofs may establish stronger contracts. Explain the
coverage, not a fashionable tool choice. Combine methods when necessary.
Do not attach a prover to every component or describe sampling as proof for
all inputs. State and justify when no non-trivial invariant or lemma arises.

Ordinary unit/behavioural test implementation belongs in the ExecPlan unless
it establishes a design-level boundary or obligation. Passing a unit suite
does not discharge a missing lifecycle or deployment property. The ExecPlan
must still plan Red-Green-Refactor and concrete verification commands.

Non-vacuity is local to each obligation. Show that preconditions admit a
witness, generators reach material classes, and model states and transitions
are reachable. Include a seeded fault, mutation, or negative control rejected
for the intended reason, or explain an independent witness/counterexample
argument when that is impractical. Expected-failure markers, empty loops,
filtered-away cases, and unreachable assertions are not acceptance evidence.

A model must correspond to the repository's actual logic. Prefer exercising a
shared pure transition function when a separately transcribed model would
only verify itself. State bounded search limits and termination reasons; do
not claim exhaustive verification merely because a tool stopped successfully.

Treat third-party documented interfaces as explicit axioms rather than
undertaking to prove a dependency's internals. Verify repository-owned
configuration, lifecycle, error handling, and integration against the real
interface or a faithful contract boundary. A mock must not assert the disputed
guarantee. Mark unexecuted experiments planned, unavailable checks unverified,
and bounded or partial results with their actual scope.

For performance claims, retain workload, control, environment, selected path,
measurement protocol, uncertainty, and acceptance threshold. Verify that the
benchmark exercises the claimed behaviour. A throughput gain is not evidence
for an unmeasured causal mechanism or a different execution path. Do not
silently lower a target or increase an agreed compute budget after seeing
results; return the decision to its owner.

## Compatibility and coherent transition states

A coherent milestone may change an interface and every caller atomically.
It need not keep old and new architectures alive together. Ask whether
compatibility would be required if the change landed atomically. If not,
do not introduce it merely to obtain an intermediate plateau.

Designs MUST NOT prescribe source-API compatibility machinery for:

- private APIs, including application-internal interfaces declared public;
- test-only APIs and support surfaces;
- pre-1.0 APIs; or
- unreleased API changes ahead of the latest applicable formal release tag.

These are independent prohibitions, not preferences. Naming a consumer or
citing an older ADR does not create an exception within these categories.
If inherited requirements conflict, expose the conflict for explicit upstream
resolution; do not silently violate the requirement or implement a shim.

Classify the actual surface and release lineage. A new edit to a previously
released 1.0+ API does not erase that published contract. For released 1.0+
APIs without known external consumers, compatibility is normally unnecessary,
subject to explicit applicable policy. For a genuinely committed external
contract, name the consumer, obligation, and deliberate compatibility or
migration approach. A proposed layer must answer compatible with whom or what.

Handle persisted data and wire formats separately. Identify existing records,
deployed binaries or peers, conversion/rollback requirements, and acceptance
evidence. Their existence does not authorize unrelated source shims. Necessary
domain or external-protocol adapters are not compatibility theatre merely by
name; obsolete-interface preservation is the relevant purpose.

Reject gratuitous aliases, deprecated entrypoints, facade types, dual
implementations, compatibility adapters, and temporary wrappers. A private
refactor can have one milestone that updates the abstraction and all callers,
then another that changes implementation behind it, without an old-API path.
Do not split an atomic change merely to increase the milestone count.

The design states necessary intermediate target states, invariants, and real
migration constraints. The ExecPlan chooses the work breakdown and records
milestone IDs, assigned gaps, validated end states, acceptance evidence,
conformance checks, recovery paths, and remaining gaps. Recovery can be a
safe revert; it need not be a permanent dual implementation.

## Freshness, dependencies, and handoff

Record evidence expiry triggers: rebases, changed external contracts, upstream
merges, moved symbols, altered benchmark paths, and release/deployment changes.
Re-check affected claims before downstream work uses them. Preserve historical
findings with their original revision; distinguish them from current truth.
A green result from an earlier tree is not automatically current evidence.

Each dependency needs a provider, consumer, required capability, scope, linked
evidence, and exact unblock condition. Separate a prerequisite for one
milestone from a release blocker or a later outcome-validation dependency.
Inspect older linked work as well as recent activity; never keep an obsolete
edge solely because a summary or tracker still shows it. Correct trackers only
within the authorized task; otherwise hand off the proposed correction.

At delivery, provide the receiving ExecPlan with the conformance basis,
selected requirement/design/gap IDs, verification obligations and axioms,
compatibility assessment, acceptance boundaries, resource constraints, and
unresolved decisions. Mark readiness by scope: ready for an implementation
plan, bounded discovery only, or blocked. Design acceptance does not bypass
the ExecPlan's approval gate.

The ExecPlan remains self-contained for its bounded task: summarize the
relevant approved contract and cite its authoritative source/revision, rather
than requiring chat memory or copying the entire design. Do not create a new
approval mechanism, status vocabulary, or execution template in this skill.

If implementation invalidates the design, the executing plan records a
proposed deviation in `Decision log`, identifies impacted IDs, enters
`BLOCKED`, and awaits explicit acceptance. Reconcile the approved resolution
into the ToR, design, ADRs, roadmap links, and ExecPlan as applicable before
`COMPLETE`. Mechanical differences that change neither intent nor architecture
need only an execution-log explanation. Explicitly accepted deferred scope can
remain linked; unaccepted deviations cannot disappear into a follow-up list.
