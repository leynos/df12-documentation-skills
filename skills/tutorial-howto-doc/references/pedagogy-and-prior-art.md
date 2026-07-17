# Pedagogy and prior art

This file is the theoretical grounding for the `tutorial-howto-doc`
skill. The skill's rules are not arbitrary house preferences; each
traces back to an established idea in documentation practice or
instructional design. Read this once to understand *why* the workflow
insists on what it insists on, then consult it when a rule feels
inconvenient and you are tempted to break it.

Everything here is a synthesis in our own words. Sources are cited, so
the originals can be consulted; nothing below is a substitute for them.

## The organizing distinction: study versus work

The most useful single idea in practical documentation is that a reader
is always in one of two relationships with a craft: **acquiring** it
(study) or **applying** it (work). A learner mastering a skill and a
practitioner getting a job done have different needs, even when the
underlying task looks identical.

This produces the two modes this skill writes:

- A **tutorial** serves the reader at *study*. Its obligation is a
  successful *learning experience*. What matters is what the learner
  does and what they take away — not what they produce.
- A **how-to guide** serves the reader at *work*. Its obligation is to
  help them *accomplish a task* correctly and safely. What matters is
  the result.

A worked analogy from medicine makes the difference vivid. A medical
student learning to suture on a practice pad is at study: the cut is
worthless, the *learning* is the point, the instructor is responsible
for safety, and the exercise is contrived to guarantee a useful
encounter. A qualified surgeon following a procedure manual during an
operation is at work: the result is everything, competence is assumed,
the real world supplies complications, and responsibility sits with the
practitioner. A document that confused the two would, in that domain, be
lethal. In software, it is merely expensive — but expensive every single
time.

This study/work distinction, and the four-quadrant map that places
tutorials and how-to guides alongside reference and explanation, is the
core of **Diátaxis**, the framework by **Daniele Procida**. This skill
borrows that distinction as its classification test and credits it
plainly. Diátaxis covers four kinds of documentation; this skill
deliberately writes only the two action-oriented ones and links out to
the other two.

The common-but-wrong shortcut is to equate tutorial with *basic* and
how-to with *advanced*. Not so. A how-to can cover something utterly
basic (how to fill in a form correctly); a tutorial can teach something
advanced (a lesson for experienced anaesthetists on difficult
intubations is still a lesson). The axis is study versus work, not easy
versus hard.

Source: Diátaxis, <https://diataxis.fr/>, especially "The difference
between a tutorial and how-to guide". Originating talks by Daniele
Procida: "What nobody tells you about documentation" (PyCon Australia
2017 and Write the Docs Prague 2017).

## Carroll's minimalism and the paradox of sense-making

In the 1980s, **John M. Carroll** and colleagues studied people learning
to use computer systems and found something counter-intuitive: the less
people knew, the *less* they used the manual. The classical model —
novices read the docs, experts improvise — was backwards in practice.

The reason is the **paradox of sense-making**. People do not approach a
new system as empty vessels. They arrive with a mental model of the task
and how it ought to work, and they are *already* trying things,
recovering from mistakes, and relating the new to the known. They are,
in Carroll's phrase, "too busy learning to make much use of the
instructions". When a procedure contradicts their mental model, they
trust the model, not the procedure.

Carroll's response was **minimalism** — not "write less" as a style tic,
but: *minimize the extent to which the instructional material obstructs
the learner's own sense-making*. The commonly recited four principles
(as distilled by JoAnn Hackos and by Hans van der Meij and Carroll) are:

1. **Choose an action-oriented approach.** Get the reader doing
   meaningful work immediately, not reading preamble.
2. **Anchor the tool in the task domain.** Frame instruction around what
   the reader is trying to accomplish, not around the system's features.
3. **Support error recognition and recovery.** Errors are inevitable and
   are *teachable moments*. Help the reader notice and recover, rather
   than pretending a clean run is the only path.
4. **Support reading to do, study, and locate.** Let the reader skim,
   dip in, and find their place; do not demand linear cover-to-cover
   reading.

Two cautions Carroll himself stressed, which this skill inherits:

- Minimalism is **not** a solution to the paradox — there is no
  "Nurnberg Funnel" that pours knowledge into a head. It is an
  accommodation that interferes less and supports more.
- Stripping a procedure down to bare steps is *not* minimalism if it
  still assumes the reader will obey against their own mental model.
  Action-orientation without anchoring in the reader's real goal fails
  the same way verbose manuals do.

How this skill uses it: principle 1 underwrites "guide action, do not
teach theory" and "results early and often"; principle 2 underwrites
"how-tos are framed from the user's goal, not the machine's"; principle
3 underwrites the "narrative of the expected" and the hazard callouts;
principle 4 underwrites scannable structure and outward links.

Sources: J. M. Carroll, *The Nurnberg Funnel* (MIT Press, 1990) and
*Minimalism Beyond the Nurnberg Funnel* (MIT Press, 1998); H. van der
Meij and J. M. Carroll, "Principles and Heuristics for Designing
Minimalist Instruction", *Technical Communication* 42(2), 1995; J.
Hackos on the four principles. Overview:
<https://www.instructionaldesign.org/theories/minimalism/>.

