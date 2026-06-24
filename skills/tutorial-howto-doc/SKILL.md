---
name: tutorial-howto-doc
description: >
  Write and revise tutorials and how-to guides — the two practical,
  action-oriented kinds of documentation. Use this skill whenever the
  user asks to write, draft, structure, or fix a tutorial, a getting-
  started guide, a walkthrough, a lesson, a how-to, a task guide, a
  recipe, a procedure, or a troubleshooting guide. Also trigger when a
  document tries to both teach and get a job done at once, when a
  "tutorial" reads like a reference dump, when steps fail for readers,
  or when the user is unsure whether they need a tutorial or a how-to.
  The skill first classifies the document by user need (study versus
  work), then drives a test-the-path workflow: scope the journey or the
  goal, execute it end to end recording real output, draft to the right
  anatomy, edit out blurred boundaries, and hand off to reference and
  explanation. It is grounded in Diátaxis, Carroll's minimalism, Gagné's
  events of instruction, and cognitive load theory.
---

# Tutorials and how-to guides

A skill for producing the two *practical* kinds of documentation: the
tutorial, which serves a reader **at study**, and the how-to guide,
which serves a reader **at work**. Both guide *action* — what the reader
*does* — and neither exists to convey theory. That is the job of
reference and explanation, which this skill points to but does not
write.

The single most expensive mistake in practical documentation is
conflating these two modes. A tutorial that behaves like a how-to
abandons the beginner; a how-to that behaves like a tutorial wastes the
expert's time and patronises them. Most of this skill's value is in
forcing the classification *before* a line is drafted, then holding the
chosen mode honest through writing and editing.

This skill is inspired by, and credits, the Diátaxis framework by
Daniele Procida, alongside older work in instructional design. It does
not reproduce that material; it synthesises it into an executable
workflow. See `references/pedagogy-and-prior-art.md` for the grounding
and full attribution.

## Before starting

Read the reference files as the workflow calls for them:

- **Pedagogy and prior art**: `references/pedagogy-and-prior-art.md`.
  Read once for the theory behind every rule below — the study/work
  distinction, Carroll's minimalism and the paradox of sense-making,
  Gagné's events of instruction, and cognitive load theory. Read it
  before writing your first tutorial; skim it before each later one.
- **Tutorial anatomy**: `references/tutorial-anatomy.md`. Read before
  drafting a tutorial.
- **How-to anatomy**: `references/how-to-anatomy.md`. Read before
  drafting a how-to guide.
- **Testing the path**: `references/testing-the-path.md`. Read when the
  guide's steps could be checked by a machine — how to make the walk
  durable (docs as tests) and how a guide's structure maps onto
  Given/When/Then, deferring the BDD mechanics to project testing skills.
- **Editing checklist**: `../tech-design-doc/references/editing-checklist.md`.
  Read before the editing pass for the fluff-elimination protocol shared
  across the df12 documentation skills.

## Governing principles

1. **Classify before you write.** Every practical document serves a
   reader who is either *acquiring* a skill (study → tutorial) or
   *applying* one (work → how-to). Decide which, explicitly, before
   drafting. When in doubt, ask the compass questions: is the reader
   here to *learn*, or to *get something done*? The answer dictates the
   anatomy, the language, and what you are allowed to leave out.

2. **Guide action; do not teach theory.** Both modes are sequences of
   things to *do*. Theory belongs elsewhere. Give the minimal
   orientation needed to act — "we use HTTPS because it is safer" — and
   link to an explanation for the reader who wants the rest. Explanation
   wedged into a procedure breaks the reader's flow and their attention.

3. **Respect the paradox of sense-making.** Readers do not arrive as
   blank slates waiting to be filled. They carry mental models, they
   improvise, and they make errors. Instructions that ignore this are
   ignored in turn. Anchor every step in something the reader is trying
   to achieve, and treat a likely error as a teachable moment to flag,
   not a failure to hide. (Carroll.)

4. **Manage cognitive load.** Working memory is small. Keep steps short
   and one action each, deliver a visible result early and often, prefer
   a worked example over an abstract rule, and cap a procedure at around
   seven primary steps. When a sequence grows past that, the scope is
   wrong — split it. (Cognitive load theory; the Good Docs Project.)

5. **A tutorial must be reliable; a how-to must be honest.** In a
   tutorial the instructor is absent and cannot rescue a stuck learner,
   so the path must work for every reader every time, and the prose must
   stand in for the teacher with a running narrative of the expected. A
   how-to operates in the real world, which it cannot control, so it
   must warn of forks and failure modes rather than pretend they do not
   exist.

