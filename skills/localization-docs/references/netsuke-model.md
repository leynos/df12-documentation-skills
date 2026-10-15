# The Netsuke model and adaptation boundary

This skill derives its document roles, glossary schema, and practical translator
workflow from `leynos/netsuke` at commit
`27d7eade290543fe0e92354ef66440788d89ce4d`, inspected on 2026-10-08. The
baseline describes the provenance of this skill, not the current state of any
repository where an agent later invokes it.

## Immutable reference documents

- [Localization style guide][style]: constant voice, content-specific tone,
  register, usage, grammar and mechanics, locale integrity, machine-readable
  boundaries, and a quality checklist.
- [Localization glossary][glossary]: four-column terminology records, source
  vocabulary grouped by domain, localizability notes, and per-locale register
  and terminology sections.
- [Translator guide][translator]: source locale, locale registry and fallback,
  file layout, keys, variables, plurals, locale contribution, bidi, validation,
  testing, and resources.

[style]: https://github.com/leynos/netsuke/blob/27d7eade290543fe0e92354ef66440788d89ce4d/docs/localization-styleguide.md
[glossary]: https://github.com/leynos/netsuke/blob/27d7eade290543fe0e92354ef66440788d89ce4d/docs/localization-glossary.md
[translator]: https://github.com/leynos/netsuke/blob/27d7eade290543fe0e92354ef66440788d89ce4d/docs/translators-guide.md

Read the pinned documents when checking why this skill requires a structure.
Inspect the target repository at its own revision before making statements about
its implementation. Newer source documents may improve the model, but changes to
this baseline should record what changed and why.

## What to carry forward

Carry forward the three-way ownership boundary, opening cross-links, the exact
`title`, `preferred`, `allowed`, `forbidden` schema, semicolon-separated
alternatives, and the U+2014 empty-set convention. Keep localizability
explanations and locale register notes beside the tables rather than extending
their schema.

Also retain the distinction between invariant product voice and contextual tone,
protected literals and translated prose, source and target locales, technical
checks and linguistic review, and completed translations versus scaffolding.

Do not transplant the source term inventory. Netsuke's distinctions between a
target, an action, and a rule illustrate why domain terminology matters; they
are not vocabulary requirements for an unrelated product. Its glossary also
distinguishes the product name `Netsuke`, executable `netsuke`, and Cargo
package `netsuke-build`. Another product needs evidence for its own names and
contexts.

## What to rediscover

### Locale ownership and fallback

The baseline translator guide names `locales/en-US/messages.ftl` as the source,
`src/locale/catalogues.rs` as the registry, Cargo metadata as a checked mirror,
and a separately maintained expected-tag test as an independent oracle. It also
describes different locale precedence before and after configuration loading.
These are Netsuke examples, not a default architecture.

For another repository, identify its actual registry, resources, metadata,
selection phases, and fallback. Do not turn deliberate language-specific rules
into a universal BCP 47 algorithm. Distinguish the language of an input tag from
the regional or script-specific catalogue that the application selects.

### Plural syntax versus runtime behaviour

The baseline guide includes plural examples but explicitly reports a string-only
argument limitation in its localization API. It says this prevents numeric CLDR
category selection as intended. Treat that as a documented limitation to verify
at the relevant revision, not a permanent property of Netsuke or Fluent.

Fluent's [selector documentation][selectors] distinguishes string selectors from
numeric selectors and requires a default variant. Its [variable documentation]
[variables] also explains locale-aware numeric formatting. Therefore, inspect
types and formatting ownership at call sites, then render representative values.
Passing a catalogue parser does not establish runtime plural correctness.

Do not copy the reference guide's category table into a new product. Determine
what the installed engine implements and what values the API can reach, and
compare it with applicable [CLDR plural rules][cldr]. Record version or range
limitations explicitly instead of presenting an obsolete table as universal.

[selectors]: https://projectfluent.org/fluent/guide/selectors.html
[variables]: https://projectfluent.org/fluent/guide/variables.html
[cldr]: https://cldr.unicode.org/index/cldr-spec/plural-rules

### Logical keys and resource syntax

The Netsuke guide describes dotted logical message keys. Before reusing those
examples, inspect how that project's loader or preprocessing layer represents
them to the parser. Do not teach a repository-specific naming convention as
portable Fluent grammar. Preserve application keys during documentation work and
use the target parser to validate examples.

### Directionality is channel-specific

The baseline translator guide distinguishes Fluent's isolation of interpolated
values from Netsuke's rules for the first strong character in terminal output.
It describes U+200F prefixes for certain RTL message values and select variants,
with explicit exceptions in tests.

The baseline glossary's Arabic prose also refers to wrapping embedded Latin
runs. Do not combine that wording into a second blanket rule or double-wrap
values. Let the translator guide own mechanics, check the actual renderer and
tests, and record any unresolved discrepancy. Glossary prose should link to the
verified mechanics instead of redefining them.

Fluent's [Unicode isolation guidance][isolation] provides background, but the
target application's runtime configuration and output channel decide the
required action. Terminal direction policy does not automatically apply to HTML.

[isolation]: https://github.com/projectfluent/fluent.js/wiki/Unicode-Isolation

### Glossary policy is contextual

The source glossary deliberately keeps forbidden alternatives conservative. For
example, a name may be correct for an executable but wrong for a Cargo package.
Do not flatten contextual records into a global banned-word list. Keep reasons,
scope, and linguistic evidence near the normative tables.

Use the [Microsoft localization style guides][microsoft] as one primary
reference corpus for locale register where relevant. Their choices inform a
decision; they do not automatically override approved product terminology or
establish native-speaker review. Record references and any local departures.

[microsoft]: https://learn.microsoft.com/en-us/globalization/reference/microsoft-style-guides

## Worked adaptation procedure

When documenting a repository with different resources or user interfaces:

1. Preserve the three document roles and glossary columns.
2. Replace every Netsuke path, package name, message domain, locale list, and
   command with inspected target evidence. Omit inapplicable examples.
3. Rebuild source terminology from that product's domain and its messages.
4. Add separate register notes for its shipped locale tags, retaining genuine
   regional or script distinctions.
5. Verify the target's argument types, plural engine, fallback, and output
   directionality. Document uncertainty and limitations before offering advice.
6. Walk the contribution and validation path, then cross-check the three
   documents for duplicated or contradictory authority.

The result should be recognizably the same documentation system without falsely
claiming that the products share an implementation.
