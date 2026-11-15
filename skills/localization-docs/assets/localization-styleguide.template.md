# {{PROJECT_NAME}} localization style guide

This guide owns the voice, tone, and writing mechanics of user-facing text.
The [glossary](localization-glossary.md) owns terminology and locale register;
the [translator's guide](translators-guide.md) owns runtime mechanics,
locale selection, and contribution procedures.

## Voice

The product's voice is clear, calm, capable, and respectful. Messages state
facts, preserve diagnostic meaning, and help the reader act without blame,
filler, humour, marketing language, or unsupported guarantees.

{{PRODUCT_SPECIFIC_VOICE_BOUNDARIES_AND_SOURCE_SUPPORTED_EXAMPLES}}

## Tone by content type

{{ACTUAL_CONTENT_FAMILIES_WITH_TONE_PATTERNS_AND_EXAMPLES}}

Identify the content type before translating. Keep repeated diagnostic and
status patterns parallel; do not translate each message in isolation.

## Formality and register

Use professional plain language and the target locale's natural technical
register. Follow the glossary's accepted address form consistently. Avoid
slang, idioms, unnecessary ceremony, and assumptions about the reader's gender.

{{PRODUCT_SPECIFIC_REGISTER_REQUIREMENTS}}

## Usage rules

Translate explanatory prose naturally while preserving the condition, relevant
value, and any remedy the source actually supplies. Do not invent warnings,
questions, assurances, or alternative product behaviour.

Keep exact identifiers, command syntax, options, paths, message keys, and
contractual interpolation names unchanged. Place interpolation expressions
where the target language needs them without changing their runtime contract.
Follow the glossary for product names and concept distinctions.

{{ACTUAL_FROZEN_LITERALS_AND_IMPORTANT_DOMAIN_DISTINCTIONS}}

## Grammar and mechanics across locales

Use natural target-language agreement, word order, capitalization, punctuation,
and script conventions outside frozen literals. Preserve sentence meaning and
keep diagnostic families consistent. Do not mirror English casing or pronouns
when that would be unnatural or wrong.

{{SENTENCE_SHAPE_AND_CONTENT_SPECIFIC_MECHANICS}}

{{REAL_LAYOUT_LIMITS_AND_TRANSLATION_EXPANSION_PREVIEW}}

{{NUMBER_DATE_UNIT_FORMATTING_OWNERSHIP_AND_PLURAL_POLICY}}

## Locale integrity

The source locale is `{{SOURCE_LOCALE}}`; its catalogue is
`{{SOURCE_CATALOGUE}}`. Preserve the documented message and argument contract.
Keep meaningful regional and script variants distinct. The translator's guide
owns the implemented coverage, selection, fallback, and direction policies.

{{SOURCE_CONTRACT_AND_LOCALE_SPECIFIC_INTEGRITY_REQUIREMENTS}}

## Machine-readable output

Keep machine-readable keys, interface literals, and command syntax stable.
Human-readable prose inside a machine-readable envelope may translate when
the interface contract allows it.

{{ACTUAL_MACHINE_OUTPUT_BOUNDARIES_OR_EXPLICIT_NOT_APPLICABLE}}

## Quality checklist

- [ ] Meaning, relevant values, and source-supported remedies survive.
- [ ] Terminology and address form match the glossary's accepted decisions.
- [ ] Repeated message families remain parallel and appropriately concise.
- [ ] Frozen identifiers and the runtime argument contract remain intact.
- [ ] Punctuation, agreement, and script conventions suit the target locale.
- [ ] Actual layout and direction checks pass in the relevant renderer.
- [ ] No invented content, humour, blame, or marketing copy appears.
- [ ] Ambiguous source text and unreviewed linguistic choices remain explicit.

{{REVIEW_ROUTE_EVIDENCE_LINKS_AND_OPEN_QUESTIONS}}
