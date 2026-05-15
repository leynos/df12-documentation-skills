# Elicitation protocol

How to conduct the structured interview that produces a terms of
reference. Read this before Phase 2 (Elicitation).

## Purpose

Elicitation extracts domain knowledge from the user's head and from
their existing artefacts, then persists it in a form the rest of the
project can build on. It is the part of the workflow that the user
cannot delegate — only they know which segment of the market they are
serving, what their non-goals are, and which assumptions they are
willing to bet on.

The skill's job in elicitation is to ask sharp questions in the right
order, challenge fuzzy answers, surface contradictions, and write
down the results before they evaporate.

## Cardinal rules

1. **One question per turn.** Two questions in a single turn produces
   one answer. Three produces a torrent of prose that conflates the
   answers. If a question has sub-parts, ask the first, get the answer,
   then ask the next.

2. **Dependency order beats section order.** "Who is the primary user?"
   gates "what job are they doing?" gates "what does success look like
   for them?" Answer in dependency order even if it means jumping
   between sections. Coherence in the final document matters more than
   the order in which it was assembled.

3. **Persist after every resolution.** Write to
   `docs/terms-of-reference.md` after each substantive answer, not at
   the end. The user can read what has been recorded and catch
   misinterpretations before they compound.

4. **Challenge fuzzy language; do not rephrase it.** When the user says
   "enterprises", do not write down "enterprises". Ask which kind,
   which size, which sector. Then write down the precise answer.

5. **Surface tensions explicitly.** If the user's answer contradicts an
   earlier one, name the contradiction: "Earlier you described the
   primary user as solo developers; this answer implies platform
   engineering teams at large companies. Which is authoritative?"

6. **Accept the exit.** The user can declare "good enough" at any
   point. Mark the remaining items in the Open Questions section and
   proceed to drafting. A v0.1 with acknowledged open questions is
   more useful than a v1.0 that took six sessions.

## Dependency tree of decisions

Questions are not equal. Some are foundational; others depend on
foundations being settled. The rough order:

```
Domain
  └─ Primary user
      └─ Job-to-be-done
          ├─ Goals
          │   └─ Success criteria
          └─ Non-goals
Market context (parallel to user, sharpens the gap)
Stakeholders (after primary user; refines secondary/non-users)
Constraints and assumptions (cross-cutting; revisited throughout)
Open questions (residue; populated continuously)
```

Resolve upstream items before downstream ones. A "primary user" that
keeps changing invalidates everything below it.

## Question patterns by section

The patterns below are starting points. The interview is responsive,
not scripted; follow what the user says, but use these as anchors when
the conversation drifts.

### Background and motivation

- "Why is this worth doing now and not five years ago?"
- "What changed in the world — technically, commercially, legally —
  that made this possible or necessary?"
- "If this project did not exist, what would the user do instead?"
- "Who, specifically, asked for this — or noticed the gap?"

Warning sign: the user describes the product's features in response.
Push back: features describe the *what*, not the *why*. Ask again.

### Domain

- "What field of practice does this belong to?"
- "What are the standard ways things are done in this field?"
- "What are the unwritten rules — assumptions a newcomer would
  violate without knowing?"
- "What prior art does this build on, replace, or coexist with?"
- "Are there regulatory or contractual constraints that shape what
  is even possible?"

When the user uses a domain term — "observability", "ETL",
"reconciliation" — ask whether it appears in `docs/context.md`. If
yes, confirm the definition. If no, ask the user to define it, and
flag it for promotion to `context.md`.

### Market context

- "Who else does this — even badly?"
- "What is the current default the user uses for this job, including
  manual processes and spreadsheets?"
- "Where specifically does the current default fail?"
- "Is the gap a capability gap, an ergonomics gap, a cost gap, or a
  trust gap?"
- "If a major competitor shipped exactly this product tomorrow, what
  would the user choose between them?"

Warning sign: "there is nothing like this on the market." This is
almost always wrong. Something occupies the space — a script, a
spreadsheet, a meeting, a different product class. Ask harder.

### Users and stakeholders

For each candidate user type:

- "What is their role and working context?"
- "What is their technical fluency relative to this domain?"
- "What is their current alternative for the job?"
- "What would they actively ignore or dislike?"
- "Is this person paying, using, or both?"

Then:

- "Who else interacts with the product without being its target user?"
- "Who funds or sponsors this work?"
- "Who can veto a release?"
- "Who is explicitly *not* a user of this product?"

The non-user question is often the most useful. It clarifies the
boundary of the primary user definition.

### Job to be done

Use the canonical structure as a forcing function:

> "Tell me the job in this form: when *[situation]*, *[user]* wants to
> *[motivation]*, so they can *[outcome]*."

Then probe:

- "What triggers the user to look for a tool like this?"
- "What does the user do immediately before and immediately after
  this job?"
- "Is the job something the user does daily, occasionally, or once?"
- "What does the user hire the current default to do? What does it
  do well? Where does it fall short?"

