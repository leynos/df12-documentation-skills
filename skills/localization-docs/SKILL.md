---
name: localization-docs
description: >-
  Create, update, or review a localization style guide, localization glossary
  or lexicon, and translator's guide as a coordinated documentation set.
  Use for df12 localization documentation, modelled on leynos/netsuke,
  including per-locale terminology, register, and repository-specific
  translation workflows. Not a catalogue-translation or runtime-audit skill.
---

# Localization documentation

Produce three coordinated Markdown documents, using Netsuke's separation of
responsibilities and glossary format without copying its implementation policy
into another product.

## Read before drafting

- Read [document contracts](references/document-contracts.md) before outlining
  any of the three documents. It owns their anatomy and glossary schema.
- Read [the Netsuke model](references/netsuke-model.md) when establishing the
  baseline. It records immutable source links and adaptation hazards.
- Read [verification and hand-off](references/verification.md) before editing
  existing documents and again before delivery.

These references ship with this skill. No companion skill is required.

## Outputs and ownership

Use these paths for a new documentation set unless the user specifies others:

- `docs/localization-styleguide.md`: voice, tone, usage, and cross-locale
  writing mechanics.
- `docs/localization-glossary.md`: source terminology, invariants,
  localizability hazards, and per-locale terminology and register decisions.
- `docs/translators-guide.md`: catalogue mechanics, locale selection, fallback,
  contribution workflow, validation, and known runtime limitations.

Discover existing equivalents first. Update them in place rather than creating
competing authorities. Preserve established paths, anchors, and useful content;
propose renames separately. Cross-link all three documents from their opening
paragraphs and the repository's documentation index.

For a request to change only one document, inspect its companions and make only
necessary consistency edits within the authorized scope. Report any remaining
companion change rather than silently expanding the task.

## Governing rules

1. **Inspect before prescribing.** Read repository instructions, current
   documents, catalogues, call sites, tests, and validation commands.
   Distinguish observed behaviour, approved policy, proposals, and unresolved
   questions. Code and tests establish current behaviour, not automatic policy
   approval.
2. **One fact, one owner.** Keep the locale registry and fallback policy in the
   translator's guide, terminology in the glossary, and writing rules in the
   style guide. Other documents link to those owners instead of maintaining
   independent lists.
3. **Format is portable; implementation is not.** Reuse Netsuke's four-column
   terminology schema and document roles. Rediscover paths, source locale,
   message domains, supported tags, runtime types, and tests for each project.
4. **Preserve the interface.** Separate translatable prose from literal
   identifiers, commands, options, paths, message keys, interpolation contracts,
   and machine-readable fields. A style decision must not change an interface.
5. **Do not invent linguistic authority.** Support locale-specific terminology
   and register decisions with existing reviewed translations, relevant primary
   guidance, or a recorded reviewer decision. Label unverified proposals and
   keep them out of normative term tables until approved.
6. **Keep product text separate from promotional copy.** Diagnostics remain
   factual, respectful, and actionable. Do not import humour or marketing tone
   from df12 public-facing copy guidance into errors or operational messages.
7. **Separate prose spelling from catalogue language.** Write documentation in
   British Oxford English unless instructed otherwise. Preserve the actual
   source catalogue's locale, spelling policy, and literals; an `en-US` label
   neither changes the documentation language nor proves every source spelling.

## Workflow

### 1. Establish scope and evidence

Read the user's request and repository guidance. Record the intended readers,
requested outputs, existing documents, and whether localization already ships.
Do not repeat questions the request or repository can answer.

Build a compact evidence map in working notes. For each claim, record the
repository path and symbol or section, inspected revision, document owner, and
any contradiction or missing evidence. Inspect:

- The source catalogue or catalogues, translated resources, representative
  message families, comments, and literal tokens.
- The authoritative locale registry, embedding or packaging configuration,
  locale-resolution code, missing-message fallback, and any independent tests.
- Argument construction and rendering call sites, parser or preprocessing
  layers, plural-rule dependencies, output channels, and directionality policy.
- Existing terminology, domain definitions, documentation indexes, contribution
  instructions, and inexpensive validation targets.

Inventory shipped, planned, and incomplete locales separately. Do not infer
support from a directory alone. For a pre-implementation repository, publish a
clearly labelled proposal and unresolved requirements rather than fictitious
commands, tests, or supported locales.

### 2. Map the document set

Use the document contracts to outline each requested output. Assign every
requirement to its owning document, then add companion links. Reuse evidence
already supplied by the user; proceed with explicit open questions where the
missing information does not block useful work.

Map Netsuke's content-type categories to the target product. Omit irrelevant
build-system concepts, and add real product surfaces such as accessible labels,
web forms, notifications, or library diagnostics where evidence supports them.
Do not invent message IDs to fill a template.

### 3. Establish the glossary

Extract canonical terms from the source catalogue and domain documentation.
Preserve distinctions the product actually makes. Group the source terms,
identify invariant literals, explain difficult concepts, and apply the exact
`title`, `preferred`, `allowed`, `forbidden` schema.

For every shipped non-source locale, inspect or create its register notes and
mapping of the difficult term subset. Preserve regional and script variants.
Record provenance and unresolved choices outside the four-column tables. Do not
mass-generate plausible translations and present them as approved lexicon.

### 4. Draft the style guide

Define constant voice, contextual tone, base register, usage rules, grammar and
mechanics, locale integrity, machine-readable boundaries, and a review
checklist. Use actual message families for examples and explain protected
literals.

Keep locale-specific address forms and term choices in the glossary. Explain how
meaning and professional distance survive translation without imposing English
word order, punctuation, grammatical gender, or plural categories.

### 5. Draft the translator's guide

Document the actual source locale, registry, fallback mechanisms, resource
layout, key conventions, variables and types, plural behaviour, locale-addition
workflow, bidirectional text, checks, and resources. Link every implementation
claim to code, configuration, a test, or explicit approved policy.

Separate valid catalogue syntax from runtime capabilities. Inspect numeric
argument types and actual selector behaviour before claiming plurals work.
Separate inline isolation from paragraph direction and explain the tested policy
for each output channel. Do not copy Netsuke's CLI or build commands verbatim.

### 6. Reconcile and verify

Follow [the verification protocol](references/verification.md). Check both the
three-document contract and the target repository's real workflow. Reconcile
contradictions rather than choosing whichever source is most convenient.

Keep implementation repairs, new translations, linguistic-oracle execution, and
locale registration outside this documentation task unless separately
authorized. Record actionable findings with evidence and validation proposals.
Do not change code or broaden translation-service access to make prose true.

### 7. Deliver

Update the relevant documentation index or README. Report the documents changed,
source revision, checks actually run, checks blocked or not run, unresolved
locale decisions, and any implementation follow-up. Never claim native-speaker
approval, translation completeness, or successful runtime validation without
evidence.

For a requested pull request, follow the repository's commit and PR conventions.
Do not create a recurring audit, invoke paid model services, merge, or publish a
release merely because this documentation skill ran.
