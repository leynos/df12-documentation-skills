"""Contract coverage for the localization documentation skill.

The module verifies the contracts of the ``localization-docs`` skill: the
ordered four-column glossary schema, the U+2014 empty-set convention, the
seven-stage authoring workflow and the document each drafting stage owns,
relative link and reference-path resolution, and discovery of the skill and its
bundled references in the README and users' guide.

Every positive assertion reads the shipped documents:
``skills/localization-docs/SKILL.md``,
``skills/localization-docs/references/document-contracts.md``,
``skills/localization-docs/references/netsuke-model.md``,
``skills/localization-docs/references/verification.md``, ``README.md`` and
``docs/users-guide.md``. Negative cases mutate a copy of that same text and
assert the specific failure the mutation introduces, so a case fails both when
the shipped guidance regresses and when the checker stops detecting it. The
module only reads these files and never modifies them.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPOSITORY_ROOT / "skills" / "localization-docs"
SKILL_FILE = SKILL_DIR / "SKILL.md"
CONTRACTS_FILE = SKILL_DIR / "references" / "document-contracts.md"
NETSUKE_MODEL_FILE = SKILL_DIR / "references" / "netsuke-model.md"
VERIFICATION_FILE = SKILL_DIR / "references" / "verification.md"
NEW_DOCUMENTS = (
    SKILL_FILE,
    CONTRACTS_FILE,
    NETSUKE_MODEL_FILE,
    VERIFICATION_FILE,
)
README_FILE = REPOSITORY_ROOT / "README.md"
USERS_GUIDE_FILE = REPOSITORY_ROOT / "docs" / "users-guide.md"

GLOSSARY_COLUMNS = ("title", "preferred", "allowed", "forbidden")
EMPTY_SET_CODE_POINT = "U+2014"
EMPTY_SET_RULES = (
    (
        "Use the single U+2014 character as Netsuke's empty-set marker in "
        "`allowed` and `forbidden` cells."
    ),
    (
        "Do not use an empty cell, a hyphen, `N/A`, or that marker for an "
        "unknown preferred translation."
    ),
)
WORKFLOW_STAGES = (
    "Establish scope and evidence",
    "Map the document set",
    "Establish the glossary",
    "Draft the style guide",
    "Draft the translator's guide",
    "Reconcile and verify",
    "Deliver",
)
DRAFTING_STAGE_TERMS = (
    (3, "glossary", ("title", "preferred", "allowed", "forbidden")),
    (4, "style guide", ("voice", "review checklist")),
    (5, "translator's guide", ("registry", "fallback")),
)
REFERENCE_FILES = ("document-contracts.md", "netsuke-model.md", "verification.md")
README_MARKER = "- [`localization-docs`]"
README_LINKS = (
    "(skills/localization-docs/SKILL.md)",
    *(f"(skills/localization-docs/references/{name})" for name in REFERENCE_FILES),
)
GUIDE_HEADING = "Localization documentation"
GUIDE_LINKS = (
    "(../skills/localization-docs/SKILL.md)",
    *(f"(../skills/localization-docs/references/{name})" for name in REFERENCE_FILES),
)

_STAGE_HEADING = re.compile(r"^### (?P<number>\d+)\. (?P<title>.+)$", re.MULTILINE)
_INLINE_LINK = re.compile(r"\[[^\]]*\]\((?P<target>[^)\s]+)(?:\s+\"[^\"]*\")?\)")
_REFERENCE_DEFINITION = re.compile(
    r"^\[[^\]]+\]:\s*(?P<target>\S+)\s*$",
    re.MULTILINE,
)
_ABSOLUTE_PREFIXES = ("http://", "https://", "mailto:", "#")


def _sentences(text: str) -> tuple[str, ...]:
    """Return whitespace-normalised sentences from ``text``."""
    flattened = " ".join(text.split())
    return tuple(
        " ".join(sentence.split()) for sentence in re.split(r"(?<=[.!?])\s+", flattened)
    )


def _empty_set_rules(text: str) -> tuple[str, ...]:
    """Return the sentences that state the empty-set marker and prohibitions."""
    return tuple(
        sentence
        for sentence in _sentences(text)
        if EMPTY_SET_CODE_POINT in sentence or "empty cell" in sentence
    )


def _table_cells(line: str) -> tuple[str, ...]:
    """Return the stripped cells of one Markdown table row."""
    return tuple(cell.strip() for cell in line.strip().strip("|").split("|"))


def _glossary_header(text: str) -> tuple[str, ...]:
    """Return the glossary schema header, rejecting any other column shape."""
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = _table_cells(line)
        if cells == GLOSSARY_COLUMNS:
            return cells
        msg = f"glossary schema header must be {GLOSSARY_COLUMNS}, found {cells}"
        raise ValueError(msg)
    msg = "document contracts must contain a glossary schema table"
    raise ValueError(msg)


def _replace_table_header(text: str, columns: tuple[str, ...]) -> str:
    """Return ``text`` with its first Markdown table header replaced."""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.lstrip().startswith("|"):
            lines[index] = "| " + " | ".join(columns) + " |"
            break
    return "\n".join(lines)


def _workflow_stages(text: str) -> tuple[tuple[int, str, str], ...]:
    """Return each numbered workflow stage as its number, title, and body."""
    headings = list(_STAGE_HEADING.finditer(text))
    stages: list[tuple[int, str, str]] = []
    for index, match in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        stages.append((
            int(match["number"]),
            match["title"].strip(),
            text[match.end() : end],
        ))
    return tuple(stages)


def _workflow_stage_titles(text: str) -> tuple[str, ...]:
    """Return the workflow stage titles in document order."""
    return tuple(title for _, title, _ in _workflow_stages(text))


def _stage_contract_gaps(text: str) -> tuple[int, ...]:
    """Return drafting stages missing their document name or required terms."""
    stages = {
        number: (title, " ".join(body.split()))
        for number, title, body in _workflow_stages(text)
    }
    gaps: list[int] = []
    for number, document, terms in DRAFTING_STAGE_TERMS:
        title, body = stages.get(number, ("", ""))
        if document not in title or any(term not in body for term in terms):
            gaps.append(number)
    return tuple(gaps)


def _rename_workflow_stage(text: str, number: int, title: str) -> str:
    """Return ``text`` with one workflow stage retitled."""
    pattern = re.compile(rf"^### {number}\. .+$", re.MULTILINE)
    return pattern.sub(f"### {number}. {title}", text, count=1)


def _replace_workflow_stage_body(text: str, number: int, body: str) -> str:
    """Return ``text`` with one workflow stage body replaced."""
    pattern = re.compile(
        rf"^### {number}\. [^\n]+$(?P<body>.*?)(?=^### |^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    return pattern.sub(
        lambda match: f"{match.group(0).splitlines()[0]}\n\n{body}\n\n",
        text,
        count=1,
    )


def _remove_workflow_stage(text: str, number: int) -> str:
    """Return ``text`` without the numbered workflow stage."""
    pattern = re.compile(
        rf"^### {number}\..*?(?=^### |^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    return pattern.sub("", text, count=1)


def _link_targets(text: str) -> tuple[str, ...]:
    """Return inline and reference-style link targets in document order."""
    inline = tuple(match["target"] for match in _INLINE_LINK.finditer(text))
    reference = tuple(match["target"] for match in _REFERENCE_DEFINITION.finditer(text))
    return inline + reference


def _broken_links(document: Path, text: str) -> tuple[str, ...]:
    """Return relative link targets that do not resolve beside ``document``."""
    broken: list[str] = []
    for target in _link_targets(text):
        if target.startswith(_ABSOLUTE_PREFIXES):
            continue
        path_part = target.split("#", 1)[0]
        if path_part and not (document.parent / path_part).resolve().exists():
            broken.append(target)
    return tuple(broken)


def _list_item(text: str, marker: str) -> str:
    """Return the Markdown list item that begins with ``marker``."""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith(marker):
            continue
        item = [line]
        for follow in lines[index + 1 :]:
            if not follow.startswith("  "):
                break
            item.append(follow)
        return "\n".join(item)
    return ""


def _section(text: str, heading: str) -> str:
    """Return the body of the level-two section named ``heading``."""
    pattern = re.compile(
        rf"^## {re.escape(heading)}$(?P<body>.*?)(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group("body") if match is not None else ""


def _missing_links(fragment: str, required: tuple[str, ...]) -> tuple[str, ...]:
    """Return the required link targets absent from ``fragment``."""
    return tuple(link for link in required if link not in fragment)


def test_glossary_schema_uses_the_exact_four_columns() -> None:
    """Ensure the glossary contract fixes the ordered four-column schema."""
    text = CONTRACTS_FILE.read_text(encoding="utf-8")

    assert _glossary_header(text) == GLOSSARY_COLUMNS


@pytest.mark.parametrize(
    "columns",
    [
        ("title", "preferred", "allowed"),
        ("preferred", "title", "allowed", "forbidden"),
        ("title", "preferred", "allowed", "forbidden", "status"),
    ],
    ids=["dropped-column", "reordered-columns", "extra-column"],
)
def test_glossary_schema_rejects_other_column_shapes(
    columns: tuple[str, ...],
) -> None:
    """Ensure a dropped, reordered, or extended schema is rejected."""
    text = CONTRACTS_FILE.read_text(encoding="utf-8")
    assert _glossary_header(text) == GLOSSARY_COLUMNS

    mutated = _replace_table_header(text, columns)

    with pytest.raises(ValueError, match="glossary schema header must be"):
        _glossary_header(mutated)


def test_empty_set_convention_is_declared() -> None:
    """Ensure the glossary contract states the empty-set rule verbatim."""
    text = CONTRACTS_FILE.read_text(encoding="utf-8")

    assert _empty_set_rules(text) == EMPTY_SET_RULES


@pytest.mark.parametrize(
    ("original", "replacement"),
    [
        ("U+2014", "U+2013"),
        ("Do not use an empty cell", "Use an empty cell"),
        ("Use the single U+2014 character", "Do not use the single U+2014 character"),
    ],
    ids=["copied-hyphen-code-point", "empty-cell-allowed", "inverted-rule"],
)
def test_empty_set_rule_mutations_are_detected(
    original: str,
    replacement: str,
) -> None:
    """Ensure changing the empty-set rule is detected in the shipped text."""
    text = CONTRACTS_FILE.read_text(encoding="utf-8")
    assert _empty_set_rules(text) == EMPTY_SET_RULES

    mutated = text.replace(original, replacement, 1)

    assert _empty_set_rules(mutated) != EMPTY_SET_RULES


def test_workflow_stages_appear_in_order() -> None:
    """Ensure the seven authoring stages keep their documented order."""
    text = SKILL_FILE.read_text(encoding="utf-8")

    assert _workflow_stage_titles(text) == WORKFLOW_STAGES


def test_workflow_rejects_a_renamed_stage() -> None:
    """Ensure a stage replaced with placeholder text no longer matches."""
    text = SKILL_FILE.read_text(encoding="utf-8")
    assert _workflow_stage_titles(text) == WORKFLOW_STAGES

    renamed = _rename_workflow_stage(text, 3, "Placeholder stage")
    titles = _workflow_stage_titles(renamed)

    assert titles[2] == "Placeholder stage"
    assert titles != WORKFLOW_STAGES


def test_workflow_rejects_swapped_stages() -> None:
    """Ensure swapping two stage titles is detected."""
    text = SKILL_FILE.read_text(encoding="utf-8")
    assert _workflow_stage_titles(text) == WORKFLOW_STAGES

    swapped = _rename_workflow_stage(text, 1, WORKFLOW_STAGES[1])
    swapped = _rename_workflow_stage(swapped, 2, WORKFLOW_STAGES[0])

    assert _workflow_stage_titles(swapped)[:2] == (
        WORKFLOW_STAGES[1],
        WORKFLOW_STAGES[0],
    )


def test_workflow_rejects_an_omitted_stage() -> None:
    """Ensure omitting a stage shortens the workflow."""
    text = SKILL_FILE.read_text(encoding="utf-8")
    assert _workflow_stage_titles(text) == WORKFLOW_STAGES

    removed = _remove_workflow_stage(text, 7)

    assert _workflow_stage_titles(removed) == WORKFLOW_STAGES[:-1]


def test_drafting_stages_name_their_document_and_required_terms() -> None:
    """Ensure each drafting stage names its document and its key rules."""
    text = SKILL_FILE.read_text(encoding="utf-8")

    assert _stage_contract_gaps(text) == ()


def test_drafting_stage_placeholder_heading_is_detected() -> None:
    """Ensure a placeholder heading loses its document ownership."""
    text = SKILL_FILE.read_text(encoding="utf-8")
    assert _stage_contract_gaps(text) == ()

    mutated = _rename_workflow_stage(text, 3, "Placeholder stage")

    assert _stage_contract_gaps(mutated) == (3,)


def test_drafting_stage_placeholder_body_is_detected() -> None:
    """Ensure a filled-in heading cannot hide placeholder body text."""
    text = SKILL_FILE.read_text(encoding="utf-8")
    assert _stage_contract_gaps(text) == ()

    mutated = _replace_workflow_stage_body(text, 4, "Placeholder guidance.")

    assert _stage_contract_gaps(mutated) == (4,)


@pytest.mark.parametrize(
    "document",
    NEW_DOCUMENTS,
    ids=lambda document: document.name,
)
def test_new_documents_have_no_broken_relative_links(document: Path) -> None:
    """Ensure every relative link and reference path resolves."""
    text = document.read_text(encoding="utf-8")

    assert _broken_links(document, text) == ()


def test_link_checker_detects_a_broken_relative_link(tmp_path: Path) -> None:
    """Ensure the link checker rejects a target that does not exist."""
    document = tmp_path / "document.md"
    document.write_text("[missing](absent.md)\n", encoding="utf-8")

    assert _broken_links(document, document.read_text(encoding="utf-8")) == (
        "absent.md",
    )


def test_readme_entry_links_the_skill_and_every_reference() -> None:
    """Ensure the README catalogue entry links the skill and its references."""
    entry = _list_item(README_FILE.read_text(encoding="utf-8"), README_MARKER)

    assert entry.startswith(README_MARKER)
    assert _missing_links(entry, README_LINKS) == ()


@pytest.mark.parametrize("reference", REFERENCE_FILES)
def test_readme_entry_requires_each_reference(reference: str) -> None:
    """Ensure removing one README reference link is detected by name."""
    text = README_FILE.read_text(encoding="utf-8")
    assert _missing_links(_list_item(text, README_MARKER), README_LINKS) == ()

    mutated = text.replace(
        f"skills/localization-docs/references/{reference}",
        "skills/localization-docs/references/reference.md",
    )
    entry = _list_item(mutated, README_MARKER)

    assert _missing_links(entry, README_LINKS) == (
        f"(skills/localization-docs/references/{reference})",
    )


def test_readme_entry_rejects_a_placeholder_skill() -> None:
    """Ensure replacing the README entry with a placeholder is detected."""
    text = README_FILE.read_text(encoding="utf-8")
    assert _missing_links(_list_item(text, README_MARKER), README_LINKS) == ()

    mutated = text.replace(README_MARKER, "- [`placeholder-skill`]", 1)

    assert _missing_links(_list_item(mutated, README_MARKER), README_LINKS) == (
        README_LINKS
    )


def test_users_guide_section_links_the_skill_and_every_reference() -> None:
    """Ensure the users' guide section links the skill and its references."""
    section = _section(USERS_GUIDE_FILE.read_text(encoding="utf-8"), GUIDE_HEADING)

    assert "localization-docs" in section
    assert _missing_links(section, GUIDE_LINKS) == ()


@pytest.mark.parametrize("reference", REFERENCE_FILES)
def test_users_guide_section_requires_each_reference(reference: str) -> None:
    """Ensure removing one users' guide reference link is detected by name."""
    text = USERS_GUIDE_FILE.read_text(encoding="utf-8")
    assert _missing_links(_section(text, GUIDE_HEADING), GUIDE_LINKS) == ()

    mutated = text.replace(
        f"../skills/localization-docs/references/{reference}",
        "references/reference.md",
    )
    section = _section(mutated, GUIDE_HEADING)

    assert _missing_links(section, GUIDE_LINKS) == (
        f"(../skills/localization-docs/references/{reference})",
    )
