---
name: terms-of-reference-doc
description: >
  Generate terms of reference documents that capture the problem space —
  domain, market, users, job-to-be-done, scope, constraints, and open
  questions — before any solution work begins. Use this skill whenever
  the user asks to write, draft, or produce a terms of reference,
  project charter, product brief, problem statement, vision and scope
  document, domain knowledge document, or "what is this for" document.
  Also trigger when the user starts a new project without an established
  brief, wants to capture domain knowledge from a subject-matter expert,
  needs to draw explicit scope boundaries before technical design, or
  asks to elicit and document the rationale for a system. The skill
  drives an elicitation-led workflow: prior-art discovery, gap analysis,
  structured interview, drafting, editing, and handoff to the design
  and roadmap skills. It produces documents in the style of df12
  Productions — precise, evidence-grounded, and free of aspirational
  fluff.
---

# Terms of reference document generation

A skill for producing rigorous terms of reference documents that
capture the problem space before any solution work begins.

The terms of reference is the upstream artefact in the df12
documentation suite. The tech design document expands on the *how*; the
roadmap sequences the *when*; the terms of reference settles the *why*,
*for whom*, and *bounded by what*. Without it, design choices float
free of the problem they are meant to solve, and roadmaps prioritise
work whose value cannot be defended.

## Before starting

Read the following reference files as needed during the workflow:

| Reference | When to read | Path |
|---|---|---|
| **Elicitation protocol** | Before Phase 2 — interview discipline, question patterns, exit conditions | `references/elicitation-protocol.md` |
| **Editing checklist** | Before Phase 4 — the fluff-elimination protocol (shared with `tech-design-doc`) | `../tech-design-doc/references/editing-checklist.md` |
| **Document anatomy** | Optional, for cross-reference — section catalogue used by `tech-design-doc` | `../tech-design-doc/references/document-anatomy.md` |

## Governing principles

1. **Problem space, not solution space.** A terms of reference describes
   what is true about the world the product enters: who the users are,
   what they are trying to accomplish, what constrains the work. It
   does not name technologies, draw architectures, or sequence
   implementation. Solution-space material that surfaces during
   elicitation is captured as a candidate for the tech design document,
   not absorbed into the terms of reference.

2. **Elicit, don't infer.** The domain knowledge lives in the user's
   head and in their existing artefacts. The skill's job is to extract
   it, challenge it, and persist it — not to manufacture it from
   plausible-sounding generalities. When the user does not know an
   answer, the skill records that as an open question rather than
   inventing one.

3. **Goals and non-goals carry equal weight.** A terms of reference
   without explicit non-goals is a wish list. Scope insurance comes
   from naming what the product will deliberately *not* do.

4. **Distinguish known, assumed, and open.** Every claim in the
   document inherits one of three statuses: established from evidence,
   assumed pending verification, or unresolved. Conflating these
   produces false confidence.

5. **Save progress; allow exit.** Elicitation is iterative. The skill
   writes the document as it goes, not only at the end. The user can
   declare "good enough" and ship a v0.1 terms of reference with open
   questions marked — that is the correct outcome when further
   elicitation has diminishing returns.

6. **The document is living.** A terms of reference is updated when
   reality changes: a new user segment appears, a constraint lifts, a
   non-goal becomes a goal. The skill produces v1; subsequent revisions
   are expected and welcome.

## Workflow

Execute these phases in order. Each phase produces concrete output
before the next begins. Do not collapse phases — particularly, do not
draft prose before the provisional sketch is agreed.

### Phase 0 — Intake and prior art discovery

The first instinct is to grill. Resist it. Find what already exists
first; the user has often answered half the questions already, and
re-asking signals that the skill has not read its inputs.

Check these locations and read what is present:

- Files attached to the prompt.
- `README.md` and any `docs/README.md` in the repository root.
- `docs/terms-of-reference.md` (prior versions; the skill may be
  updating rather than creating).
- `docs/context.md` (ubiquitous language; defines terms the user
  already considers settled).
- `docs/adr/` or `docs/decisions/` (architectural decisions reveal
  constraints and prior reasoning).
- `docs/design.md`, `docs/architecture.md`, or any tech design
  documents.
