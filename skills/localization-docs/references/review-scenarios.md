# Localization documentation review scenarios

Use these scenarios for desk review or independent fresh-agent evaluation.
Record which method ran, the input revision, changed files, observed outcome,
and outstanding checks. These scenarios specify expected behaviour; their
presence is not evidence that an agent has passed them.

## Existing Fluent developer tool

Give the agent a source catalogue, shipped regional variants, a locale
registry, and distinct help and diagnostic surfaces. Request the complete set.
Expect three cross-linked documents, the exact four-column glossary, evidence
for registry and fallback facts, and separate syntax, rendering, and linguistic
checks. Reject an inventory or command copied from Netsuke without verification.

## Different source locale and application surface

Use an `en-GB` source with several resource files and browser accessibility
text, or a non-Fluent application. Expect the actual source, layout, renderer,
and formats. The shared document ownership and glossary schema still apply.
Reject invented Rust paths, CLI flags, an `en-US` source, or a Fluent migration.

## Regional variants and incomplete linguistic evidence

Include distinct region or script variants, accepted address-form decisions,
and a locale whose terminology has not had linguistic review. Expect separate
locale sections and explicit review gaps outside authoritative tables. Reject
collapsed variants, invented review approval, copied foreign-locale mappings,
or unsupported locales added merely to match Netsuke's inventory.

## Plural structure and misleading checks

Provide a numeric-looking argument passed as a string, a copied plural table,
and a test that checks only key coverage. Include a target selector whose
natural plural branches repeat a variable more often than the source.
Expect a runtime-type limitation, verification of implemented plural data,
and separation of argument identity from textual occurrence counts. Reject a
claim of working numeric selection based on valid syntax or compilation alone.

## Right-to-left output and machine interfaces

Provide a runtime with interpolation isolation and terminal lines beginning
with Latin text, plus machine-readable diagnostic fields. Include conflicting
prose that recommends wrapping every variable. Expect evidence about isolation
and paragraph direction, a recorded conflict, and renderer-specific guidance.
Reject double-wrapped variables, blindly inserted controls, changed JSON keys,
or a universal terminal/HTML direction rule.

## Ambiguous and overloaded terminology

Use a word with a literal command sense and a prose sense, accepted compounds,
and two domain concepts that must stay distinct. Expect scoped records,
localizability notes, conservative forbidden forms, and a code-context question
where meaning remains unresolved. Reject global string replacement, blanket
substring bans, or a guessed new authoritative translation.

## Narrow update and missing implementation

First request one locale's glossary correction in an existing set. Expect a
scoped edit preserving paths and unrelated accepted decisions, with only
necessary link repairs. Then request a new set in a repository with no locale
loader. Expect explicit provisional policy and open implementation questions.
Reject catalogue rewrites, fabricated commands, or implementing a new stack.

## Template and validation honesty

Copy the templates to their default output paths. Expect sibling links to
resolve, the exact glossary header and U+2014 empty-set sentinel, no unresolved
authoring markers in completed sections, and a clear distinction between
observed facts and open questions. With a required tool absent, expect a
blocked or unrun check, not a success claim, a disabled gate, or fabricated
fresh-agent or native-speaker validation.
