# Netsuke baseline and adaptation notes

Inspected reference: `leynos/netsuke` at commit
`27d7eade290543fe0e92354ef66440788d89ce4d` on 8 October 2026. These immutable
links identify the model for this skill; they do not assert that Netsuke or a
target repository still has the same runtime behaviour at a later revision.

## Reference documents

- [Localization style guide][style]: voice/tone separation, content families,
  professional register, usage rules, mechanics, integrity, and machine-output
  boundaries.
- [Localization glossary][glossary]: the four-column terminology schema,
  semicolon alternatives, U+2014 empty sets, source-concept groups,
  localizability notes, and per-locale register and difficult-term mappings.
- [Translator's guide][translators]: locale precedence, registry and fallback,
  resource layout, keys and variables, plurals, contribution workflow,
  right-to-left behaviour, validation, and testing.

Retain those responsibilities and the glossary format. Select relevant source
concepts afresh for every product. Netsuke's distinctions between targets,
actions, and rules illustrate semantic precision; they are not a vocabulary
that belongs in every df12 application.

## Details that must not become cross-repository defaults

### Source locale and integration points

The reference names `en-US` and `locales/<tag>/messages.ftl`. It also names
Netsuke's Rust registry, Cargo metadata, an independent expected-tag test, and
explicit language fallback rules. Re-inspect all of these in the target.
English prose style and the source catalogue's locale are separate decisions.

### Lookup identifiers and Fluent syntax

The translator's guide uses dotted Netsuke lookup keys. Do not reproduce them
as generic, parser-valid Fluent examples without checking the target's loader
or preprocessing. Standard Fluent's identifier grammar is the authority for
unprocessed FTL. The bundled generic examples use hyphenated identifiers.

### Plural syntax versus runtime behaviour

The reference guide describes an argument-stringification limitation and
separates the application's plural-rule data from newer CLDR data. Record that
as a claim made by the reference, not a current diagnosis of another project.
Check argument construction, the exact plural implementation, and exercised
selector branches before describing working numeric pluralization.

A source may repeat a variable across plural branches. Consequently, a rule
about variable names and argument types cannot safely become a universal rule
requiring equal textual occurrence counts across languages. Explain the
actual repository contract and escalate contradictions rather than rewriting
the catalogue to satisfy an invented rule.

### Right-to-left direction and isolation

The reference translator's guide says Fluent isolates interpolated values and
prescribes leading U+200F marks for specific terminal-rendered fragments. Its
glossary contains broader wording about wrapping embedded Latin runs. Do not
combine these into a mandate to wrap every placeholder twice. Verify the
target runtime and renderer, record any documentation conflict, and keep the
mechanical policy in the translator's guide.

### Validation layers

The inspected [localizer implementation][loader] explicitly distinguishes its
build audit's key-parity checks from Fluent parsing at load time. Do not claim
that a compile-time catalogue audit proves syntax correctness without reading
what the audit actually checks. Likewise, a catalogue that differs from the
English source has not thereby passed linguistic review.

### Table formatting

Netsuke's glossary has a file-local MD060 exception with an explanation about
multilingual display width and its formatter. Do not copy that suppression or
relax a target's lint rules pre-emptively. Use the target formatter first;
report a reproducible conflict before proposing the narrowest justified
exception. Formatting must not change exact identifiers or terminology.

## Primary references for verification

Read the relevant sources when a claim depends on them. Record exact versions
or accessed revisions for changeable behaviour; use linguistic sources for
linguistic decisions and implementation evidence for application behaviour.

- [Fluent syntax guide][fluent] and [grammar][grammar] for syntax and terms.
- [Fluent selectors][selectors] for defaults, string matching, numeric matching,
  and cardinal or ordinal selection.
- [Unicode CLDR plural rules][plurals] for language categories, distinct from
  the runtime's implemented data version.
- [Microsoft localization style guides][register] for language-specific
  technical register; accepted repository decisions still need reconciliation.
- [W3C text-size guidance][expansion] for expansion and layout considerations.
- [W3C bidirectional inline-text guidance][bidi] for HTML direction and
  isolation; do not transfer HTML instructions unchanged to terminal output.

[style]: https://github.com/leynos/netsuke/blob/27d7eade290543fe0e92354ef66440788d89ce4d/docs/localization-styleguide.md
[glossary]: https://github.com/leynos/netsuke/blob/27d7eade290543fe0e92354ef66440788d89ce4d/docs/localization-glossary.md
[translators]: https://github.com/leynos/netsuke/blob/27d7eade290543fe0e92354ef66440788d89ce4d/docs/translators-guide.md
[loader]: https://github.com/leynos/netsuke/blob/27d7eade290543fe0e92354ef66440788d89ce4d/src/cli/localization/mod.rs#L73-L86
[fluent]: https://projectfluent.org/fluent/guide/
[grammar]: https://github.com/projectfluent/fluent/blob/main/spec/fluent.ebnf
[selectors]: https://projectfluent.org/fluent/guide/selectors.html
[plurals]: https://cldr.unicode.org/index/cldr-spec/plural-rules
[register]: https://learn.microsoft.com/en-us/globalization/reference/microsoft-style-guides
[expansion]: https://www.w3.org/International/articles/article-text-size
[bidi]: https://www.w3.org/International/articles/inline-bidi-markup/
