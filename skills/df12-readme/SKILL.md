---
name: df12-readme
description: "Generate README files for projects in the df12 Productions house style"
---
# df12 README skill

Use this skill when creating or updating `README.md` files for df12 Productions
projects. This skill produces READMEs that are welcoming, clear, and get
developers to "Hello World" quickly.

**df12 Productions**: https://df12.studio/

## Trigger phrases

- `/readme`, `/df12-readme`
- "write a README", "create README", "update the README"
- "document this project"

## House style principles

### Tone

- **Welcoming and friendly**: The README is often someone's first impression of
  the project. Make them feel welcome.
- **Personality allowed**: A light touch of humour, a relevant pun, or the
  occasional emoji is fine. Do not overdo it—one or two emojis maximum, usually
  in the title or section headers.
- **Short, digestible paragraphs**: Respect the reader's time. No walls of
  text.
- **British English (Oxford variant)**: Use -ize spellings (realize,
  organization), -our spellings (colour, behaviour), -re endings (centre,
  fibre). Keep US spellings only for code identifiers.

### Structure

Follow this structure, adapting as needed for the project:

```markdown
# Project Name

*Brief tagline explaining what this project does (one line).*

[Optional: short paragraph expanding on the tagline, 2-3 sentences max]

______________________________________________________________________

## Why {project-name}?

Explain the problem this solves and why someone would use it. Keep it brief
(3-5 bullet points or a short paragraph).

______________________________________________________________________

## Quick start

### Installation

[Minimal steps to install]

### Basic usage

[Minimal code example that demonstrates the core functionality]

______________________________________________________________________

## Features

[Brief feature list—bullet points work well here]

______________________________________________________________________

## Learn more

- [Users' Guide](docs/users-guide.md) — full documentation
- [Developers' Guide](docs/developers-guide.md) — contributing and development
- [Roadmap](docs/roadmap.md) — planned features and progress

______________________________________________________________________

## Licence

[Licence type] — see [LICENSE](LICENSE) for details.

______________________________________________________________________

## Contributing

[Brief invitation to contribute, link to contribution guidelines]
```

### Key principles

1. **Rapid time to Hello World**: Centre a working code example early. The
   reader should be able to copy-paste and see something work within the first
   scroll.

2. **Link, don't duplicate**: The README is a signpost, not an encyclopaedia.
   Point to `docs/users-guide.md` for full documentation rather than
   reproducing it.

3. **Code examples should work**: Every code block should be correct and
   runnable. Use language identifiers (`bash`, `rust`, `python`, etc.).

4. **Horizontal rules for major sections**: Use `______` (six or more
   underscores) between major sections for visual breathing room.

5. **Sentence case headings**: "Quick start" not "Quick Start".

6. **The 80-column rule**: Wrap prose at 80 columns for readability in
   terminals and diff views.

## Information sources

Before writing, gather information from these project locations:

| Information needed     | Where to find it                                     |
| ---------------------- | ---------------------------------------------------- |
| Project purpose        | `docs/design-doc.md` or principal design document    |
| Features and scope     | Design document, `Cargo.toml`/`pyproject.toml`       |
| Installation           | `docs/users-guide.md`, build configuration           |
| Usage examples         | `docs/users-guide.md`, `examples/` directory         |
| Current status         | `docs/roadmap.md`                                    |
| Licence                | `LICENSE` file                                       |
| Contributing info      | `AGENTS.md`, `docs/developers-guide.md`              |

_Table 1: Information sources for README content._

If you cannot locate the principal design document, ask the user.

## Template with placeholders

```markdown
# {Project Name}

*{One-line description of what it does}.*

{Optional: 2-3 sentence expansion if the tagline needs context}

______________________________________________________________________

## Why {project-name}?

{Brief explanation of the problem and why this project exists.
Use bullet points for multiple value propositions:}

- **{Benefit 1}**: {explanation}
- **{Benefit 2}**: {explanation}
- **{Benefit 3}**: {explanation}

______________________________________________________________________

## Quick start

### Installation

```{language}
{minimal installation command(s)}
```

### Basic usage

```{language}
{minimal working example—aim for < 20 lines}
```

______________________________________________________________________

## Features

- {Feature 1}
- {Feature 2}
- {Feature 3}

______________________________________________________________________

## Learn more

- [Users' Guide](docs/users-guide.md) — full documentation
- [Developers' Guide](docs/developers-guide.md) — contributing and development
- [Roadmap](docs/roadmap.md) — planned features and progress

______________________________________________________________________

## Licence

{Licence type} — see [LICENSE](LICENSE) for details.

______________________________________________________________________

## Contributing

Contributions welcome! Please see [AGENTS.md](AGENTS.md) for guidelines.
```

## Example excerpts from df12 projects

### Good title and tagline

```markdown
# 🫏 git-donkey

*For projects that require a worktree, git-donkey provides support.*
```

```markdown
# rstest-bdd

*Where Rustaceans come for their gourd‑related puns.*
```

### Good TL;DR

```markdown
> **TL;DR**: Behaviour‑Driven Development (BDD), idiomatic to Rust. Keep your
> unit tests and your acceptance tests on the same vine, run everything with
> `cargo test`, and reuse your `rstest` fixtures.
```

### Good "Why" section

```markdown
## Why claude-q?

When working with Claude Code, you often think of tasks while in the
middle of something else:

- "I should refactor that module... but not now"
- "Need to add tests for this... after the current feature"
- "This would be a good time to update the docs"

Instead of interrupting your flow or forgetting these tasks, queue them
with `=qput` and let Claude handle them when the time is right.
```

### Good quick start

```markdown
## Quick start

```shell
# Create a worktree for feature/awesome-stuff from main
git donkey feature/awesome-stuff

# Track a remote branch
git track feature/from-teammate
```
```

## What to avoid

- **Walls of text**: Break up long explanations. If it needs that much detail,
  it belongs in the Users' Guide.
- **Emoji overload**: One or two is friendly; a dozen screams "AI wrote this."
- **Vague descriptions**: "A tool for doing things" tells the reader nothing.
- **Missing code examples**: The Quick Start section must have runnable code.
- **Duplicating documentation**: Link to guides instead of copying them.
- **Broken examples**: Test that code blocks actually work.
- **US spellings**: Use British English except in code identifiers.

## Process

1. **Read the project**: Examine design documents, existing code, and any
   existing documentation.
2. **Identify the core value**: What problem does this solve? Why would someone
   use it?
3. **Find the simplest working example**: What's the shortest path to "it
   works"?
4. **Draft the README**: Follow the structure above.
5. **Verify code examples**: Ensure they compile/run.
6. **Check links**: Ensure all documentation links are valid.
7. **Apply style guide**: British English, 80-column wrap, sentence case
   headings.

## Validation checklist

Before finalising the README, verify:

- [ ] Title clearly identifies the project
- [ ] Tagline explains what it does in one line
- [ ] "Why" section explains the value proposition
- [ ] Quick start includes installation and a working example
- [ ] Code examples are correct and use language identifiers
- [ ] Links to Users' Guide, Developers' Guide, and Roadmap are present
- [ ] Licence section references the LICENSE file
- [ ] Contributing section invites contributions
- [ ] British English spelling throughout (except code identifiers)
- [ ] Paragraphs wrapped at 80 columns
- [ ] Headings in sentence case
- [ ] Emoji usage is minimal (0-2 total)