Warning sign: the user describes a feature ("they want to export
CSV") instead of a job. Ask: "Why do they want CSV? What do they do
with it after?" Keep asking why until you reach a situation and an
outcome.

### Goals and non-goals

For goals:

- "What would the product have to do for you to consider it a
  success?"
- "If we built this and users adopted it but did not [X], would we
  call it a success?"
- "Is this goal verifiable — could a reasonable observer check
  whether we achieved it?"

For non-goals:

- "What might a reasonable reader assume is in scope that is not?"
- "What feature requests will you say no to, and why?"
- "What user segments are out of scope?"
- "What problem in this domain are you *not* solving?"

A goals list of fifteen items with a non-goals list of two is a smell.
Force the user to either cut goals or expand non-goals until the lists
are roughly comparable.

### Success criteria

- "What signal tells you the job is being done?"
- "Is that signal measurable, and if so, how?"
- "What is the threshold above which you would call this a success?"
- "What signal tells you the product is operationally sustainable?"
- "What signal tells your sponsor or business this was worth doing?"

Warning sign: "users will be happy" or "we will know it when we see
it." Push for a measurable signal, or record that the criterion is
currently unmeasurable as an open question.

### Constraints and assumptions

Constraints:

- "What is fixed regardless of design choices?"
- "What deadlines, budgets, or platform requirements bind the work?"
- "What regulatory or contractual obligations apply?"

Assumptions:

- "What are you taking as given without verification?"
- "What happens if that assumption turns out to be wrong?"
- "What other teams or third parties does this depend on?"

Every assumption gets paired with a failure consequence. Assumptions
without consequences are facts; if there is no consequence, the
assumption is not load-bearing.

### Open questions

Throughout the interview, log items as they emerge. At the end:

- "Which of these unresolved items would block design work?"
- "Which can wait until after v1?"
- "For each, what evidence or decision would close it?"
- "Who can resolve it?"

## Challenging fuzzy language

When the user uses one of these terms, do not write it down. Ask the
clarifying question instead.

| Fuzzy term | Clarifying question |
|---|---|
| "users" | Which user type? Primary, secondary, both? |
| "enterprises" | What size? What sector? What maturity? |
| "developers" | Which languages? Which roles? Which seniority? |
| "the team" | Which team? Internal, customer, both? |
| "easy" | Easy compared to what? Measured how? |
| "fast" | Faster than what? In what units? |
| "scalable" | To what scale? Under what conditions? |
| "modern" | Compared to what? In what specific way? |
| "robust" | Against what failure mode? Tolerating what? |
| "intuitive" | Intuitive to whom? With what prior knowledge? |
| "industry-standard" | Which industry? Whose standard? Cite. |
| "best practice" | Whose practice? When? With what evidence? |
| "the right thing" | Right by what criterion? Right for whom? |
| "obviously" | Obvious to whom? Worth stating explicitly. |

When the user pushes back ("you know what I mean"), persist gently:
the terms of reference is the document the next developer reads
without the user in the room. They will not know what the user means.

## Surfacing tensions

Two kinds of tension matter:

1. **Internal contradictions.** The user's current answer conflicts
   with an earlier one. Surface it:

   > "Earlier you said the primary user is solo developers working on
   > personal projects. This answer about audit requirements implies a
   > regulated enterprise environment. Are both in scope, or has the
   > primary user shifted?"

2. **External contradictions.** The user's answer conflicts with an
   existing artefact (README, prior ToR, context.md). Surface it:

   > "The README describes this as a CLI tool for offline use. You
   > just described a SaaS dashboard. Which is authoritative?"

In both cases, record the resolution explicitly. If the resolution
changes earlier sections, update them — do not leave the document
internally inconsistent.

## Save-as-you-go discipline

After every substantive answer:

1. Write the resolved content to the appropriate section of
   `docs/terms-of-reference.md`.
2. Update the status tag if applicable: `[ASSUMED]` becomes `[KNOWN]`,
   `[OPEN]` becomes `[KNOWN]` or remains `[OPEN]` with refined
   wording.
3. Update the Open Questions section if a new question surfaced.
4. Briefly state what was just written. The user can read it and
   correct misinterpretations immediately, when the cost of correction
   is lowest.

Do not batch writes to the end of the session. The user has spoken
for ten minutes; they will not remember the precise wording they used
when they read the document tomorrow.

## Exit conditions

The interview ends when one of the following holds:

1. **All `[OPEN]` items are resolved.** The ideal case. Proceed to
   drafting.

2. **The user declares "good enough".** Mark remaining `[OPEN]` items
   in the Open Questions section with resolution criteria. Note in
   the front matter that the document is v0.1 with acknowledged open
   questions. Proceed to drafting.

3. **The remaining `[OPEN]` items require external input the user
   cannot provide in the session.** Market research, legal advice,
   stakeholder interviews. Mark them, record what is needed, and
   proceed to drafting v0.1 with the gaps acknowledged.

4. **The interview has surfaced a fundamental disagreement that
   cannot be resolved in the session.** A co-founder dispute, an
   unsettled business model, a regulatory uncertainty. Capture both
   positions in the Open Questions section, note that resolution is
   required before design can proceed, and stop. A terms of reference
   that papers over fundamental disagreement is worse than no terms
   of reference.

The skill should *not* try to grind through every open item if the
user's energy or attention is flagging. Diminishing returns set in
quickly. A clean v0.1 with five open questions beats a thrashed
attempt at v1.0.

## Anti-patterns in elicitation

- **The leading question.** "You probably want X, right?" The user
  agrees to whatever sounds plausible. Ask open questions; let the
  user produce the answer.

- **The compound question.** "Who is the user and what is their job
  and what does success look like?" Three questions, one answer.

- **The premature summary.** "So what you're saying is…" followed by
  a paraphrase that smooths over the messy parts. The messy parts
  are where the design decisions live. Resist the urge to summarise
  early.

- **The vocabulary creep.** The skill starts using the user's fuzzy
  term and forgets to challenge it. After three turns of "the
  platform", everyone has forgotten that "platform" was never
  defined. Catch this in the next save-as-you-go pass.

- **The infinite grill.** Endless probing on a single decision long
  past the point of diminishing returns. The user is bored, the
  decision is good enough, and the skill keeps asking. Move on.

- **The implicit answer.** The skill assumes it knows what the user
  meant rather than asking. The cost of one clarifying question is
  trivial; the cost of building on a wrong assumption is enormous.
