---
name: roadmap-grooming
description: >
  Groom and curate a *living* GIST (Goals, Ideas, Steps, Tasks) roadmap as it
  accretes work during execution — audit findings, code and design review
  follow-ups, dogfooding fixes, and new ideas. Use this skill whenever you are
  maintaining an existing roadmap rather than authoring one: when refactoring or
  re-architecting tasks have piled up and need consolidating into proper steps;
  when a hardening or refactoring phase has inflated into many single-task
  "steps"; when new feature ideas risk being buried among refactoring work, or
  refactoring work risks being dismissed as low value; when deciding what is
  genuine debt versus self-generating audit churn; or whenever a roadmap has
  grown and needs to be made legible again. This is the maintenance counterpart
  to the roadmap-doc skill, which authors a roadmap from design documents — read
  roadmap-doc for the GIST grammar, format, and anti-patterns this skill assumes.
---

# Roadmap grooming skill

## Relationship to roadmap-doc

The [`roadmap-doc`](../roadmap-doc/SKILL.md) skill *authors* a roadmap from
design documents, Requests for Comments (RFCs), and Architectural Decision
Records (ADRs). This skill *grooms* one that is already being executed against
and continuously fed new work. The two share the GIST model, the formatting,
and the authoring anti-patterns — all defined in `roadmap-doc` and its
[`references/conventions.md`](../roadmap-doc/references/conventions.md). Do
not re-derive those here: read them, then apply the grooming discipline below.
In short, use `roadmap-doc` to write a roadmap and `roadmap-grooming` to keep
it true and legible as it grows.

## Required companion skill

`roadmap-grooming` depends on `roadmap-doc`. Agents must have access to
[`roadmap-doc/SKILL.md`](../roadmap-doc/SKILL.md) and
[`roadmap-doc/references/conventions.md`](../roadmap-doc/references/conventions.md)
before this skill can be applied correctly. When installing a single skill,
install `roadmap-doc` alongside `roadmap-grooming`; otherwise the required GIST
grammar, roadmap format, dependency notation, and anti-patterns are missing.

## Why grooming is a distinct activity

A roadmap built from a design document is coherent on day one. Under execution
it is fed from many mouths — post-merge audits, code and design reviews,
dogfooding reports, and fresh ideas — and without active grooming it degrades
in two predictable, opposite ways:

- **New ideas get lost.** A feature or capability, appended wherever there was
  room, ends up buried among refactoring work and becomes invisible.
- **Refactoring gets dismissed.** Internal-quality work, judged by user-facing
  value it was never meant to have, reads as "low value" and is deprioritized
  or cut wholesale.

Both are the same root failure: **the roadmap does not distinguish *kinds* of
work, so they bleed together and are mis-valued.** Grooming makes the kind of
work explicit and keeps the kinds separate, each judged on its own terms.

## 1. Classify work by kind, and keep the kinds in separate phases

Every phase has exactly one **kind**:

- **Capability** — new user-facing value (a feature, a command, a behaviour).
  This is forward "idea" work.
- **Refactor / consolidation** — remove duplication, single-source a seam,
  improve internal structure without changing behaviour.
- **Re-architecting** — change a boundary or structure, usually ADR-worthy.
- **Hardening** — robustness against edge cases: guards, property tests,
  recovery paths.
- **Reconciliation** — make documentation, naming, and conventions true and
  consistent.

State the kind in the phase's `Idea:` line. **Never interleave capability
phases with refactor or hardening phases.** Capability work lives in its own
track — a dedicated "Features and extensions" phase or number range — so a new
idea is never appended into the middle of a refactoring phase where it
vanishes. When a new idea arrives, it goes to the capability track, not after
the last refactoring step because that is where the cursor happens to be.

## 2. Value each kind on its own axis

A phase's value statement must match its kind, so no kind is judged by an axis
it was never meant to serve:

- **Capability** is valued by user-facing outcome.
- **Refactor / re-architect** is valued by *codebase health and future
  velocity*: duplication removed, one true name, defect surface reduced, the
  cost of the next change lowered. Frame the `Idea:` as the investment — what
  future cost it avoids and what it enables — so a reviewer sees the return
  rather than dismissing it.
- **Hardening** is valued by *failure modes closed*.
- **Reconciliation** is valued by *truth*: a reader can trust the docs.

Making the axis explicit is what stops refactoring being waved away as low
value, and stops a clean-codebase investment being silently deprioritized.

## 3. Construct proper steps from refactoring and re-architecting tasks

Refactoring work usually *arrives as scattered fragments* — one audit finding
per duplication, one review note per seam. Left alone they become a sprawl of
single-task "steps". The grooming move is to assemble them into a few coherent
steps. The method:

