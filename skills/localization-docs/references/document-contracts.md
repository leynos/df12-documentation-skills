# Document contracts

Use this anatomy for a new set. When updating an existing set, preserve its
structure where it already fulfils these responsibilities. Every document must
name its companions and the boundary of its own authority.

## Localization style guide

Default path: `docs/localization-styleguide.md`.

### Opening and voice

State the audience, covered product surfaces, and relationship to the glossary
and translator's guide. Distinguish constant product voice from contextual tone.
For operational messages, use clear, calm, capable, respectful language: state
facts, avoid blame, preserve relevant values, and give only supported remedies.

Do not turn product positioning or public-facing copy personality into a rule
for diagnostics. Record a different established product voice explicitly rather
than silently importing Netsuke's entire brand policy.

### Tone by content type

Describe only content families the product has. For each family, identify its
purpose, representative message keys or source locations, expected sentence
shape, tone, and layout constraints. Netsuke's categories provide a starting
point, not a mandatory list:

- Help and about text: neutral explanation with complete sentences or coherent
  noun phrases, following the entry's role.
- Validation errors: specific conditions, values, and valid choices.
- Runtime and I/O errors: condition, relevant context, and supported
  remediation.
- Hints: constructive instructions in the locale's natural instruction form.
- Status and progress: compact, parallel labels without loss of distinctions.
- Rendered pages: descriptive prose appropriate to its presentation context.

Add accessibility text or other surfaces when they exist. Pair examples with
source locations. Label invented examples as illustrative and non-normative.

### Formality and register

Define the base professional distance and link to each locale's glossary notes
for address forms, politeness, honorifics, and gender conventions. Preserve a
consistent, natural register without translating English formality literally. Do
not impose English grammatical constructions on another language. Prefer
established inclusive forms; record genuinely unsettled choices for review.

### Usage rules

Provide concrete do and do-not guidance. Preserve diagnostic meaning, ordering
where significant, technical distinctions, and repeated message-family patterns.
Do not invent advice, guarantees, prompts, warnings, or blame.

Distinguish explanatory prose from frozen tokens. Identify product names,
executables, package names, API symbols, option values, paths, and machine
fields from repository evidence. Link to the glossary for their exact preferred
forms. Do not declare a word universally untranslatable merely because Netsuke
treats one occurrence as an identifier.

### Grammar and mechanics across locales

Cover word order and agreement, sentence shape, text expansion, punctuation,
quotation marks, spacing, numbers, dates, units, capitalization, plurals,
scripts, and transliteration. Preserve case and punctuation inside literal
interfaces. Avoid unsupported numerical claims about translation expansion.

Explain that translators can reposition variables to suit natural grammar while
preserving the application's variable contract. Distinguish preformatted opaque
strings from values the runtime formats by locale. Leave plural-engine details
and supported argument types to the translator's guide.

### Locale integrity and machine-readable output

Link to the source catalogue and supported-tag authority. Preserve meaningful
regional and script distinctions. Delegate bidi mechanics to the translator's
guide rather than duplicating direction-mark rules.

Identify the actual boundary between localized prose and machine-consumed data.
A human-readable field can translate while its field name, schema, enum values,
identifiers, and exit-status meaning remain stable. Do not claim that every JSON
value must remain English. Derive each rule from the interface contract.

### Quality checklist

Include meaning, terminology, register, message-family consistency, literal and
variable preservation, locale-appropriate mechanics, layout, and unsupported
content checks. Link technical gates to the translator's guide. Instruct the
translator to inspect call-site context and raise ambiguity rather than guess.

## Localization glossary

Default path: `docs/localization-glossary.md`.

### Schema

Use exactly these four columns, in this order, in source and locale terminology
tables:

| title       | preferred     | allowed              | forbidden               |
| ----------- | ------------- | -------------------- | ----------------------- |
| Source term | Required form | Accepted alternative | Observed confusing form |

The sample row above explains the fields; it is not a terminology decision.
Replace it with evidence-backed records in a real glossary.

- `title`: the canonical source term or concept key. Use the same key in locale
  tables so reviewers can trace each mapping to its source record.
- `preferred`: the form translators must use in the stated context.
- `allowed`: acceptable alternatives, separated by semicolons. Qualify limited
  contexts, such as executable names versus product prose.
- `forbidden`: observed misspellings, interface-breaking variants, or collisions
  between distinct concepts, separated by semicolons.

Use the single U+2014 character as Netsuke's empty-set marker in `allowed` and
`forbidden` cells. Do not use an empty cell, a hyphen, `N/A`, or that marker for
an unknown preferred translation. Empty means no alternatives or prohibitions;
it does not mean nobody has decided yet.

Keep `title` and `preferred` non-empty. Do not add `locale`, `status`, `notes`,
or `source` columns: headings establish locale scope, and surrounding prose
carries decisions and evidence. Use code spans for literals and the established
term formatting. Escape literal pipes in cells so the table remains parseable.

A prose annotation on a value is not a new term spelling. Keep contextual
qualifiers explicit, especially when a product name and executable differ.
Preserve existing formatter ownership; do not copy lint suppressions from the
reference repository without reproducing the underlying problem.

### Source terminology

State the authoritative source locale and catalogue paths before the tables.
Group terms according to the product's real domain. Netsuke uses product and
ecosystem names, build-model concepts, template language, localization concepts,
and command-line vocabulary; another repository needs its own domain groups.

Record invariant product and interface names once and state the scope of the
invariant. Explain distinctions between adjacent concepts. Keep prohibitions
conservative and justified. A source spelling or naming convention belongs to
this repository, not automatically to all df12 products.

### Localizability notes

