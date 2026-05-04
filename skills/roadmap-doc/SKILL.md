---
name: roadmap-doc
description: >
  Generate development roadmaps from design documents, RFCs, and ADRs found in
  a repository or provided with the prompt. Use this skill whenever the user
  asks to create, draft, write, or generate a roadmap, execution plan, delivery
  plan, or development plan for a software project — especially when design
  documents, RFCs, or ADRs are available as source material. Also trigger when
  the user asks to turn a design document or set of RFCs into actionable work
  items, or to plan the build order for a system described in technical
  documentation. Trigger even for partial requests such as "plan the next phase"
  or "break this design into tasks" when design documentation is present.
---

# Roadmap document skill

Generate outcome-oriented development roadmaps from design documents, RFCs,
and ADRs. The output is a Markdown roadmap file ready for a repository's
`docs/` directory.

## When to read references

Before generating any roadmap, read
`/mnt/skills/user/roadmap-doc/references/conventions.md` for the full
formatting rules, GIST alignment model, and a worked structural example.
Follow those conventions exactly.

## Workflow

### 1. Gather source material

Identify the design documents, RFCs, and ADRs that define the system. These
are the authoritative inputs. Check these locations:

- Files attached to the prompt.
- `docs/` in the repository root (design documents, ADRs).
- `docs/rfcs/` in the repository root (RFCs).
- Any other paths the user indicates.

Read every document before planning. Do not begin drafting until the full
scope is understood.

### 2. Extract the architectural skeleton

From the source material, identify:

- **Subsystems and boundaries.** What are the major components and where do
  they meet? These inform phase and step boundaries.
- **Dependencies and sequencing constraints.** Which components must exist
  before others can be built? These determine task ordering.
- **Open questions and required decisions.** ADRs to be written, scope
  decisions to be made, alternatives to be resolved. These become early
  tasks that unblock later work.
- **Contracts and interfaces.** IR schemas, API surfaces, CLI contracts,
  plugin boundaries. Settling these early prevents rework.
- **Validation and test requirements.** What must be tested and how? These
  become tasks woven into delivery steps, not deferred to the end.
- **Deferred scope.** Items the design explicitly postpones. These become a
  final phase to keep the v1 boundary disciplined.

### 3. Plan vertical slices

Structure the roadmap around vertical slices of user-facing functionality,
not horizontal layers. Each slice should deliver something usable end-to-end.

Think in terms of domains, not tiers. "Markdown linting with real spans and
safe fixes" is a good slice. "Build the parser layer" is not — it delivers
infrastructure without a usable product surface.

Exceptions: the first phase may be foundational (contracts, build spine, test
scaffolding) when the project has unresolved architectural decisions or no
existing skeleton. Even then, frame the phase as an idea to validate, not as
a layer to build.

### 4. Apply the GIST model

Once the foundational phase is in place, every subsequent phase, step, and
task must align with the GIST (Goals, Ideas, Steps, Tasks) model:

- **Phase = Idea.** State a testable hypothesis. What will the project learn
  or prove by completing this phase? If the phase cannot be wrong, it is not
  an idea — it is a wish.
- **Step = Workstream.** Each step pursues a single delivery objective that
  validates or falsifies some aspect of the phase idea. State what question
  the step answers and what informs subsequent steps. Steps are sequenced so
  each one either unlocks the next or reduces a specific delivery risk.
- **Task = Execution unit.** A concrete, measurable piece of build work with
  clear acceptance criteria. Tasks cite dependencies on prior tasks or steps
  using dotted notation. Tasks cite relevant design document sections or RFCs.
  Tasks should be review-sized: small enough for one realistic pull request
  review and broadly comparable in review burden to other tasks in the same
  roadmap.

### 5. Draft the roadmap

Write the roadmap as a Markdown file following the conventions in
`references/conventions.md`. Use the document structure described there.

While drafting, continuously cross-check against the source material:

- Every RFC, design document section, and ADR should be referenced by at
  least one task. If a source document has no roadmap coverage, either add
  tasks or note that the scope is explicitly deferred.
- Every task dependency must be satisfiable within the roadmap's own
  structure. Do not create circular dependencies.
- Every step must contribute to validating the phase idea. If a step does not
  serve the idea, it belongs in a different phase or is not a real step.

### 6. Review and tighten

After the first draft, review for these failure modes:

- **Layer cake.** Are phases organised by technical tier rather than by
  delivered value? Restructure around user-facing slices.
- **Passive structure.** Are steps just headings that group unrelated tasks?
  Each step must have a concrete objective and a learning opportunity.
- **Vague tasks.** Does a task describe an aspiration ("Improve X") rather
  than a deliverable ("Implement X with Y acceptance criteria")? Rewrite.
- **Mis-sized tasks.** Are tasks not review-sized? Split or merge them.
- **Mechanical step sizing.** Are steps all the same size? Steps do not need to
  be uniform. A run of uniformly sized steps is a warning that the underlying
  tasks may be sized to fit headings rather than realistic review boundaries.
- **Missing dependencies.** Does a task silently assume work from another
  step? Add the dependency citation.
- **Missing citations.** Does a task implement something from a design
  document or RFC without citing it? Add the reference.
- **Orphaned design scope.** Does a design document section or RFC have no
  corresponding roadmap coverage? Add tasks or note the deferral.
- **Scope creep.** Does the roadmap include work the design explicitly
  rejects or defers? Move it to the deferred phase or remove it.
- **Timeframes.** Does the roadmap promise dates or durations? Remove them.
- **Testing theatre.** Does the roadmap contain standalone tasks whose sole
  purpose is to write unit or behavioural tests? These belong inside
  development tasks as implementation expectations, not as separate roadmap
  tasks. Where specific outcome testing is not obvious from the task
  description, move it to the task's `Success:` criterion.
- **Isolated proving step.** Does the roadmap defer model checking, lemma
  proofs, or property-based provers to a standalone step rather than
  weaving them into development tasks? Hardening tasks are appropriate only
  when the proving scope clearly exceeds a single PR.
- **Missing E2E or combinatorial tasks.** Are there flag combinations,
  feature interactions, or integration surfaces that need dedicated
  end-to-end or combinatorial test suites? These warrant their own tasks
  and should be encouraged, not collapsed into implementation tasks or
  deferred.

### 7. Deliver the file

Write the final roadmap to `docs/roadmap.md` (or the path the user
specifies) and present it.

## Key constraints

- British English, Oxford spelling (-ize, -our, -re, -yse).
- No timeframes or date commitments.
- Sentence-case headings.
- 80-column paragraph wrapping, 120-column code wrapping.
- GFM checkboxes for tasks and sub-tasks.
- Dotted numbering for phases, steps, and headline tasks.
- Dependencies cited using dotted notation.
- Design document and RFC sections cited per task where applicable.
- Success criteria stated where not immediately obvious from the task
  description.
- Unit and behavioural tests are part of implementation, not standalone
  tasks; where specific outcome testing is not inferrable, state it as a
  `Success:` criterion on the relevant task.
- E2E suites and combinatorial tests (covering flag and feature
  combinations) are first-class tasks and should be scoped and sized
  accordingly.
- Model checking, provers, and property-based testing belong inside delivery
  tasks; dedicated hardening tasks are appropriate only when the proving
  scope exceeds a single PR.
- Oxford comma where it aids comprehension.
