# Problem-space contract and evidence

Read this alongside `../SKILL.md` before intake and handoff. These are df12
rules informed by selected TOGAF concepts and delivery experience, not a
requirement to adopt the whole framework. Keep problem intent here, design
choices in the technical design, sequencing in the roadmap, and execution in
the ExecPlan. The companion design reference
`../../tech-design-doc/references/field-evidence.md` records the rationale and
sources; it is background reading, not an additional execution dependency.

## Tailor the records, not the obligations

Use the existing ToR sections. Add short records where they resolve a real
question; do not impose four enterprise architecture domains, an architecture
board, a catalogue for every noun, or a new repository-wide numbering scheme.
A small library may need only a few IDs, two stakeholder concerns, and a short
handoff. Goals and non-goals need defensible boundaries, not equal counts.

A bounded discovery can proceed with explicit uncertainties. It must not claim
implementation approval. Reuse answers already present in authoritative input;
ask one unresolved, decision-relevant question at a time. Never fill a template
with invented owners, approval dates, consumers, measurements, or principles.

## Separate evidence, authority, and delivery state

For a material claim, capture its kind, statement, source and revision, last
check, and evidence status. Distinguish an observed fact, an accepted
requirement, an assumption, a proposal, and an unresolved question. Keep the
existing `[KNOWN]`, `[ASSUMED]`, and `[OPEN]` evidence labels, but record
approval separately when the claim directs work.

An explicit brief can establish what the sponsor requests. It cannot establish
that an empirical claim in that brief is true. Likewise, a merged change can
establish what implementation landed, not that a product outcome occurred.
Agent summaries, reviewer suggestions, and generated documents do not approve
themselves by repetition. Identify the actual decision authority, or leave it
unknown.

For implementation claims, distinguish at least the relevant states:
proposed, approved, implemented, verified, released, deployed, and
outcome-validated. These are separate dimensions, not a compulsory waterfall.
Use only states that matter to the work. Never infer deployment from a merged
PR, availability from an open PR, or abandonment from a quiet workstream.

When reconstructing a ToR after implementation, describe what the code does
as baseline evidence. Do not reverse-engineer supposed user approval from its
existence. Keep disputed scope and design/intent mismatches visible for the
technical design's gap analysis.

## Selective identifiers and change impact

Preserve established identifiers. Otherwise use a small, project-local scheme
for material items, such as `TOR-GOAL-004`, `TOR-CONSTRAINT-002`,
`TOR-SUCCESS-003`, `TOR-ASSUMPTION-005`, and `TOR-OPEN-006`. These names are
examples, not a compulsory vocabulary. Do not number every paragraph.

Keep each definition in one authoritative location. A compact record contains
ID, statement, provenance, evidence status, approval/owner where relevant, and
known downstream links. An assumption also records its failure consequence,
verification route, and expiry trigger. A missing consequence does not turn an
assumption into a fact; omit immaterial assumptions instead of blessing them.

On change, identify which goals, concerns, requirements, designs, roadmap
items, and ExecPlans need review. Keep IDs stable across editorial changes.
Record material revisions and supersession explicitly; never recycle an ID
for an unrelated obligation. Link only to downstream items that exist. At the
first handoff, name the receiving artefact and unresolved mapping instead of
fabricating its future milestone IDs.

## Stakeholder concerns and decision rights

Extend the stakeholder mapping with the concern, question to answer, required
evidence, and decision right. Distinguish users from operators, maintainers,
funders, reviewers, and parties affected without directly using the software.
Merge roles only when they have the same relevant concerns.

For example, an operator may ask what remains running after cancellation; a
maintainer may need an auditable explanation of dependencies; a sponsor may
need a measured resource ceiling. The ToR records those questions and required
outcomes. It does not choose a shutdown mechanism or draw the architecture.

Ask who may accept a scope change, resolve an assumption, or accept residual
risk. Advisory review, technical approval, release authority, and product
prioritization are not interchangeable. A discovery agent may recommend a
change without approving it or completing the parent goal.

## Optional scenario probe

