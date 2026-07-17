# Tutorial anatomy

The section-by-section structure for a tutorial — a *lesson* that takes
a learner, by the hand, through a successful first encounter with the
product. Read this before drafting. The ordering follows the shape of an
effective lesson (Gagné's events; see
`pedagogy-and-prior-art.md`).

A tutorial serves the reader **at study**. Its success is measured by
what the learner gains, not by what they produce. Hold that in mind: the
deployed app at the end is the *occasion* for learning, not the point of
it.

## Front matter

- **Title.** Name the journey, not a feature. "Build and deploy a first
  API" beats "The deployment subsystem". Avoid "Learn about…".
- **One-line destination.** A single sentence the learner reads before
  anything else: "This tutorial builds a small to-do API and deploys it
  to a live URL. Along the way, the path introduces routing, a database,
  and a deploy command." Set the picture; do not frame the destination
  as a list of learning outcomes.
- **Time and level.** "About 30 minutes. Assumes basic terminal use; no
  prior knowledge of the framework is needed." Keep the assumed level
  genuinely low.

## 1. What the tutorial builds (orientation)

A short paragraph, and ideally a picture or sample of the finished
result, so the learner can see the destination and recognize it when
they arrive. This is Gagné's "inform the learner of the objective" and
it sets expectations that every later step pays off.

Resist listing learning outcomes as a syllabus. Describe the *thing the
tutorial makes*; the learning rides along inside it.

## 2. Prerequisites

The minimum the learner needs in place to succeed, stated so they
discover gaps now rather than halfway through:

- Operating system, runtime, or tool versions.
- Accounts or credentials required.
- The starting state — ideally a clean machine or a provided starter
  project, so the captured output matches what the learner sees.

Keep this list short. A long prerequisites list is often a sign the
scope is too advanced for a tutorial; reconsider before adding to it.

## 3. The steps

The body. Each step follows the *do, then confirm* pattern — Gagné's
"elicit performance" immediately followed by "provide feedback":

```text
N. <Imperative action, starting with a verb.>

   <Optional: one clause of orientation — where to do it, why, if not
   obvious. Then a worked example: the exact command or code.>

   <Expected result: the real output the learner should now see.>
```

Rules for steps:

- **One action per step.** If a step contains an "and then", it is two
  steps.
- **Start with a verb**, imperative form: "Run", "Create", "Open".
  Never the *-ing* form.
- **Around seven primary steps maximum.** Past that, split the tutorial
  or regroup. Cap substeps at about four.
- **Always show expected output.** Paste the real prompt, log line, or
  screenshot captured during the path walk. The absent tutor speaks
  through this confirmation.
- **Maintain a narrative of the expected.** "After a few seconds, the
  server prints `Listening on :8080`." "This command returns several
  hundred lines of logs — that is normal." Prepare the learner for what
  is about to happen.
- **Point out what to notice.** "Notice the prompt now shows
  `(venv)` — that means the environment is active." Close the loop of
  learning the learner is too busy to close alone.
- **Flag likely slips.** "`command not found` usually means step 2 was
  skipped." Errors are teachable moments; pre-empt the common ones.
- **Stay concrete and on one line.** No optional alternatives, no
  alternative flags, no diversions. A tutorial follows a single managed
  path to the conclusion. Options are for how-to guides and reference.
- **Minimize explanation.** One clause of justification at most — "HTTPS
  is used here because it is safer" — then a link to an explanation for
  the curious. Do not stop the action to teach.
- **Use a guided voice.** Keep the tutor present in the prose through
  clear, concrete instructions and immediate confirmation after action.

## 4. What the tutorial built (summary)

Close by describing — and mildly admiring — what the learner has
accomplished: "The result is a working API, deployed and reachable, with
data persisting between requests." This is Gagné's
retention-and-transfer event. Do not merely restate the objectives
verbatim; name the concrete result and the skills exercised.

## 5. Where to go next

Outward links the body kept out of the way:

- Explanation, for the learner now ready to understand *why*.
- Reference, for the full options behind the commands they ran.
- The next tutorial or a related how-to.

Optionally invite repetition — learners reaffirm the *feeling of doing*
by running a successful exercise again. Where the steps are reversible,
say so.

## Pre-publication checklist

- [ ] The destination is stated in one sentence before any step.
- [ ] Prerequisites are listed and genuinely minimal.
- [ ] Every step starts with an imperative verb and does one thing.
- [ ] Every step shows the real, captured expected output.
- [ ] There are no options, forks, or optional alternatives in the body.
- [ ] Explanation is one clause plus a link, never a paragraph.
- [ ] Likely errors are flagged with their early-warning signs.
- [ ] Primary steps number about seven or fewer.
- [ ] The whole path has been executed from the assumed starting state.
- [ ] Where the steps are machine-checkable, the walk is captured as an
      automated test in CI; the *do, then confirm* pattern maps onto
      `When`/`Then` (see `testing-the-path.md`).
- [ ] The summary names the concrete achievement; next-step links exist.
- [ ] Prose uses a guided voice; British/Oxford spelling throughout.