1. **Gather** the fragments for a theme.
2. **De-duplicate.** Merge true duplicates; subsume a narrow item under a
   broader one that already covers it; drop anything already done.
3. **Separate re-architecting from refactoring.** Re-architecting changes a
   boundary (ADR-worthy, larger); it *sets the target* the refactors align to,
   so it anchors the step (or earns its own) and is never buried among small
   don't-repeat-yourself (DRY) tasks where a load-bearing structural decision
   goes unreviewed. Refactoring *realizes* that structure and becomes the
   follow-through.
4. **Align by seam, not by wording.** Cluster tasks by the actual boundary,
   invariant, or module they touch — not their surface phrasing. Two cohesion
   gates: if you cannot state **one hypothesis** the whole cluster serves, it
   is two or more steps (split); if a task does not serve the seam, it is
   misfiled (reroute — do not force-fit it).
5. **Synthesize the step.** Name the seam, then write the hypothesis: *"is
   `<seam>` now expressed once, correctly, documented, and pinned so it cannot
   re-fork?"* The cluster becomes the step's tasks. Set the consolidation
   standard as the definition of done for every task.
6. **Sequence.** Foundational consolidation and re-architecting first; then the
   dependents — *and the hardening, and the docs* — via `Requires`, so they
   attach to the single-sourced result rather than a copy that re-diverges.

This is harder than splitting fake steps, and its failure mode is the opposite:
**over-consolidation** into an amorphous grab-bag. The one-hypothesis, one-seam
gate is what keeps a constructed step cohesive. See
`references/step-construction.md` for a worked example.

### Consolidation standard

Every consolidation task has the same definition of done: **one canonical
implementation, under one name, documented as the source of truth, pinned by a
test.** Reference this standard instead of redefining it for each fragment.

## 4. Bust buckets, and fix the generator

- A **single-task "step"** is a smell: it is a task wearing a step's hat. Fold
  it into the thematic step whose hypothesis it serves.
- When **two or more same-theme items** accrue (several "single-home X"), apply
  the construction method above before they multiply.
- **Findings fold into existing steps, never a new step per finding.** A process
  that files each audit or review finding as its own step is the engine of
  bucket inflation. Route findings into the relevant existing step, or a single
  debt task, filtered by severity. If you control that process — a triage step,
  a reviewer prompt — fix it there; prevention beats periodic cleanup.

## 5. Distinguish genuine debt from manufactured churn

Valuing refactoring (section 2) does not mean accepting all of it. Two things
look alike and must be told apart:

- **Genuine debt** — real duplication, a real missing guard, a real
  inconsistency. It is bounded: consolidate the seam once and it is done. Worth
  a step.
- **Manufactured churn** — the output of a process auditing its own output (an
  audit of an audit-generated task finds another micro-issue, endlessly). It is
  self-generating, never converges, and produces tidiness with no real return.

Track the former; drop the latter. A tell for churn: the work grows as fast as
it is cleared, and each item is a single trivial tweak with no seam behind it.

## 6. Grooming cadence and triggers

Groom at these triggers, not on a timer:

- A phase exceeds a handful of steps, or single-task steps start to accrue.
- A capability task has landed inside a refactoring phase.
- A run of uniformly small steps appears (sized to fit headings, not seams).
- Two or more same-theme refactoring fragments sit unconsolidated.
- An audit or review batch has just landed and needs routing.

A grooming pass: re-classify phases by kind; lift any buried capability work
into the capability track; construct steps from the accumulated fragments
(section 3); fold single-task steps; and confirm each phase's value statement
matches its kind.

## Key constraints

- This skill assumes the GIST grammar, formatting, and authoring anti-patterns
  defined in the [`roadmap-doc`](../roadmap-doc/SKILL.md) skill and its
  [`references/conventions.md`](../roadmap-doc/references/conventions.md).
  Follow them; do not restate or contradict them.
- British English, Oxford spelling (-ize, -our, -yse); sentence-case headings;
  80-column prose wrapping.
- Preserve dotted numbering and dependency citations when restructuring: when a
  phase, step, or task moves, every `Requires` reference to it must move with
  it. A renumber that leaves a dangling or mis-pointed reference is a defect —
  do it with a tool, or verify every reference resolves afterwards.
- Grooming only re-shapes and re-values existing intent; it does not invent or
  delete scope. Dropping manufactured churn (section 5) is the one sanctioned
  removal, and it is recorded, not silent.

## When to read references

Read `references/step-construction.md` when constructing steps from a pile of
refactoring or re-architecting tasks; it walks one worked example end to end.