Use a short scenario when multiple actors, lifecycle behaviour, integrations,
or exceptional paths obscure the job-to-be-done. Record trigger, actors,
preconditions, normal flow, important exceptional flows, observable outcome,
and measure. Include a failure or cancellation path when it matters.

JTBD explains the motivation; the scenario tests whether the requirement
covers the actual situation. Do not substitute a feature list, technology
choice, or implementation script. Skip the scenario when it adds no useful
information to a small or already explicit brief.

Useful unresolved-question probes include: who bears the cost when this fails;
what must remain true after interruption; which observer decides success; and
which evidence would disprove the claimed benefit. Ask them individually, not
as a questionnaire the user must complete before any progress is saved.

## Success measures, dependencies, and resource boundaries

For each material success criterion, record the baseline if known, target,
measurement conditions, evidence source, and accountable owner. Distinguish a
measurement from its causal explanation. Missing data stays open. Do not
weaken a threshold, change a control, or substitute a cheaper metric merely
because a later implementation misses the agreed result.

Capture supplied budget, runtime, memory, CI, and infrastructure constraints
without inventing values or expanding discovery into an unbounded campaign.
The design explains how to stay within them; the ExecPlan defines approved
execution tolerances. A cheaper experiment is preferable only when it can
answer the same decision-relevant question.

A dependency record names the required capability, provider and consumer,
version/release or other availability condition, linked evidence, last check,
and the precise work it gates. Classify it as blocking a design decision, an
implementation milestone, a release, or later outcome validation. A related
issue or planned feature is not automatically a blocker.

Use historical GitHub-sync and daily-work summaries to locate evidence, then
inspect the underlying PR, commit, release, or deployment record. Reconcile
stale blocker edges against their actual unblock condition, not only a recent
activity window. Keep GitHub execution evidence distinct from programme
priorities; do not create a one-to-one mirror of issues into goals. Propose
tracker corrections when outside the authorized write scope.

## Compatibility is an explicit constraint, never a milestone side effect

Terms of reference MUST NOT impose source-API compatibility machinery on:

- private APIs, including public declarations used only within an application;
- test-only APIs and support surfaces;
- pre-1.0 APIs; or
- unreleased API changes ahead of the latest applicable formal release tag.

These exclusions are independent. A named consumer does not create an
exception for a pre-1.0 or test-only API. Record an inherited conflicting
commitment as a conflict requiring explicit resolution, not a reason to
prescribe aliases, deprecated entrypoints, facades, wrappers, or shims.

Evaluate the surface and its release lineage, not just whether the branch is
ahead of a tag. An edit to an already released 1.0+ API does not make that
existing contract unreleased. Use the applicable package's formal release tag
in a multi-package repository; record uncertainty rather than guessing.
For released 1.0+ surfaces, identify real external consumers and an existing
commitment. No known consumers normally means no compatibility machinery,
subject to an explicit applicable policy.

Persisted data and wire formats are separate. An internal pre-1.0 application
may still need to read records already written or communicate with a deployed
peer. Name that state and the outcome to preserve. It does not justify an
unrelated source-API wrapper. Ordinary domain boundaries and necessary external
protocol adapters are not prohibited merely because they are called adapters;
the prohibition concerns preserving obsolete source interfaces.

## Handoff and feedback

Before handoff, identify the accepted revision, material IDs, stakeholder
concerns, success criteria, governing constraints, assumption expiry triggers,
and dependency conditions. Classify each remaining question by what it gates
and who can resolve it. State whether the scope is ready for design, ready only
for bounded discovery, or blocked. Do not represent a draft as accepted.

When implementation falsifies an assumption, record the evidence and proposed
revision here, then assess effects on the design, roadmap, and ExecPlan. Do not
replace an approved outcome with what the implementation happens to achieve.
The ExecPlan's `Decision log` records deviations; architectural deviations
enter `BLOCKED` until explicitly accepted. Before it reaches `COMPLETE`, the
approved resolution must appear in the authoritative upstream artefacts and
all affected links. An unrecorded promise to reconcile later is not completion.
