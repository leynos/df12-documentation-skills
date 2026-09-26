# Architecture-contract sources and field evidence

This reference explains the additions to `architecture-contract.md` and
`../../terms-of-reference-doc/references/problem-contract.md`. It is a rationale
ledger, not a source of live project status. Observations below were checked on
26 September 2026. Reinspect their cited revisions before applying them to a
current task.

## Framework ideas and local policy

[The Open Group's TOGAF overview][togaf-overview] distinguishes core concepts
from configurable guidance. Its [practitioner competency mapping][togaf-roles]
includes requirements management throughout the development cycle,
stakeholder concerns, gap analysis, implementation governance, and change
management. These motivate the traceability, baseline/target/gap, and feedback
records in these skills. They do not mandate our file layout or ID scheme.

The [TOGAF SOA source book][togaf-soa] describes selecting views around
stakeholder concerns and documenting principle statements, rationale, and
implications. It is older TOGAF 9-era material, used for those enduring
concepts rather than presented as the text of the current standard.
[Business Scenarios][togaf-business] provide the rationale for the optional
multi-actor scenario probe; the df12 probe complements, not replaces, JTBD.

Plateau terminology also appears explicitly in the [ArchiMate implementation
and migration vocabulary][archimate-roles]. Here it means a coherent validated
repository state, not a mandatory modelling notation or enterprise transition
programme. These skills use original, tailored guidance; they neither
reproduce the standard's templates nor claim certification or conformance.

The absolute exclusions for private, test-only, pre-1.0, and unreleased source
APIs are **df12 policy**, not a claim about what TOGAF or semantic versioning
requires. Persisted/wire-format migration remains a separate obligation.

## Rollout basis

[agent-helper-scripts PR #103][execplan-rollout] merged on 17 August 2026.
It introduced the architecture-contract layer: conformance bases, selective
traceability, coherent plateaus, compatibility prohibitions, blocked
deviations, and completion reconciliation. Its reported validation included
an atomic internal migration and a blocked contradictory architecture premise.
That is evidence reported by the PR, not an experiment rerun for this update.

The [current ExecPlan skill][execplan-skill], inspected with blob SHA
`177dc358d4d27ff8e3bc06b84710402e47bf002c`, also requires joint verification
planning and non-vacuity checks. Downstream authors should inspect their
installed version; the link to `main` is a discovery link, not a version pin.
The documentation skills supply inputs to its existing contract rather than
forking that contract or adding another execution approval gate.

## Post-rollout applications

### Cuprum: test the mechanism and the measured path

The [read-size ExecPlan at the inspected revision][cuprum-plan] records an
August measurement update and September revalidation. It distinguishes the
tee workload from capture-only execution, exposes a read-boundary CRLF defect,
and records tests that would lose multi-iteration coverage at a larger read
size while still passing. Its status separates local validation from pending
hosted acceptance. These are recorded findings, not independent reruns here.

The resulting rules are to preserve measurement scope and controls, test
non-vacuity at the actual boundary, treat mechanistic explanations as claims
to verify, and reopen evidence after changes. A performance plateau in this
example is a measured curve feature, not the architectural milestone concept.
Do not weaken a success threshold merely to make a proposed design pass.

### Wireframe: expose false axioms and conflicting compatibility demands

[Wireframe PR #655][wireframe-plan] records a blocked plan after review found
that aborting the supervisor did not establish the claimed shutdown guarantee.
Its plan names prerequisites separately for an implementation milestone and
completion. It also replaces a disconnected model with checks over production
transition logic and records findings that expire after an upstream change.
These are documented planning/review findings, not a completed implementation.

The same plan treats a published pre-1.0 test surface as compatibility-bound.
That historical premise conflicts with the df12 policy above. Preserve the
lesson about discovering the conflict, not the conflicting compatibility rule.
A named consumer or inherited RFC is not a waiver: surface the contradiction
and obtain an explicit upstream resolution instead of generating a wrapper.

These findings motivate real-interface axiom checks, model/implementation
correspondence, scoped blocker edges, evidence expiry, and explicit deviation
handling. A mock that assumes the disputed lifecycle guarantee proves nothing
about it.

### Weave containment: repository delivery is not host convergence

[dev-env-rocky PR #181][weave-containment] distinguishes containment in the
repository from operator rollout and explicitly says that it did not converge
managed hosts. It describes focused verification and separate deployment
acceptance, including limits of checks that encounter no applicable state.
A merge or successful dry run cannot establish actual host reconciliation.

The resulting rules separate implemented, verified, deployed, and
outcome-validated states, require evidence at the claimed boundary, and retain
operator-owned follow-up without silently granting agents rollout authority.

## Lessons located through sync and daily-work retrospectives

Historical sync and daily-work threads supplied discovery leads about stale
blockers, outcome claims, and intentionally paused work. They are not public
status authorities or substitutes for the underlying evidence. The rules
therefore require checking older linked work as well as recent activity,
scoping blocker edges, and distinguishing deliberate pauses from abandonment.
No private thread transcript or current tracker-state claim is published here.

One corroborating repository record is [Dakar PR #3][dakar-compiler], merged
on 17 July 2026, with linked implementation and verification evidence. This
predates the ExecPlan rollout: it informs the later sync/reconciliation lesson,
not a claim that the new skill caused that implementation. Its GitHub record
cannot independently establish a programme tracker's current state.

Treat this ledger as a set of inspected cases, not a controlled evaluation of
agent reliability. The regression scenarios in
`../../../docs/architecture-contract-validation.md` specify future behavioural
checks; writing them does not mean an independent agent has passed them.

[togaf-overview]: https://www.opengroup.org/togaf/new-version
[togaf-roles]: https://help.opengroup.org/hc/en-us/articles/32127544219026-Competency-to-Role-Mapping-TOGAF-Enterprise-Architecture-Practitioner
[togaf-soa]: https://www.opengroup.org/soa/source-book/togaf/p4.htm
[togaf-business]: https://www.opengroup.org/certifications/togaf-portfolio-faq
[archimate-roles]: https://help.opengroup.org/hc/en-us/articles/32127767621906-Competency-to-Role-Mapping-ArchiMate-3-Practitioner
[execplan-rollout]: https://github.com/leynos/agent-helper-scripts/pull/103
[execplan-skill]: https://github.com/leynos/agent-helper-scripts/blob/main/skills/execplans/SKILL.md
[cuprum-plan]: https://github.com/leynos/cuprum/blob/991dee6429ccd415df4cc184e8d558c68d4ccf92/docs/execplans/5-1-1-raise-read-size-to-profiled-plateau.md
[wireframe-plan]: https://github.com/leynos/wireframe/pull/655
[weave-containment]: https://github.com/leynos/dev-env-rocky/pull/181
[dakar-compiler]: https://github.com/leynos/dakar/pull/3