- `docs/roadmap.md`.
- Any pitch decks, briefs, or proposals the user references.

**A note on order.** If a tech design document or roadmap exists but
no terms of reference, the skill is being asked to write upstream
documentation downstream. This is a smell worth surfacing: the design
may be solving a problem that has not been articulated, or the team may
have implicit assumptions worth making explicit. Acknowledge the
ordering, then proceed — reconstructing the terms of reference from
existing solution-space artefacts is a legitimate exercise.

Produce a working note that catalogues:

- What artefacts exist.
- Which sections of the terms of reference each artefact informs.
- Where artefacts conflict (these become elicitation targets).
- What is conspicuously absent (also elicitation targets).

### Phase 1 — Provisional sketch and gap analysis

Build a section-level sketch of the terms of reference from the prior
art alone. For every section, mark each claim with one of three tags:

- `[KNOWN]` — established from an explicit source in the prior art.
- `[ASSUMED]` — the prior art implies it but does not state it; or it
  is a reasonable inference that needs confirmation.
- `[OPEN]` — no answer in the prior art.

Example:

```markdown
## 4. Users and stakeholders

### Primary user
[KNOWN] Solo developers and small teams shipping CLI tools.
Source: README.md, intro paragraph.

[ASSUMED] Predominantly Rust and Python developers.
Source: inferred from example projects in /examples.

[OPEN] Whether enterprise developers in regulated environments are in
or out of scope.
```

Present the sketch to the user before proceeding. Confirm `[KNOWN]`,
challenge `[ASSUMED]`, agree the priority order for resolving `[OPEN]`.

This phase exists specifically to prevent the failure mode the Grill
With Docs skill was built to address: the agent re-asking questions
whose answers already sit in `docs/context.md` or the README. The user
should never have to repeat themselves.

### Phase 2 — Elicitation

→ Read `references/elicitation-protocol.md` for question patterns,
single-question discipline, dependency ordering, and exit conditions.

The elicitation phase resolves `[ASSUMED]` and `[OPEN]` items in
dependency order. The most important rules:

1. **One question at a time.** Asking three questions at once produces
   one answered question and two forgotten ones, or a torrent of prose
   that conflates the answers.
2. **Walk dependencies, not sections.** "What is the primary user?"
   gates "what job are they doing?" gates "what is success?" — answer
   in that order, even if it crosses section boundaries.
3. **Challenge fuzzy language.** When the user says "developers", ask
   which kind. When they say "enterprises", ask which size, sector,
   maturity. Fuzziness in the terms of reference becomes ambiguity in
   the design.
4. **Surface tensions.** If the user's current answer contradicts an
   earlier one, name the contradiction and ask which is authoritative.
   Do not silently resolve it.
5. **Persist as you go.** Write to `docs/terms-of-reference.md` after
   each substantive resolution, not at the end. The user can read the
   evolving document and catch drift.
6. **Accept exits gracefully.** When the user says "good enough, let's
   ship this with open questions noted", do it. Mark the remaining
   items in the Open Questions section and proceed to drafting.

### Phase 3 — Drafting

By Phase 3, the document is mostly written. Drafting consolidates,
fills gaps, and writes the connective tissue between resolved items.

The output document follows the structure in the next section. While
drafting:

- **Cross-reference `docs/context.md`** for every domain term. If the
  terms of reference introduces a term not in `context.md`, propose it
  as an addition.
- **Flag ADR candidates.** Decisions surfaced during elicitation that
  are hard to reverse — choice of regulatory framework, primary user
  segment, business model — warrant ADRs. Note them in the handoff
  section.
- **Distinguish goals from outcomes.** A goal is what the product
  attempts; an outcome is what the user experiences. Both belong, but
  in different sections. "Reduce time-to-first-value to under five
  minutes" is an outcome, not a goal. The corresponding goal might be
  "make the default configuration usable without editing files."
- **Phrase non-goals as positives.** "We are not building X" is fine,
  but "X is out of scope; users seeking X should use Y" is more useful
  and prevents the non-goal from being relitigated.

### Phase 4 — Editing pass

→ Read `../tech-design-doc/references/editing-checklist.md` for the
complete protocol.

