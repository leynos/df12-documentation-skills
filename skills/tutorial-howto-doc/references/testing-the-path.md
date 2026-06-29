# Testing the path

A tutorial or how-to is a promise: *follow these steps to get this
result.* A walk-through done once, by hand, verifies that promise
for a single moment. The product then moves on, and the document rots —
quietly, because prose does not fail a build. These are the most
rot-prone pages you own (see the "living document" principle in
`SKILL.md`).

This file covers how to make the *walk the path* phase **durable**: how
to encode a guide's happy path as an automated test that runs in CI, so
the promise is re-checked on every release rather than every time a user
complains. It does **not** teach test frameworks or the BDD process —
defer those mechanics to the project's testing skills and conventions.
The concern here is only where verification meets the *writing* process.

The governing idea is **"docs as tests"** (Manny Silva): a documented
procedure is a test case executed against the real product, and a user's
report of a broken step is simply a test that should have failed in CI
first. Read this once; consult it when scoping a guide whose steps a
machine could check.

## Two levels of verification

Pick the level (or both) that fits the guide. They are complementary,
not alternatives.

### Embedded-snippet testing

Verifies that the code blocks shown *in the prose* actually run and
produce the output the prose claims. The document is the test source, so
the snippet and its expected output cannot drift — they are the same
text the reader sees.

- **Python**: `doctest` for interpreter-style blocks; **Sybil** to run
  fenced code blocks and doctests embedded in Markdown or Sphinx; also
  `byexample`, `mkcodes`.
- **Other ecosystems**: equivalents exist (e.g. Rust runs ```` ```rust ````
  examples as doctests under `cargo test`).

Best for: reference-adjacent tutorials where the value *is* the code, and
the reader copies and pastes it.

### End-to-end path testing

Verifies the *journey* — the ordered commands, the state they build, and
the results — not just isolated snippets. This is where BDD fits, because
a guide's structure already maps onto a scenario.

- **Python**: pytest-bdd (Gherkin on the `pytest` runner).
- **Rust**: rstest-bdd (Gherkin under `cargo test`, reusing `rstest`
  fixtures and typed placeholders).
- **TypeScript / Bun**: `@aboviq/bun-test-cucumber` (Cucumber on the
  `bun test` runner, threading a typed state object between steps).
- **CLI / UI flows**: tool-driven approaches such as Doc Detective that
  drive the product and assert on what it returns.

Best for: multi-step procedures, CLI walk-throughs, and anything where
the order and accumulated state matter.

## The mapping: a tutorial already is Given/When/Then

The reason BDD sits so naturally under a practical guide is that the
guide is *already written* as a behaviour narrative. The structure this
skill mandates maps onto Gherkin with almost no translation:

| Guide element | Gherkin |
| --- | --- |
| starting state / prerequisites | `Given` (shared → `Background`) |
| a step's action ("run X") | `When` |
| expected output ("the output shows Y") | `Then` |
| variant inputs (OS, version, role) | `Scenario Outline` + `Examples` |

The most useful consequence: the **narrative of the expected** — the
confirmations the tutorial anatomy already requires after every step —
*is* the `Then` oracle. The same literal pasted into the prose
("`Listening on :8080`") becomes the string the test asserts. This is
not a test in addition to the tutorial; it gives the tutorial's
confirmations a machine that checks them.

Likewise, the skill's existing rules already produce good steps: one
action per step (one `When`), imperative phrasing, explicit expected
output (a `Then`), and a known starting state (a `Given`/`Background`).
A guide that follows the anatomy is most of the way to a feature file.

## Keep the prose and the test in lockstep

An automated test that has drifted from the document is as misleading as
no test at all — it goes green while the reader is misled. Guard against
drift:

- **Prefer a single source of truth.** With embedded-snippet testing the
  document *is* the source, which is ideal. With path testing, keep the
  `.feature` file and the prose adjacent (e.g. `tutorial.md` beside
  `tutorial.feature`) and treat editing one without the other as an
  incomplete change.
- **Share the expected-output literals.** The string asserted in a
  `Then` step and the output shown in the prose must be the same text.
  When real output is captured during the walk, it serves both.
- **Wire it into CI.** A test that is not run does not prevent rot.
  Record the trigger (per release, per merge) in the handoff, so the
  retest cadence is automatic, not a manual reminder.

## Where this fits in the writing workflow

This is an extension of the skill's existing phases, not a new track:

- **Phase 1 (Scope).** Decide the verification strategy up front:
  snippet-level, path-level, or both, and which ecosystem tool. This is
  a writing decision because it sharpens how steps are phrased — atomic,
  imperative, each with explicit expected output — which the anatomy
  already demands.
- **Phase 2 (Walk the path).** Capture the manual walk *as* the test.
  The real commands become `When` steps; the real output becomes `Then`
  assertions; the clean starting state becomes the
  `Given`/`Background`. One disciplined walk yields both the captured
  output for the prose and the executable scenario.
- **Phase 5 (Handoff).** Commit the feature file and step definitions
  alongside the document, wire them into CI, and note the cadence.

## Scope and boundaries

- This skill decides *that* a guide should be verified and *how
  verification shapes the writing*. It does **not** teach Gherkin syntax,
  step-definition mechanics, fixtures, or the wider BDD collaboration
  process — those belong to the project's dedicated testing and BDD
  skills. Name the tool, map the structure, defer the mechanics.
- Not every guide warrants an automated test. A short conceptual
  walk-through with no reproducible commands may not. Use judgement; the
  payoff scales with how often the steps run and how badly a silent
  break would hurt.

## Credits and prior art

Researched via the Firecrawl MCP. Cited, not reproduced:

- **Docs as Tests** — Manny Silva. <https://www.docsastests.com/>. The
  principle that documentation should verify as well as inform.
- **Sybil** — runs code examples embedded in documentation under pytest.
  <https://sybil.readthedocs.io/>. With Python's standard `doctest`.
- **pytest-bdd** — Gherkin on the pytest runner.
  <https://pytest-bdd.readthedocs.io/>.
- **rstest-bdd** — BDD for Rust, built on `rstest`, under `cargo test`.
  <https://crates.io/crates/rstest-bdd>.
- **@aboviq/bun-test-cucumber** — Cucumber on Bun's test runner.
  <https://www.npmjs.com/package/@aboviq/bun-test-cucumber>.
