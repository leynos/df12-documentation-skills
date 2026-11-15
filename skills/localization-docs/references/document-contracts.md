# Localization document contracts

The three documents form one maintained interface for authors, translators,
reviewers, and localization auditors. Keep their boundaries visible. The
[templates](../assets/) are drafting aids,
not substitute evidence for the target repository.

## Style guide

Default path: `docs/localization-styleguide.md`.

Retain Netsuke's useful section anatomy:

1. Introduction and links to the glossary and translator's guide.
2. Voice: constant product personality and prohibited deviations.
3. Tone by content type: the target's real message families and surfaces.
4. Formality and register: cross-locale principles, with locale choices owned
   by the glossary.
5. Usage rules: actionable do/don't guidance and frozen interfaces.
6. Grammar and mechanics across locales: agreement, sentence shape,
   punctuation, capitalization, text expansion, formatting, plurals, scripts.
7. Locale integrity: source-message contract and distinct regional or script
   variants, with implementation details delegated to the translator's guide.
8. Machine-readable output: exact interface invariants versus human prose
   inside envelopes.
9. Quality checklist and ambiguity escalation.

Use concrete source-supported examples. A useful diagnostic preserves the
condition, the relevant value, and any remedy supplied by the source; it does
not add reassurance, blame, urgency, or a promise. UI labels, accessibility
text, browser content, and CLI help need distinct treatment when they exist.
Do not add Netsuke CLI families to a product that does not have them.

Professional distance and inclusivity carry across locales, but their grammar
does not translate mechanically. Avoid assumptions about the reader's gender;
record natural, established locale conventions rather than inventing forms.

Document real layout constraints and preview methods. Text expansion depends
on language, content, and rendering. Do not prescribe a universal percentage,
truncate meaning, or count code points as terminal display width.

## Glossary

Default path: `docs/localization-glossary.md`.

### Stable schema

Every terminology table has exactly this header:

```text
| title | preferred | allowed | forbidden |
```

A row represents one concept or context-qualified sense, not an unqualified
word substitution. `title` names the source concept in source and target
sections. `preferred` supplies the accepted form for that sense; `allowed` and
`forbidden` contain semicolon-separated alternatives. Use U+2014, the em-dash
character, for an empty set, not a hyphen, blank cell, `N/A`, or the word
`none`. Preserve this sentinel in the copied template.

Use code spans for exact forms, particularly identifiers, as Netsuke does.
Put explanatory qualifiers after forms where their scope matters. Do not
translate qualifiers into executable matching rules or treat the tables as a
naive find-and-replace dictionary. Escape literal pipes in table cells using
the repository's Markdown conventions; explain ambiguities involving literal
semicolons in surrounding prose rather than inventing a new delimiter.

Do not add language, confidence, reviewer, status, source, or notes columns.
Locale headings and adjacent prose carry those details. Do not create a
parallel YAML or JSON lexicon unless explicitly requested; any separately
requested export must identify its derivation and avoid becoming a competing
source of truth.

### Required anatomy

1. Introduction, ownership, and links to both companion documents.
2. Schema, delimiter and empty-set conventions, and actual source locale.
3. Source terminology grouped by relevant concepts, including invariant names
   and interface literals.
4. Localizability notes explaining semantic collisions, overloaded words,
   noun/verb differences, loan words, and script hazards.
5. Locale terminology with one section per in-scope shipped target tag.
6. Clearly separated unresolved terminology or register decisions, when any.

Do not repeat the source locale as a target section without a concrete need.
For a full-set task, account for every shipped locale, including an explicit
review gap where no trustworthy mapping exists. Do not fill gaps with invented
approval or silently treat an experimental catalogue as a supported locale.

A locale section should identify its language or script variant, address form,
professional register, relevant inflection conventions, loan words, and
preferred mappings for difficult concepts. Cite the specific linguistic
reference or accepted repository decision. A related locale is supporting
evidence, not permission to collapse regional or script distinctions.