The editing pass is mandatory. Apply all seven passes from the
checklist (structural coherence, fluff elimination, vocabulary
precision, consistency, source verification, locale enforcement, final
read).

Terms-of-reference-specific targets for the editing pass:

- **Aspirational language.** "We aim to delight users" is not a goal;
  it is mood music. Cut or replace with a verifiable outcome.
- **Persona zoo.** A document with seven personas usually has two real
  ones and five composites. Consolidate.
- **Stealth solutions.** Phrases like "the system will use" or "the
  database stores" smuggle solution-space decisions into the problem
  statement. Move them to the design document or cut.
- **Job-to-be-done as feature list.** "The user wants to filter the
  dashboard" is a feature, not a job. The job is the situation the
  user is in and the outcome they need. Rewrite.
- **Vague success criteria.** "Users will be satisfied" is not
  measurable. Either name the signal that indicates success, or
  acknowledge that the criterion is currently unmeasurable and record
  it as an open question.

### Phase 5 — Handoff and companion artefacts

A finished terms of reference is the start of a chain, not the end.
Before delivering, identify what comes next:

1. **Context.md additions.** Every domain term used in the terms of
   reference that is not already in `docs/context.md` should be a
   candidate addition. Produce a patch or a list of proposed entries.
2. **ADR candidates.** Hard-to-reverse decisions surfaced during
   elicitation become ADRs. Name them; do not write them in this skill.
3. **Open questions register.** The Open Questions section lists what
   remains unresolved, with criteria for resolution and an owner where
   possible. This is the primary input to the next iteration.
4. **Downstream readiness.** Note whether the terms of reference is
   complete enough to begin a tech design (`tech-design-doc`) or
   roadmap (`roadmap-doc`). It usually is, with open questions
   acknowledged; it occasionally is not, and the user should know
   that before downstream work begins.

Deliver the document to `docs/terms-of-reference.md` unless the user
specifies otherwise.

## Document structure

The output `docs/terms-of-reference.md` follows this structure. Section
ordering reflects dependency: later sections may refer to earlier ones,
not the reverse.

### Front matter

- **Title.** Project or product name followed by "— terms of reference".
- **Status.** Draft, v0.1, accepted, superseded.
- **Audience.** Who is expected to read this. For a terms of reference,
  the audience usually includes product owners, engineering leads,
  design, and any external sponsor.
- **Companion documents.** Pointers to `context.md`, `docs/design.md`,
  `docs/roadmap.md`, relevant ADRs.
- **Date and version.** Last substantive revision.

### 1. Background and motivation

Why does this work exist now? What changed in the world — technological,
regulatory, commercial, organisational — that makes this worth doing?
This is not the origin story of the product; it is the answer to "why
not five years ago, and why not five years from now?"

If the answer is "the founder thought it would be a good idea",
acknowledge that honestly. A weak motivation is information.

### 2. Domain

The territory the product operates in. Cover:

- The field of practice (e.g. observability, compliance reporting,
  audio production).
- Established conventions, norms, and assumptions in that field.
- Prior art the product builds on, displaces, or coexists with.
- Regulatory or contractual bedrock that shapes what is even possible.

Cross-reference `docs/context.md` for terminology. If `context.md` does
not yet exist, this section is where the first cut of domain
vocabulary appears — but flag it for promotion to `context.md`.

### 3. Market context

Where the product sits relative to others. Cover:

- Direct competitors, with named examples.
- Adjacent products users may already use for related jobs.
- The current default — including "do nothing" — that the product
  competes against.
- The gap the product addresses, framed as a specific deficiency in
  the existing landscape rather than a generic "there's nothing like
  this."

A market context section that names no competitors is suspect.
Something always occupies the space, even if it is a spreadsheet or
manual process.

### 4. Users and stakeholders

Identify the people involved. For each user type:

- A descriptive name (not a marketing persona name).
- Their context: role, working environment, technical fluency.
- What they care about.
- What they will ignore or actively dislike.
- Their current alternative for the job-to-be-done.

Distinguish:

- **Primary users.** The product is built for them.
- **Secondary users.** They interact with the product but it is not
  built for them (e.g. reviewers of artefacts the primary user
  produces).
- **Stakeholders.** They influence or fund the work without using the
  product directly.