6. **Test the path — and keep it tested.** Steps that have not been
   executed are hypotheses, not instructions. Run the tutorial or the
   how-to end to end — or have a subject-matter expert demonstrate it —
   and record the *actual* output. A walk done once verifies the promise
   for a moment; where the steps are machine-checkable, make the walk
   *durable* by encoding the happy path as an automated test that runs in
   CI ("docs as tests"). A guide already reads as Given/When/Then — its
   prerequisites, its actions, and its narrative of the expected — so the
   confirmations you write double as the test's assertions. See
   `references/testing-the-path.md`; defer the BDD mechanics to the
   project's testing skills. Re-test after every notable release; these
   are the documents that rot fastest.

7. **The document is living.** A tutorial is the most revision-hungry
   page you own because its end-to-end story cascades when the product
   changes. Ship it complete for today, expect to revise it, and note
   the retest cadence in the handoff.

## The classification test

Run this first, every time. It is adapted from the Diátaxis compass.

| If the reader is… | …they need… | serving… |
| --- | --- | --- |
| learning the tool | a **tutorial** | acquiring skill (study) |
| getting a known job done | a **how-to guide** | applying skill (work) |
| looking up a fact or option | *reference* (not here) | cognition, at work |
| trying to understand *why* | *explanation* (not here) | cognition, at study |

Two questions resolve almost every case:

- **Study or work?** Is the reader here to become able, or to get a
  result? A driving lesson versus a route to the airport.
- **Managed path or real world?** Can you control everything the reader
  encounters (tutorial), or must you prepare them for what the world
  throws up (how-to)?

Tell-tale signs you have misclassified:

- A "tutorial" that opens with prerequisites the beginner cannot have,
  offers three alternative commands per step, or assumes the reader
  already knows where things are → it is really a how-to.
- A "how-to" that explains concepts, refuses to assume competence, and
  contrives a clean sandbox → it is really a tutorial, or it is two
  documents fused together.

If a single document genuinely must do both, that is two documents.
Split them and cross-link.

## Workflow

Execute these phases in order. Do not draft prose before the scope is
agreed, and do not publish before the path is tested.

### Phase 0 — Intake and classification

Find what already exists before writing anything:

- Files attached to the prompt.
- `README.md`, `docs/`, and any existing `docs/tutorials/` or
  `docs/how-to/` trees (the skill may be revising, not creating).
- The product itself: install it, read its CLI help, find the real
  commands. A tutorial or how-to written without touching the product
  is fiction.
- `docs/context.md` for the ubiquitous language, if present.

Then **classify** using the test above, and state the verdict to the
user in one line: "This is a tutorial, because the reader is learning
X," or "This is a how-to, because the reader already knows X and needs
to accomplish Y." If the request bundles both, propose the split.

### Phase 1 — Scope

**For a tutorial**, agree:

- The single, concrete artefact the learner will have built or done by
  the end ("a running, deployed to-do API"), stated up front so they
  can picture the destination. Avoid "you will learn…"; describe what
  *we will make*.
- The learner's assumed starting point — and keep it genuinely low.
- The concepts, tools, and commands the learner must *encounter* along
  the way (distinct from what they must be *told*). List them; the
  journey must touch each one.
- A time budget. Fifteen to sixty minutes is the workable range; longer
  tutorials overwhelm. If the scope will not fit, cut it, do not rush
  it.

**For a how-to**, agree:

- The real-world goal, framed from the *user's* perspective, not the
  machinery's: "restore a database from a backup", not "use the
  `pg_restore` command". Title it as exactly what it shows: "How to
  restore a database from a backup."
- The competence you may assume (so you can omit the obvious).
- Sensible entry and exit points; a how-to need not be end-to-end
  complete the way a tutorial must be.
- The forks and error scenarios the real world will present, and the
  single safest, surest path you will recommend through them.

For either mode, also decide the **verification strategy** now: are the
steps machine-checkable, and if so at what level — the embedded code
snippets, the end-to-end path, or both — and with which tool? This is a
writing decision, because committing to verification sharpens how you
phrase steps (atomic, imperative, each with explicit expected output).
See `references/testing-the-path.md`.

### Phase 2 — Walk the path

This phase is non-negotiable and is where most defects are caught.

- **Tutorial**: perform the whole journey yourself from the assumed
  starting state, ideally on a clean machine or fresh project. Capture
  the *exact* output of each step — prompts, log lines, screenshots.
  Note where a learner is likely to slip, and what the early-warning
  sign of each slip looks like. Reliability is built here, not asserted
  later.