Explain difficult terms before presenting locale mappings. Identify polysemy,
false friends, loans, noun/verb differences, domain-specific distinctions,
identifier-versus-prose usage, constrained status labels, and script hazards.
Explain what the term means and what would go wrong with a tempting alternative.

Reference the domain model or code when a distinction carries product semantics.
Do not turn personal stylistic preferences into technical prohibitions.

### Locale terminology

Use a level-three heading containing the language name and exact locale tag,
following Netsuke's shape: ``### German (`de`)``. Keep `pt-BR` and `pt-PT`, for
example, distinct when both ship. The source locale has its source section
rather than a duplicate translation section.

Each shipped non-source locale needs:

1. Register notes: address form, instruction style, politeness or honorifics,
   inclusivity, and any relevant regional or script choices.
2. Loan-word and transliteration notes, with references to shared invariants.
3. Locale-specific hazards and the reason for each important terminology choice.
4. A four-column table mapping the difficult source-term subset, not an
   indiscriminate duplication of invariant product names.
5. Provenance for externally grounded choices and any reviewer decisions.

Use readable prose and source links around the tables. Shared language guidance
may serve related locales, but document meaningful regional differences and
never replace two supported tags with a generic-language section.

When evidence is missing, keep the locale section and record the open decision
outside its normative table. Mark coverage incomplete and identify the needed
linguistic review. Proposed terms must not masquerade as approved `preferred`
values. Planned locales belong in a clearly separate section.

### Maintenance

Explain how maintainers accept a terminology change and reconcile affected
messages and companion documents. Do not rewrite catalogues under a
documentation-only request. Record migration implications and approval needs.

## Translator's guide

Default path: `docs/translators-guide.md`.

Follow Netsuke's numbered section anatomy where it fits. Mark genuinely
inapplicable sections with a reason rather than fabricate an implementation.

### 1. Introduction

Name the localization system, actual source locale, supported surfaces, and
entry points for locale selection. Link the style guide and glossary before
teaching mechanics. Separate multiple initialization stages only where they
actually exist. Derive the shipped-tag inventory from its authoritative source.

### 2. The locale registry

Name the registry and embedding or packaging locations. Identify deliberate
metadata mirrors and independent test oracles, with their drift checks. Explain
how to add a tag without creating a second undocumented registry.

Distinguish locale negotiation from per-message fallback. Document precedence,
tag normalization, aliases, script/region matching, unsupported tags, and
missing-message behaviour only to the extent the implementation supports them.
Preserve meaningful variants and explain ambiguous-language resolution.

### 3. File structure

Show actual source and translation resource paths, split catalogues, generated
files, and comments. Identify which files translators edit and which commands
generate derived files. Do not assume one FTL file per locale or a Rust build.

For Fluent, cover messages, values, attributes, terms, references, placeables,
and comments. Use examples accepted by the target parser. Explain application
preprocessing separately from portable Fluent syntax.

### 4. Message key conventions

Map real message families to purposes and representative keys. Identify
code-facing constants or extraction sources where present. Distinguish a logical
application key from a parsed Fluent identifier and from an attribute reference.
Do not rename keys to make documentation examples resemble another project.

### 5. Variable usage

Explain syntax, required variable names, runtime types, units, provenance, and
formatting ownership. Document representative variables by message family.
Separate opaque paths and identifiers from localizable values. State actual
validation rules for variable names and occurrences; do not infer them by
counting braces in raw text or copying the source's number of plural branches.

### 6. Plural forms

Describe numeric selectors, explicit numeric variants, grammatical categories,
and required default variants. Record the runtime's actual plural engine and
data version where discoverable, not only the latest CLDR documentation.

Check that call sites pass numeric values. Cover representative reachable
integers, zero, fractions, and larger values where the API permits them.
Separate cardinal and ordinal handling when relevant. Document unsupported types
and string-only argument limitations rather than claiming a syntax example
proves runtime support. Do not copy English category sets into other locales.

### 7. Adding or updating a locale

Write an executable workflow: prerequisites, source resource, translation,
terminology review, registration and metadata, fallback updates, validation,
rendering checks, and submission. For an existing locale, explain source changes
and terminology updates without suggesting duplicate registration.

Use real repository commands, working directories, and expected observations. A
copied source catalogue is a scaffold, not a completed translation. Do not
invent snapshots or expected output. Respect build and CI cost limits.

### 8. Right-to-left locales

Distinguish runtime interpolation isolation, paragraph direction, markup, and
terminal rendering. Name relevant Unicode controls by code point and explain
precisely where the repository requires them and which tests cover exceptions.
Test each rendered variant when it can change initial directionality.

Do not insert invisible controls indiscriminately, double-wrap isolated values,
or apply terminal-specific rules to HTML. Link from glossary register notes to
this policy instead of maintaining incompatible copies.

### 9. Quality checklist

Include source coverage, orphaned keys, variable contracts, approved
terminology, register, required plural categories, protected literals,
directionality, rendering, and contribution checks. Distinguish technical
validation from linguistic review; neither substitutes for the other.

### 10. Validation during build or CI

Identify actual validation entry points, diagnostic meanings, and enforcement
level. Do not promise a compile-time audit when the project only has a script or
manual check. State known gaps and proposed improvements separately.

### 11. Testing translations

Name tests for registry resolution, resources, variable interpolation, plurals,
fallback, literal integrity, and rendering where they exist. Give documented
commands and interpretation of results. Identify missing coverage honestly.

### 12. Resources

Link repository authorities, primary localization-system documentation, the
applicable plural data, locale-specific style references, and review procedures.
Keep implementation claims traceable to the inspected revision.
