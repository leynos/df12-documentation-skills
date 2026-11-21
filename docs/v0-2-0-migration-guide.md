# Migration guide: v0.1.0 to v0.2.0

_Moving `terms-of-reference-doc` and `tech-design-doc` practice onto the
contract-aligned guidance._

______________________________________________________________________

## Who should read this

Read this if you use `terms-of-reference-doc` or `tech-design-doc`, or review
the documents they produce. Both skills now read a named contract reference
before intake, record traceable identifiers, classify each API surface before
proposing compatibility work, and reconcile implementation deviations through
the ExecPlan `BLOCKED`/`COMPLETE` states.

## Impact at a glance

| Priority    | Area             | What to do                                                                                     |
| ----------- | ---------------- | ---------------------------------------------------------------------------------------------- |
| Required    | Contract reading | Read the skill's contract reference before intake and again at handoff.                        |
| Required    | Traceability     | Record the contract records and stable IDs the handoff names.                                  |
| Required    | Compatibility    | Classify each API surface; never propose compatibility machinery for a prohibited category.    |
| Required    | Deviations       | Record an implementation deviation in `Decision log` and enter `BLOCKED` until it is accepted. |
| Recommended | Evidence         | Record each claim's source, limit, and expiry trigger.                                         |

_Table 1: Obligations when moving from v0.1.0 to v0.2.0._

## 1. Read the contract reference before intake

`terms-of-reference-doc` requires `references/problem-contract.md` before
intake and again at handoff. `tech-design-doc` requires
`references/architecture-contract.md` before intake, outlining, and handoff.

### Before

```text
Start from the sponsor's brief, then draft the objectives.
```

### After

```text
Read `references/problem-contract.md`, then draft the objectives from the
brief, marking each claim `[KNOWN]`, `[ASSUMED]`, or `[OPEN]`.
```

A brief or request establishes what the sponsor asks for, not the truth of an
empirical claim inside it; that claim needs its own evidence.

## 2. Record the traceable contract records

Both skills now produce records that downstream design and ExecPlans inherit.
Keep IDs stable across editorial changes; a renamed ID breaks the trace.

- **Terms of reference.** Record the accepted revision, material IDs,
  stakeholder concerns, success criteria, governing constraints, assumption
  expiry triggers, and dependency conditions.
- **Technical design.** Record the conformance basis, selected
  requirement/design/gap IDs, verification obligations, compatibility
  assessment, acceptance boundaries, and unresolved decisions.

A gap record carries its ID, upstream requirement, baseline evidence, target
state, disposition, resolution owner, unblock condition, and verification
obligation. Approval, evidence, and delivery state stay separate: an approved
design can remain unimplemented, and a merged change can remain unreleased.

## 3. Classify the API surface before proposing compatibility work

Designs and terms of reference MUST NOT prescribe or impose source-API
compatibility machinery for private APIs (including application-internal public
surfaces), test-only APIs, pre-1.0 APIs, or unreleased API changes ahead of the
latest formal release tag. A named consumer or an older RFC does not waive a
prohibition; escalate the conflict to its owner and update callers atomically.

Released 1.0+ contracts and deployed-data or wire-format obligations are a
separate assessment. Read the latest formal release tag, then assess those
surfaces on their own evidence.

### Before

```text
Keep the pre-1.0 signature working by adding an alias for the one consumer
that still calls it.
```

### After

```text
The pre-1.0 alias is prohibited. Raise the policy conflict with its owner and
update the consumer atomically in the same change.
```

## 4. Reconcile deviations through `BLOCKED` and `COMPLETE`

An executing ExecPlan records a proposed deviation in `Decision log`, enters
`BLOCKED`, and waits for explicit acceptance. Before it reaches `COMPLETE`, the
approved resolution must appear in the upstream terms of reference, design, or
ADR, and all affected links must agree. Correct transcription drift directly;
do not rewrite requirements to legitimise a generated artefact or current code.

## What does not need to change

- Existing documents that already carry stable IDs, sourced claims, and a
  stated compatibility assessment need no rewrite.
- The ExecPlan skill is unchanged. This release changes the guidance the two
  documentation skills hand to it, not the handoff mechanics.
- Nothing in this release changes repository gates, release tooling, or
  deployed hosts.

## Migration checklist

- [ ] Read the contract reference named by each skill before intake.
- [ ] Label every prior-art claim `[KNOWN]`, `[ASSUMED]`, or `[OPEN]`.
- [ ] Record the handoff IDs, concerns, criteria, and dependency conditions.
- [ ] Classify each API surface as prohibited or separately assessed.
- [ ] Record any implementation deviation and enter `BLOCKED`.
- [ ] Reconcile the approved resolution upstream before claiming `COMPLETE`.

## Common errors and fixes

- **Error:** `Designs MUST NOT prescribe source-API compatibility machinery
  for:`
  - **Fix:** Remove the shim, alias, facade, wrapper, or compatibility
    entrypoint, and update the affected callers in the same change.
- **Error:** `Terms of reference MUST NOT impose source-API compatibility
  machinery on:`
  - **Fix:** State the required outcome instead of a compatibility mechanism,
    and let the design record the compatibility assessment.
- **Error:** an approved design, a merged pull request, or a passing test is
  reported as implementation, release, or deployment evidence.
  - **Fix:** Record the state that actually holds. Approval, evidence, and
    delivery are independent.
- **Error:** a deviation is recorded but the plan proceeds to `COMPLETE`.
  - **Fix:** Enter `BLOCKED`, obtain explicit acceptance, reconcile the
    upstream artefacts, then continue.
