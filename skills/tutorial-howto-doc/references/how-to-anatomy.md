# How-to guide anatomy

The section-by-section structure for a how-to guide — *directions* that
take an already-competent reader through a real-world goal. Read this
before drafting.

A how-to serves the reader **at work**. It is a recipe, not a lesson: it
assumes basic competence, addresses a specific goal, and gets out of the
way. It does not teach concepts and it does not contrive a sandbox — it
prepares the reader for the real world, including the ways the task can
go wrong.

## Front matter

- **Title.** State exactly what the guide shows, framed as the *user's*
  goal: "How to restore a database from a backup." Not "Restoring a
  database" (might be about *whether* to), not "The `pg_restore`
  command" (that is reference). Good titles serve search engines as well
  as readers.

## 1. What this guide does (problem statement)

One short paragraph naming the goal and when the reader would want it:
"This guide shows you how to restore a PostgreSQL database from a
`pg_dump` backup. Use it when recovering from data loss or cloning
production data into a staging environment."

Frame it from the user's project, not the machine's operations. The tool
is an incidental bit-player; the reader's goal is the subject.

## 2. Before you begin (prerequisites)

What the reader needs in place. Because a how-to addresses the
competent, this assumes familiarity and lists only the specifics:

- Required access, credentials, or permissions.
- Tools and versions.
- State the task depends on (a backup file exists; the target database
  is reachable).

Optionally, redirect readers who are in the wrong place: "If you need to
*create* a backup first, see [How to back up a database]." A how-to may
assume the reader is asking the right question.

## 3. The steps

An ordered sequence toward the goal. Unlike a tutorial, a how-to may
fork, may start and end at reasonable points rather than end to end, and
relies on the reader's judgement to adapt it.

```text
N. <Imperative action, starting with a verb.>

   <Optional: terse orientation or rationale, only if not obvious to a
   competent reader.>

   <Optional: command or code; sample output where it helps the reader
   confirm success.>
```

Rules for steps:

- **Conditional imperatives for the forks.** "If you are restoring to a
  fresh database, run X. If restoring over an existing one, first do Y."
  The real world branches; name the branches that matter.
- **Recommend one safest path.** Where several routes exist, do not make
  the reader choose — pick the surest one and document it. Mention
  alternatives by link, not inline. Eliminating needless choice is a
  service.
- **Assume competence; omit the obvious.** Do not explain what any
  practitioner in the domain already knows. "Turn the tap clockwise to
  stop the water" is not guidance; it is noise.
- **Warn before hazards, not after.** Put a callout *before* any step
  that is irreversible, destructive, long-running, or surprising:
  "Warning: `--clean` drops existing objects before restoring. Confirm
  you are pointed at the right database." A how-to cannot promise
  safety, so it must prepare for danger.
- **One action per step; about eight to ten steps maximum.** If the task
  is larger, split it into sub-tasks with their own short step lists.
- **Provide sample output to confirm success**, especially for commands
  whose effect is not visible. Show what a correct result looks like.
- **Do not teach concepts.** If the reader needs the *why*, link to an
  explanation. If they need exhaustive options, link to reference. Keep
  them on this page and on task.
- **Seek flow.** Order steps the way the work actually flows. Minimize
  context-switching between tools, and avoid making the reader hold a
  thought open across many steps before it resolves into an action.

## 4. See also

The links the body deliberately omitted, gathered at the end so they do
not interrupt the work:

- Explanation, for the background and the *why*.
- Reference, for the full option lists and signatures.
- Related how-tos (the inverse task, the next task, the cleanup task).

## Pre-publication checklist

- [ ] The title names the user's goal, not a command or a "whether".
- [ ] The problem statement says what the goal is and when to pursue it.
- [ ] Prerequisites assume competence and list only the specifics.
- [ ] Steps use conditional imperatives for genuine forks.
- [ ] One safest path is recommended; alternatives are links, not inline
      choices.
- [ ] Nothing teaches a concept the competent reader already holds.
- [ ] Every irreversible or destructive step has a callout *before* it.
- [ ] Commands with invisible effects show sample confirming output.
- [ ] Steps number about ten or fewer; larger tasks are split.
- [ ] The path has been executed start to finish (or demonstrated by an
      SME); where machine-checkable, the recommended path is captured as
      an automated test in CI (see `testing-the-path.md`).
- [ ] "See also" links cover the why (explanation) and the what
      (reference); British/Oxford spelling throughout.