Keep forbidden forms conservative: observed misspellings, broken interface
spellings, and demonstrated concept collisions. Existing translations are
usage evidence, not automatic proof of correctness. Preserve accepted decisions
unless the task authorizes revision, and make unresolved conflicts explicit.

## Translator's guide

Default path: `docs/translators-guide.md`.

Use the following anatomy, tailoring only inapplicable sections:

1. Introduction: source locale, user surfaces, locale-request precedence.
2. Locale registry and fallback policy, including integration points.
3. File structure, resource ownership, and actual catalogue format.
4. Message-key conventions and any lookup-to-storage transformation.
5. Variable meanings, runtime types, interpolation, and formatting.
6. Plural forms, other selectors, examples, and current limitations.
7. Updating an existing locale and adding a new locale as separate procedures.
8. Right-to-left rendering, isolation, direction, and frozen-token handling.
9. Quality checklist covering syntax, semantics, layout, and linguistic review.
10. Build-time or CI validation: actual checks, failure behaviour, and gaps.
11. Testing and preview: verified commands and expected observations.
12. Resources and escalation or contribution route.

### Runtime facts

Differentiate how a locale request is chosen, how it resolves to a supported
catalogue, and how a missing message falls back. Record startup versus runtime
behaviour when they differ. The registry, manifest, generated resources,
packaging, test fixtures, and independent expected-locale oracle may all need
updates; enumerate only integration points found in the target repository.

Treat locale variants as distinct until the target's explicit negotiation
policy says otherwise. Never infer that a language-only truncation of a BCP 47
tag produces the right regional or script variant. Verify malformed and
unsupported tags, missing resources, and missing-message behaviour separately.

### Fluent-specific contract

Fluent is the reference format, not a requirement to migrate a different stack.
Document another format's equivalent contracts when the target does not use
Fluent. For Fluent targets:

- Show valid syntax for messages, attributes, terms, comments, variables, and
  selectors used in the target. Clearly label simplified examples. Describe
  repository preprocessing and use the real loader when checking such files.
- Preserve the application's externally addressed messages and attributes,
  required references, variable names and types, and frozen literals. Explain
  whether the target permits locale-local terms or additional helper messages.
  Do not assert that all Fluent resources universally require identical keys.
- Preserve the argument contract, not English placeable position or an equal
  count of textual occurrences. Locale-specific selectors may repeat a
  variable or require different branches. Identify stricter project checks
  and report any conflict without silently changing either contract.
- Numeric values select exact-number or plural-category branches; strings
  select string keys. Verify the runtime passes numbers where plural rules
  require them. Every select expression needs a default variant.
- Distinguish CLDR's current rules from the data implemented by the runtime.
  Verify cardinal versus ordinal rules, integers, fractions, relevant large
  values, and explicit numeric matches. Do not reproduce Netsuke's plural
  category table as a timeless language reference.
- Do not add unsupported formatting functions or change variable types in a
  translation. Explain which layer formats numbers, dates, units, and paths.
- Preserve translator context and explain comment conventions. Reject parser
  junk or recovery artefacts even when a parser returns a resource object.

### Rendering and review

Separate isolation around interpolated values from the direction of a whole
line or paragraph. Verify terminal behaviour, HTML directionality, framework
configuration, or other actual rendering context. Do not assume that manually
wrapping every variable fixes bidirectional text. Never alter machine-readable
identifiers to repair their presentation.

Give the commands needed to reproduce preview and validation locally, with
prerequisites and expected output. Distinguish parse success, catalogue
coverage, negotiation, interpolation, exercised plural branches, visual layout,
and linguistic acceptance. List unsupported or untested paths honestly.

## Applying templates

Copy the requested template into its output location before resolving links.
All three templates link to their eventual sibling filenames, not to filenames
inside the skill package. Adjust links when the target uses another layout.

Replace `{{UPPER_SNAKE_CASE}}` markers with verified content. Remove authoring
instructions and unused example rows. When a fact remains unknown, replace its
marker with a specific open question and verification step, not a guessed
answer. Preserve existing document anchors and accepted decisions during
updates instead of replacing whole files with freshly filled templates.