- **How-to**: execute the task start to finish. Confirm the recommended
  path, identify the forks worth mentioning, and record the genuine
  error messages a user will hit and how to recover. Where you cannot
  run it, have an SME demonstrate and record the session.

If the path cannot be made to work reliably, stop and fix the scope or
the product before writing — do not paper over a broken path with prose.

Where a verification strategy was chosen in Phase 1, **capture the walk
as the test** rather than throwing it away. The commands you run become
the actions, the output you record becomes the assertions, and the clean
starting state becomes the setup — one disciplined walk yields both the
captured output for the prose and the executable scenario. See
`references/testing-the-path.md`.

### Phase 3 — Draft

→ Read `references/tutorial-anatomy.md` or
`references/how-to-anatomy.md` for the section-by-section structure.

While drafting a **tutorial**:

- Maintain a *narrative of the expected*: "After a few seconds, the
  server responds with `Listening on :8080`." Show the real output you
  captured.
- Point out what to notice ("the prompt now shows your branch name").
- Keep results coming early and often; let each step produce something
  visible.
- Ruthlessly minimise explanation. One clause of justification, then a
  link. The learner is *doing*, not studying.
- Stay concrete and particular. No options, no "you could also". One
  line to the conclusion.
- Use the first-person plural: "we", "let's". The tutor is present in
  the prose.

While drafting a **how-to**:

- Use conditional imperatives: "If you want X, do Y."
- Assume competence; omit what any practitioner already knows.
- Prefer usefulness to completeness; start and end somewhere reasonable
  and let the reader join it to their own work.
- Warn about the unexpected — callouts for the irreversible step, the
  destructive flag, the long-running command.
- Seek flow: order steps the way the work actually flows, minimising
  context-switching and held-open thoughts.

### Phase 4 — Editing pass

→ Read `../tech-design-doc/references/editing-checklist.md` for the
shared protocol, then apply these mode-specific passes.

The boundary-blur hunt is the most important edit:

- **Explanation creep (tutorials and how-tos).** Find every sentence
  that explains *why* and ask whether the reader needs it *now*. Cut it
  to a clause and a link, or move it to an explanation document.
- **Teaching creep (how-tos).** Find every passage that assumes no
  competence or defines basics. Delete or link out; a how-to addresses
  the already-competent.
- **Option sprawl (tutorials).** Find every "you can also", "or", or
  alternative command. Remove it; a tutorial follows one line.
- **Machine-shaped goals (how-tos).** Find titles and openings framed
  around a command or feature rather than a user goal. Rewrite around
  what the user is trying to achieve.
- **Missing expected output (tutorials).** Find every step that asks the
  reader to act without telling them what they should then see. Add the
  captured result.
- **Unwarned hazard (how-tos).** Find every irreversible or destructive
  step with no callout. Add the warning before the step, not after.
- **Step bloat (both).** Count primary steps. Past about seven for a
  how-to, or any step doing more than one thing, split or regroup.

### Phase 5 — Handoff and links

- Place the document under the right tree (`docs/tutorials/` or
  `docs/how-to/`) unless the user specifies otherwise.
- Add the outward links the body deliberately omitted: explanation for
  the *why*, reference for the exhaustive options, the next tutorial or
  related how-to for what comes after.
- For a tutorial, end with a brief, mildly admiring summary of what the
  learner built, and a pointer to where they go next.
- If the walk was captured as a test, commit the feature file and step
  definitions alongside the document and wire them into CI, so the
  retest cadence is automatic.
- Record the retest cadence (e.g. "re-run against each minor release"),
  noting whether it is enforced by CI or left to a manual reminder.
- Note any domain terms introduced that belong in `docs/context.md`.

## Language

**Tutorials.**

- "In this tutorial, we will build…" — set the destination.
- "First, run X. You should see Y." — act, then confirm.
- "Notice that…", "Let's check that…" — close the loop of learning.
- "We use X here because it is safer (see [explanation])." — minimal
  justification, then a link.
- "You have built a working…" — name the achievement at the end.

**How-to guides.**

- "This guide shows you how to…" — name the goal.
- "If you want X, do Y. To achieve W, do Z." — conditional imperatives.
- "Refer to [reference] for the full list of options." — do not inline
  the reference.
- "Warning: this step cannot be undone." — flag hazards before they
  occur.

## Failure modes

- **The product fights the path.** The clean tutorial journey cannot be
  made reliable because the product itself is awkward at that point.
  Surface this — it is product feedback, not a documentation problem to
  hide. A tutorial cannot paper over a step that fails for some readers.

- **The user wants one document to teach and to do.** A common request:
  "write a tutorial that's also the reference for deployment." Decline
  the fusion, explain the cost briefly, and offer the split with
  cross-links.