- **Non-users.** People the product is explicitly not for. Naming them
  prevents scope drift.

A stakeholder mapping table is often clearer than prose for this
section. Use one.

### 5. Job to be done

For each primary user, state the job in the canonical form:

> When *[situation]*, *[user type]* wants to *[motivation]*, so they
> can *[outcome]*.

Avoid feature-shaped jobs ("the user wants to export CSV"). A genuine
job-to-be-done is the situation and the outcome; the feature is the
solution. Multiple features can serve one job; one feature can serve
multiple jobs.

Where relevant, name:

- The functional dimension (what is accomplished).
- The emotional dimension (how the user wants to feel).
- The social dimension (how the user wants to be seen).
- The competing alternatives currently used, including
  workarounds and "do nothing".

### 6. Scope

Two subsections, of roughly equal length:

#### 6.1 Goals

Verifiable outcomes the product attempts to deliver. Each goal should
be falsifiable: a reasonable observer could check whether the product
has achieved it.

#### 6.2 Non-goals

Explicit exclusions. Each non-goal should be plausible enough that a
reasonable reader might have expected it to be in scope; recording
non-goals that nobody would have expected is busywork.

Where useful, pair non-goals with a redirect: "X is out of scope; users
needing X should use Y."

### 7. Success criteria

How will the team know the product is working? Distinguish:

- **User-facing success.** Signals from users — adoption, retention,
  task completion, satisfaction — that indicate the job is being done.
- **Operational success.** Signals from the system — uptime, latency,
  cost — that indicate the product is sustainable.
- **Strategic success.** Signals from the sponsor or business — revenue,
  market position, capability built — that indicate the work was worth
  doing.

