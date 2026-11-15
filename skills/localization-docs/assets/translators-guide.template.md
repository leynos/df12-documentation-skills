# {{PROJECT_NAME}} translator's guide

This guide explains how to update translations and add supported locales. Read
the [style guide](localization-styleguide.md) for voice and writing mechanics,
and the [glossary](localization-glossary.md) for terminology and locale
register.

## 1. Introduction

{{LOCALIZATION_STACK_SOURCE_LOCALE_AND_ACTUAL_USER_SURFACES}}

{{LOCALE_REQUEST_PRECEDENCE_WITH_CODE_OR_TEST_EVIDENCE}}

Describe startup and runtime precedence separately when the application uses
more than one resolution stage.

## 2. The locale registry

{{SHIPPED_TAGS_EXPERIMENTAL_LOCALES_AND_AUTHORITATIVE_REGISTRY}}

{{MANIFEST_PACKAGING_GENERATED_RESOURCE_AND_INDEPENDENT_TEST_INTEGRATION}}

### Fallback policy

{{EXACT_TAG_SCRIPT_REGION_UNSUPPORTED_TAG_AND_MISSING_MESSAGE_BEHAVIOUR}}

Distinguish catalogue negotiation from missing-message fallback. Document
regional and script variants explicitly rather than inferring language-only
fallbacks.

## 3. File structure

{{ACTUAL_CATALOGUE_LAYOUT_RESOURCE_DOMAINS_AND_FILE_OWNERSHIP}}

{{ACTUAL_FORMAT_AND_COMMENT_CONVENTIONS}}

For a Fluent target, the following is a simplified syntax example, not an
existing application key. Replace it with a verified example where possible;
remove it when the target uses another format.

```ftl
# Context: report an operation failure and preserve the affected path.
operation-failed = Failed to process { $path }: { $details }
```

## 4. Message key conventions

{{ACTUAL_IDENTIFIER_PATTERNS_NAMESPACES_ATTRIBUTES_TERMS_AND_PREPROCESSING}}

Explain the distinction between application lookup identifiers and stored
resource syntax when the loader transforms them. Identify generated files
that translators must not edit directly.

## 5. Variable usage

{{VARIABLE_MEANINGS_RUNTIME_TYPES_FORMATTING_OWNERSHIP_AND_EXAMPLES}}

Preserve the runtime argument contract and frozen literals. Move expressions
with the target language's grammar. Document any repository restriction on
locale-local terms, helper messages, attributes, or additional selectors.

## 6. Plural forms and selectors

{{IMPLEMENTED_PLURAL_DATA_ARGUMENT_TYPES_AND_REQUIRED_SELECTOR_BEHAVIOUR}}

This generic Fluent example requires a numeric `$count`. It does not prove the
application currently supplies one. Replace or remove it to match the target.

```ftl
files-processed = { $count ->
    [one] Processed { $count } file.
   *[other] Processed { $count } files.
}
```

{{VERIFIED_TARGET_LOCALE_EXAMPLES_EXACT_MATCHES_AND_DEFAULT_VARIANTS}}

### Current limitations

{{OBSERVED_UNSUPPORTED_OR_UNTESTED_BEHAVIOUR_WITH_EVIDENCE_OR_NONE}}

## 7. Updating and adding locales

### Update an existing locale

{{SOURCE_DIFF_CONTEXT_TRANSLATION_GLOSSARY_REVIEW_AND_VALIDATION_STEPS}}

### Add a new locale

{{VERIFIED_CATALOGUE_REGISTRY_MANIFEST_PACKAGING_FALLBACK_AND_TEST_STEPS}}

A copied source catalogue is a scaffold, not a finished translation. Distinguish
required registration from planned support and retain independent test oracles
where the repository deliberately uses them.

## 8. Right-to-left locales

{{ACTUAL_RENDERER_ISOLATION_PARAGRAPH_DIRECTION_AND_PREVIEW_REQUIREMENTS}}

Document marks or direction attributes only where the actual renderer needs
them. Do not double-wrap interpolations or put controls into machine-readable
identifiers. Include mixed-script, leading-literal, and selector-variant cases
when relevant.

## 9. Quality checklist

- [ ] Syntax parses through the actual loader without junk or recovery errors.
- [ ] Keys, attributes, references, and arguments meet the repository contract.
- [ ] Terminology, register, and meaning pass the required linguistic review.
- [ ] Supported locale negotiation and missing-message fallback work.
- [ ] Relevant selector branches execute with the actual runtime types.
- [ ] Frozen literals, command syntax, and machine interfaces remain intact.
- [ ] Rendered layout, direction, and accessibility checks cover the surfaces.
- [ ] Registry, packaging, and independent expected-locale data agree.
- [ ] Unresolved review and unsupported behaviour remain visible.

## 10. Build-time and CI validation

{{ACTUAL_CHECKS_WHEN_THEY_RUN_FAILURE_BEHAVIOUR_AND_COVERAGE_GAPS}}

Do not describe key coverage as syntax validation, or syntax validity as
linguistic approval.

## 11. Testing translations

{{VERIFIED_COMMANDS_PREREQUISITES_EXPECTED_OBSERVATIONS_AND_REVIEW_ROUTE}}

Separate checks actually run from commands documented for a future contributor.
Keep structural, runtime, rendered, and linguistic evidence distinct.

## 12. Resources

{{REPOSITORY_EVIDENCE_PRIMARY_FORMAT_AND_LOCALE_REFERENCES}}