## Gagné's nine events of instruction

**Robert Gagné** (1965) described nine events that support the mental
conditions for learning. They map cleanly onto a good tutorial and are
the skeleton behind the tutorial anatomy:

1. **Gain attention** — open with something that engages, not boilerplate.
2. **Inform the learner of the objective** — say what the tutorial will
   build, so they can picture the destination.
3. **Stimulate recall of prior learning** — connect to what the reader
   already knows; this is also where the (low) assumed starting
   point.
4. **Present the content** — the steps, in a meaningful order.
5. **Provide learning guidance** — worked examples, the narrative of the
   expected, pointing out what to notice; scaffolding that can be
   removed as competence grows.
6. **Elicit performance (practice)** — the reader *does* each step; this
   is the heart of a tutorial, not an afterthought.
7. **Provide feedback** — show the expected output, so the reader can
   confirm they are on track. The absent tutor speaks through this.
8. **Assess performance** — the reader sees the working artefact; the
   result is its own assessment.
9. **Enhance retention and transfer** — the closing summary, the
   invitation to repeat, and the links to what comes next.

How this skill uses it: events 2, 5, 6, and 7 are why a tutorial states
its destination, supplies worked examples, makes the reader act, and
always shows expected output. Note that events 6 and 7 — *do*, then
*confirm* — are exactly the step pattern the anatomy enforces.

Source: Gagné, Briggs and Wager, *Principles of Instructional Design*,
4th ed. (1992). Overview:
<https://www.niu.edu/citl/resources/guides/instructional-guide/gagnes-nine-events-of-instruction.shtml>.

## Cognitive load theory, worked examples, and scaffolding

**Cognitive load theory** (John Sweller and others) holds that working
memory is severely limited and that learning fails when it is
overloaded. Load comes in kinds worth separating:

- **Intrinsic load** — the inherent difficulty of the material. Manage
  it by breaking a complex task into smaller steps and sequencing them,
  so each builds on the last.
- **Extraneous load** — load imposed by *how* the material is presented,
  not by the material itself. This is wasted effort, and it is what
  premature explanation, option sprawl, and poor ordering inflict on a
  reader. Minimize it.

Two consequences this skill leans on heavily:

- **The worked-example effect.** Novices learn more from studying a
  fully worked example than from being told an abstract rule and left to
  apply it. Concrete-first beats general-first; the general pattern
  emerges from the particular instances. This is why tutorials stay
  concrete and show real commands and real output rather than describing
  them in the abstract.
- **Scaffolding** (rooted in Vygotsky's *zone of proximal development*).
  Provide support that lets the learner succeed at something just beyond
  their independent reach, then remove it as they gain competence. A
  tutorial is scaffolding made of prose: heavy support early, the
  explicit "where to type this" and "what the result looks like",
  tapering as the learner finds their feet.

A practical limit falls out of all this: keep a procedure to roughly
seven primary steps, and one action per step. When a sequence runs
longer, intrinsic load is too high for one sitting and the scope should
be split. The Good Docs Project codifies the same limits (≤7 primary
steps, ≤4 substeps; tutorials of 15–60 minutes).

Sources: J. Sweller, "Cognitive Load During Problem Solving" (1988) and
subsequent work; overviews of cognitive load theory and scaffolding in
instructional practice, e.g.
<https://www.structural-learning.com/post/cognitive-load-theory-a-teachers-guide>.

## The Good Docs Project templates

**The Good Docs Project** publishes community-maintained, openly
licensed templates for documentation types, including a tutorial
template and a how-to template. They are practitioner consensus rather
than theory, and they corroborate the structural rules this skill uses:
explicit learning objectives and audience for tutorials; problem
statement and prerequisites for how-tos; imperative verbs; step limits;
and a clear separation between the learning-oriented and task-oriented
modes. The anatomy reference files draw on this consensus.

Source: <https://www.thegooddocsproject.dev/> (tutorial and how-to
templates).

## How the sources converge

The four traditions agree more than they differ, and the agreement is
what this skill encodes:

- **Doing beats telling.** Diátaxis ("ruthlessly minimize explanation"),
  Carroll (action-orientation), Gagné (elicit performance), and CLT (the
  worked-example effect) all say the reader learns and accomplishes by
  acting, not by reading theory.
- **Meet the reader where they are.** Carroll's paradox, Gagné's "recall
  of prior learning", and scaffolding all insist that instruction must
  start from the reader's real state and goal.
- **Confirm at every step.** Gagné's feedback event and Diátaxis's
  "narrative of the expected" both make the document stand in for an
  absent teacher by telling the reader what success looks like.
- **Respect the limits of attention.** CLT and the step-count
  conventions all push toward small, single-purpose, well-ordered steps
  and a bounded scope.

When a drafting decision is genuinely unclear, return to the first
point of convergence: does this sentence help the reader *act*, or is it
there because the author wanted to *tell*? Cut toward action.
