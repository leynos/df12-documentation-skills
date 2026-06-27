# Constructing steps from refactoring tasks: a worked example

This walks the construction method from `SKILL.md` section 3 end to end, on a
real shape of degraded roadmap. Names are generalised; the pathology is not.

## The situation

A project's final "deferred extensions" phase had been fed by post-merge audits
for weeks. Each audit filed its finding as a *new step*, so the phase had grown
to about 37 steps and roughly 100 open tasks. Reading the phase's headings
showed the pathology at a glance:

- ~14 steps beginning "Single-home X" or "Consolidate Y" — each a one- or
  two-task DRY refactor of a specific seam.
- ~11 steps beginning "Harden Z against W" — each a one-task defensive fix.
- 3 genuine feature steps (a configurable pack set, a new pass, a new detector),
  buried in the middle.

Twenty-one of the 37 steps held a single task: tasks wearing step hats. The two
dominant themes were the same idea fragmented, and the features were invisible.

## The construction

### 1. Gather and classify by kind

Tag each step by kind: ~14 refactor, ~11 harden, 3 capability, the rest
reconciliation or convention. The separation problem is immediately visible —
capability work is scattered among refactoring.

### 2. Lift capability into its own track

Move the 3 feature steps into a new "Features and extensions" phase. They are
no longer buried, and they are now valued by user outcome on their own axis.

### 3. De-duplicate and align the refactor fragments by seam

The 14 "single-home" fragments are not 14 ideas; they cluster by the seam each
touches:

- **Machine-payload projections / envelopes** — the compile-currency,
  reconciliation-payload, and finding-outcome envelope projections.
- **Loaders, builders, scan primitives** — the pack/ledger loader and the
  inline-table builder.
- **Command facade, predicates, writers** — the facade seams, the
  done-predicate, and the multi-file writer.
- **Word-count, draft-sourcing, disk-evidence** — the draft reader, the
  word-count seams, and the disk-evidence predicates.
- **Corpus and end-to-end test scaffolding** — the fixture plugin and the
  command-driving harness.

*Five seams, not fourteen steps.*

### 4. Synthesise one step per seam

For each seam, write a step whose hypothesis is "is this seam expressed once,
documented, and pinned?", and whose tasks are the cluster, each carrying the
consolidation standard (one canonical implementation, documented, tested). The
14 fragments become 5 coherent single-source steps.

### 5. Consolidate the hardening and sequence it after

The 11 "harden" fragments collapse into one or two hardening steps, sequenced
*after* the single-source steps with `Requires`, so each guard is applied to
the single-sourced code rather than to a copy it would then have to re-harden.

### 6. The result

37 bucket-steps become about 7 honest steps — 5 single-source, 1 hardening, 1
reconciliation — plus a real features phase. The roadmap now reads as intent
rather than as an audit log.

## The cohesion gates in action

- A "settle the number-formatting convention" finding *looked* like it belonged
  with the projection seam, but its hypothesis is "is the numeric format
  settled once" — a *convention*, not a projection. It went to the
  reconciliation step. (A task that does not serve the seam is misfiled:
  reroute, do not force-fit.)
- The "corpus scaffolding" and "command-driving harness" fragments were first
  drafted as one step, but no single hypothesis covered both the fixture-plugin
  seam and the harness seam, so it split into two. (If one hypothesis does not
  cover the cluster, it is two steps.)

## Fixing the generator

The restructure is wasted if the audit process keeps filing one step per
finding. Change the triage so findings fold into the relevant existing
single-source or hardening step — or a single debt task — filtered by severity.
Otherwise the 37 buckets simply grow back. Prevention at the generator beats
periodic re-grooming.