Specific signals beat aspirational metrics. "Median time from `git
clone` to first successful run is under five minutes" is a signal.
"Users find it easy to get started" is not.

### 8. Constraints and assumptions

#### 8.1 Hard constraints

What cannot change regardless of design choices: regulatory
requirements, contractual obligations, technical platform requirements,
budget ceilings, deadline floors.

#### 8.2 Assumptions

What the work proceeds on faith of. Each assumption should have a
named consequence if it fails. "We assume users have a working Python
installation" is paired with "if they do not, onboarding fails at step
one and a fallback is required."

#### 8.3 Dependencies

External work the project relies on: other teams' deliverables,
third-party services, upstream library releases. Name them; note where
they sit on the critical path.

### 9. Open questions

Decisions that remain unresolved. For each:

- The question, stated precisely.
- Why it matters (what downstream work it gates).
- Criteria for resolution (what evidence or decision closes it).
- Owner, if known.
- Suggested resolution path: further elicitation, an ADR, an
  implementation spike, market research, etc.

A terms of reference with no open questions is either remarkably
mature or insufficiently interrogated. Most v0.1 documents will have
several.

### Appendices

- **Stakeholder mapping table** (if not placed in §4).
- **References.** Sources cited in the document with URLs and access
  dates.
- **Glossary pointer.** A note directing readers to `docs/context.md`
  for terminology, and an inline mini-glossary if `context.md` does
  not exist yet.

## Failure modes

- **The user cannot articulate the problem.** The elicitation surfaces
  that the project is being undertaken on instinct rather than on a
  defensible problem statement. Do not paper over this. Record what
  the user *can* say, mark the rest as open, and recommend an
  exploratory phase (user interviews, market research, a discovery
  spike) before proceeding to design.

- **Existing artefacts contradict each other.** README says one thing,
  the founder's pitch deck says another. Surface the conflict, ask
  which is authoritative, and record the resolution. If the conflict
  cannot be resolved in the session, mark it as an open question and
  identify who can resolve it.

- **The user wants to skip to design.** A frequent request. Push back
  briefly: a terms of reference completed in a single session pays for
  itself many times over in design conversations that no longer have
  to relitigate basic premises. If the user still wants to skip, do
  so — but record what is being skipped as an open question, so the
  design phase knows what it is operating without.

- **Solution-space material dominates the conversation.** The user
  keeps wanting to talk about architecture, technology choices, or
  features. Acknowledge each item, capture it as a candidate for the
  tech design document, and return to problem-space questions.

- **No prior art exists.** A genuinely greenfield project with no
  existing artefacts is rare. When it does happen, the entire document
  is built from elicitation; the workflow is the same, but Phase 0
  produces an empty catalogue. Phase 1's provisional sketch then
  consists entirely of `[OPEN]` items.

- **The project is downstream of a decision already made.** Sometimes
  the terms of reference is being written to justify a project that
  has already been chartered. The skill cannot un-charter the project,
  but it can ensure the document accurately reflects the constraints
  imposed by the prior decision — and surfaces the cost of those
  constraints as open questions or non-goals.

## Anti-patterns to avoid

- **The mission statement.** Aspirational copy without verifiable
  content. "We will revolutionise observability for cloud-native
  workloads" tells the reader nothing they can act on. Replace with
  the specific deficiency in current observability that the product
  addresses.

- **The persona zoo.** Five or more personas, each with a name,
  photo-like description, and quote, but no operational distinctions
  between them. Consolidate to the real distinctions.

- **The everything-in scope.** A goals section that lists twenty items
  and a non-goals section with one item. The scope is undefended.
  Force the user to cut goals or expand non-goals until the lists are
  roughly comparable in length and the boundaries are defensible.

- **The aspirational user.** Describing the user the product hopes to
  attract, rather than the user it currently or initially serves.
  Phase 1 of any product is built for the user who shows up first.

- **JTBD as feature list.** "The user wants to filter the dashboard"
  is the solution. "When a sales rep is preparing for a customer call,
  they want to assess account health quickly, so they can lead with
  context" is the job. Rewrite features as jobs.

- **The buried assumption.** Constraints stated as facts. "Users have
  reliable internet" is an assumption, not a fact; treat it as one
  and pair it with a failure consequence.

- **The cosmetic non-goal.** "We will not build an artificial general
  intelligence" — no reader expected you to. Non-goals should record
  exclusions that a reasonable reader might have assumed were in
  scope.

- **Solution-shaped goals.** "Goal: build a CLI with subcommands for
  X, Y, Z" is a feature list disguised as a goal. The goal is what
  the CLI enables the user to do, not what shape the CLI takes.

## Tool integration notes

### Relationship to `tech-design-doc`

The terms of reference is the upstream input. A finished terms of
reference unblocks tech design by settling the problem statement,
user definition, scope boundaries, and constraints. The `tech-design-doc`
skill's Phase 0 (Intake and scoping) should explicitly read
`docs/terms-of-reference.md` if present.

If solution-space decisions surface during elicitation, capture them
as candidates for the design document — do not absorb them into the
terms of reference.

### Relationship to `roadmap-doc`

The roadmap derives its phase ideas — the falsifiable hypotheses each
phase tests — from the terms of reference. A roadmap whose phases
cannot be traced back to goals, non-goals, and success criteria in the
terms of reference is sequencing work without a defensible rationale.

### Relationship to `docs/context.md`

The terms of reference introduces domain vocabulary that should
ultimately live in `context.md` (the ubiquitous language document).
Where `context.md` exists, cross-reference it. Where it does not, the
terms of reference is often the artefact that motivates its creation;
flag this in the handoff.

### Relationship to ADRs

Hard-to-reverse decisions surfaced during elicitation are ADR
candidates. The skill identifies them; the user (or a separate ADR
skill) writes them. Do not embed ADR-shaped content in the terms of
reference itself — pointer-and-summary is enough.

### df12 copy skill

If producing a terms of reference for a df12 Productions product, load
the `df12-copy` skill for voice and style enforcement. The editing
pass should then apply both the editing checklist from
`tech-design-doc` and the self-check from `df12-copy`.

## Key constraints

- British English, Oxford spelling (-ize, -our, -re, -yse).
- Sentence-case headings.
- 80-column paragraph wrapping, 120-column code wrapping.
- Active voice unless the agent is genuinely unknown or irrelevant.
- Tables for stakeholder mapping, comparison matrices, and any
  structured data.
- Companion documents referenced by path, not by hyperlink alone.
- One question per elicitation turn; persist progress after each
  resolution.
- Open questions section is mandatory, even if empty (in which case
  record explicitly that no open questions remain).
