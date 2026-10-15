# {{PROJECT_NAME}} localization glossary

This glossary owns accepted terminology and locale-specific register. The
[style guide](localization-styleguide.md) owns voice, tone, and writing
mechanics; the [translator's guide](translators-guide.md) owns locale selection,
runtime mechanics, and contribution procedures.

## Schema

Each terminology row describes one concept or context-qualified sense:

- `title`: the canonical source term, also used in target-locale tables.
- `preferred`: the accepted form for that concept in this section's locale.
- `allowed`: acceptable alternatives, separated by semicolons.
- `forbidden`: evidenced unacceptable forms, separated by semicolons.

The U+2014 character in an alternatives cell means the set is empty. Preserve
the four columns and this sentinel. Qualify alternatives whose meaning depends
on context; keep evidence, rationale, and review status outside the rows.

The source locale is `{{SOURCE_LOCALE}}`, and its catalogue is
`{{SOURCE_CATALOGUE}}`. Its source-message terminology is authoritative even
when explanatory documentation uses another English spelling convention.

## Source terminology ({{SOURCE_LOCALE}})

### Product and ecosystem names

{{INVARIANT_NAME_RULES_AND_LITERAL_VERSUS_PROSE_DISTINCTIONS}}

Table 1: Product and ecosystem terminology

| title                   | preferred                  | allowed | forbidden |
| ----------------------- | -------------------------- | ------- | --------- |
| {{SOURCE_PRODUCT_TERM}} | {{PREFERRED_PRODUCT_FORM}} | —       | —         |

### Domain and interface concepts

{{RELEVANT_CONCEPT_GROUPS_AND_SEMANTIC_DISTINCTIONS}}

Table 2: Domain and interface terminology

| title                  | preferred                 | allowed | forbidden |
| ---------------------- | ------------------------- | ------- | --------- |
| {{SOURCE_DOMAIN_TERM}} | {{PREFERRED_DOMAIN_FORM}} | —       | —         |

## Localizability notes

{{TERM_SPECIFIC_HAZARDS_LOAN_WORDS_INFLECTION_AND_IDENTIFIER_NOTES}}

Explain why a term needs care, including overloaded meanings and distinctions
that the product depends on. Do not add speculative forbidden synonyms or
turn scoped terminology decisions into blanket substring bans.

## Locale terminology

Each section records the difficult source-term mappings and register of one
in-scope shipped target locale. Invariant names above remain invariant and
need not be repeated. Record gaps rather than inventing approved translations.

### {{LOCALE_NAME}} (`{{LOCALE_TAG}}`)

{{ACCEPTED_REGISTER_ADDRESS_FORM_SCRIPT_AND_REGIONAL_CONVENTIONS}}

{{LOAN_WORD_POLICY_AND_SPECIFIC_LINGUISTIC_OR_REPOSITORY_EVIDENCE}}

Table 3: {{LOCALE_NAME}} terminology

| title                  | preferred                | allowed | forbidden |
| ---------------------- | ------------------------ | ------- | --------- |
| {{SOURCE_DOMAIN_TERM}} | {{ACCEPTED_TARGET_FORM}} | —       | —         |

{{LOCALE_SPECIFIC_LOCALIZABILITY_NOTES}}

## Open terminology decisions

{{UNRESOLVED_CHOICES_EVIDENCE_NEEDED_AND_REVIEW_ROUTE_OR_NONE}}