- **No clean environment to test in.** Recording real output requires a
  reproducible starting state. If none exists, that is the first thing
  to establish; until then, mark outputs as unverified rather than
  inventing them.

- **The scope keeps growing.** Every tutorial wants to become a course
  and every how-to a manual. Hold the line at one artefact / one goal
  and one sitting; spin additional scope into follow-on documents.

- **The author knows too much.** Expertise makes the obvious invisible
  ("just configure the gateway") and the basic seem unworthy of mention.
  For tutorials especially, the cure is watching a real beginner attempt
  the path; short of that, distrust every step you found "too trivial to
  write down".

## Anti-patterns to avoid

- **The reference dump in tutorial's clothing.** A wall of every option
  and flag, no narrative, no destination. It informs cognition, not
  action — it is reference, mis-shelved.

- **The lecture.** Paragraphs of theory before the reader does anything.
  Learners learn by doing; move the theory to explanation and let them
  act on page one.

- **The choose-your-own-adventure tutorial.** Branches and alternatives
  in what should be a single managed line. Every fork is a chance to get
  lost; a tutorial eliminates the unexpected.

- **The machine's-eye how-to.** "Using the `--force` flag" as a title,
  steps that walk the tool through its motions rather than walking the
  user toward a goal. Reframe around the human's project.

- **The silent leap.** A step that produces no visible result, or whose
  result the document never states, so the reader cannot tell whether it
  worked. Every step earns its confirmation.

- **The untested procedure.** Steps written from memory or from the spec
  rather than from execution. They drift from reality and fail readers
  at the worst moment.

- **The empty scaffold.** Creating `tutorials/`, `how-to/`,
  `reference/`, and `explanation/` folders with nothing in them. Build
  the content first; the structure earns its place by being filled.

## Tool integration notes

### Relationship to reference and explanation

This skill deliberately writes only the two action-oriented modes. The
*why* belongs in explanation and the exhaustive *what* in reference.
Where the draft is tempted into either, the correct move is a link out,
not an inline digression. If those documents do not yet exist, note them
as companions to be written — do not absorb their content here.

### Relationship to `terms-of-reference-doc` and `tech-design-doc`

Those skills define the problem space and the system. A tutorial or
how-to documents the product *as it is for the user* once it exists.
Read them for the audience definition and the domain vocabulary, but do
not let solution-space or problem-space framing leak into a practical
guide.

### Relationship to `en-gb-oxendict`

Apply the British/Oxford spelling rules throughout. Load that skill if
the locale conventions are in question.

### df12 copy skill

If producing a tutorial or how-to for a df12 Productions product, load
the `df12-copy` skill for voice. Note the tension: df12 voice is playful,
but a tutorial's narrative of the expected and a how-to's hazard
warnings must stay unambiguous. Where wit and clarity conflict in a
step, clarity wins.

## Credits and prior art

This skill synthesises, and gratefully credits, the following. None is
reproduced; each is cited so a reader can go to the source.

- **Diátaxis** — Daniele Procida. The four-kinds map and the
  study/work compass that underpin the classification test.
  <https://diataxis.fr/>. Originating talk: "What nobody tells you
  about documentation" (PyCon AU / Write the Docs, 2017).
- **Minimalism / *The Nurnberg Funnel*** — John M. Carroll. The paradox
  of sense-making, action-orientation, and error recovery.
- **Nine Events of Instruction** — Robert Gagné. The shape of an
  effective lesson.
- **Cognitive load theory** — John Sweller and others. Worked examples,
  small steps, and load management.
- **The Good Docs Project** — community tutorial and how-to templates.
  <https://www.thegooddocsproject.dev/>.
- **Docs as Tests** — Manny Silva. The principle that documentation
  should verify as well as inform, behind the durable test-the-path
  guidance. <https://www.docsastests.com/>.

Full references with URLs are in `references/pedagogy-and-prior-art.md`
and `references/testing-the-path.md` (the latter also credits Sybil,
pytest-bdd, rstest-bdd and `@aboviq/bun-test-cucumber`).

## Key constraints

- British English, Oxford spelling (-ize, -our, -re, -yse).
- Sentence-case headings.
- 80-column paragraph wrapping, 120-column code wrapping.
- Imperative verbs in steps; never the *-ing* form (it translates
  poorly). Start with a verb: "Run", "Set up", "Connect".
- One action per step; around seven primary steps maximum per
  procedure.
- Show real, captured output — never invented output.
- Theory and exhaustive options are linked, not inlined.
- Classify the document (tutorial or how-to) explicitly before drafting.
