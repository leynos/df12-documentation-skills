"""Contract coverage for the localization documentation skill."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPOSITORY_ROOT / "skills" / "localization-docs"
SKILL_FILE = SKILL_DIR / "SKILL.md"
CONTRACTS_FILE = SKILL_DIR / "references" / "document-contracts.md"
NEW_DOCUMENTS = (
    SKILL_FILE,
    CONTRACTS_FILE,
    SKILL_DIR / "references" / "netsuke-model.md",
    SKILL_DIR / "references" / "verification.md",
)
README_FILE = REPOSITORY_ROOT / "README.md"
USERS_GUIDE_FILE = REPOSITORY_ROOT / "docs" / "users-guide.md"

GLOSSARY_COLUMNS = ("title", "preferred", "allowed", "forbidden")
EMPTY_SET_CODE_POINT = "U+2014"
EMPTY_SET_USE = f"Use the single {EMPTY_SET_CODE_POINT} character"
EMPTY_SET_INVERSION = "Do not use the single U+2014 character"
EMPTY_SET_PROHIBITIONS = ("Do not use an empty cell", "`N/A`")
WORKFLOW_STAGES = (
    "Establish scope and evidence",
    "Map the document set",
    "Establish the glossary",
    "Draft the style guide",
    "Draft the translator's guide",
    "Reconcile and verify",
    "Deliver",
)
DRAFTING_STAGE_OUTPUTS = (
    (3, "glossary"),
    (4, "style guide"),
    (5, "translator's guide"),
)
REFERENCE_FILES = ("document-contracts.md", "netsuke-model.md", "verification.md")
MINIMUM_STAGE_WORDS = 15
PLACEHOLDER_MARKERS = ("placeholder", "todo", "tbd")
README_REQUIREMENTS = (
    "skills/localization-docs/SKILL.md",
    "localization-docs",
    *REFERENCE_FILES,
)
USERS_GUIDE_REQUIREMENTS = ("localization-docs", *REFERENCE_FILES)

_STAGE_HEADING = re.compile(r"^### (?P<number>\d+)\. (?P<title>.+)$", re.MULTILINE)
_INLINE_LINK = re.compile(r"\[[^\]]*\]\((?P<target>[^)\s]+)(?:\s+\"[^\"]*\")?\)")
_REFERENCE_DEFINITION = re.compile(
    r"^\[[^\]]+\]:\s*(?P<target>\S+)\s*$",
    re.MULTILINE,
)
_ABSOLUTE_PREFIXES = ("http://", "https://", "mailto:", "#")


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


def _declares_empty_set_convention(text: str) -> bool:
    """Return whether ``text`` affirms the glossary empty-set convention."""
    return (
        EMPTY_SET_USE in text
        and EMPTY_SET_INVERSION not in text
        and all(marker in text for marker in EMPTY_SET_PROHIBITIONS)
    )


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


def _stage_guidance_is_substantive(body: str) -> bool:
    """Return whether a stage body contains real guidance, not a placeholder."""
    lowered = body.lower()
    return len(body.split()) >= MINIMUM_STAGE_WORDS and not any(
        marker in lowered for marker in PLACEHOLDER_MARKERS
    )


def _missing_stage_outputs(text: str) -> tuple[int, ...]:
    """Return drafting stages that omit their document or substantive guidance."""
    stages = {number: (title, body) for number, title, body in _workflow_stages(text)}
    gaps: list[int] = []
    for number, document in DRAFTING_STAGE_OUTPUTS:
        title, body = stages.get(number, ("", ""))
        if document not in title or not _stage_guidance_is_substantive(body):
            gaps.append(number)
    return tuple(gaps)


def _rename_workflow_stage(text: str, number: int, title: str) -> str:
    """Return ``text`` with one workflow stage retitled."""
    pattern = re.compile(rf"^### {number}\. .+$", re.MULTILINE)
    return pattern.sub(f"### {number}. {title}", text, count=1)


def _replace_workflow_stage_body(text: str, number: int, body: str) -> str:
    """Return ``text`` with one workflow stage body replaced."""
    pattern = re.compile(
        rf"^### {number}\. .+$(?P<body>.*?)(?=^### |^## |\Z)",
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


def _discovery_gaps(readme: str, guide: str) -> tuple[str, ...]:
    """Return discovery entries missing from the README or users' guide."""
    gaps = [f"README: {item}" for item in README_REQUIREMENTS if item not in readme]
    gaps.extend(
        f"users guide: {item}" for item in USERS_GUIDE_REQUIREMENTS if item not in guide
    )
    return tuple(gaps)


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
    text = _replace_table_header(CONTRACTS_FILE.read_text(encoding="utf-8"), columns)

    with pytest.raises(ValueError, match="glossary schema header must be"):
        _glossary_header(text)


def test_empty_set_convention_is_declared() -> None:
    """Ensure the glossary owner documents the U+2014 empty-set convention."""
    text = CONTRACTS_FILE.read_text(encoding="utf-8")

    assert _declares_empty_set_convention(text)


def test_empty_set_convention_rejects_an_inverted_rule() -> None:
    """Ensure negating the empty-set rule is detected despite its strings."""
    text = CONTRACTS_FILE.read_text(encoding="utf-8").replace(
        EMPTY_SET_USE,
        EMPTY_SET_INVERSION,
    )

    assert EMPTY_SET_CODE_POINT in text
    assert not _declares_empty_set_convention(text)


@pytest.mark.parametrize(
    ("original", "replacement"),
    [
        ("U+2014", "U+2013"),
        ("Do not use an empty cell", "Use an empty cell"),
    ],
    ids=["copied-hyphen-code-point", "empty-cell-allowed"],
)
def test_empty_set_convention_rejects_other_markers(
    original: str,
    replacement: str,
) -> None:
    """Ensure replacing the empty-set marker or rule is detected."""
    text = CONTRACTS_FILE.read_text(encoding="utf-8").replace(original, replacement)

    assert not _declares_empty_set_convention(text)


def test_workflow_stages_appear_in_order() -> None:
    """Ensure the seven authoring stages keep their documented order."""
    text = SKILL_FILE.read_text(encoding="utf-8")

    assert _workflow_stage_titles(text) == WORKFLOW_STAGES


def test_workflow_rejects_a_renamed_stage() -> None:
    """Ensure a stage replaced with placeholder text no longer matches."""
    text = SKILL_FILE.read_text(encoding="utf-8")

    renamed = _rename_workflow_stage(text, 3, "Placeholder stage")

    assert _workflow_stage_titles(renamed) != WORKFLOW_STAGES


def test_workflow_rejects_swapped_stages() -> None:
    """Ensure swapping two stage titles is detected."""
    text = SKILL_FILE.read_text(encoding="utf-8")

    swapped = _rename_workflow_stage(text, 1, WORKFLOW_STAGES[1])
    swapped = _rename_workflow_stage(swapped, 2, WORKFLOW_STAGES[0])

    assert _workflow_stage_titles(swapped) != WORKFLOW_STAGES


def test_workflow_rejects_an_omitted_stage() -> None:
    """Ensure omitting a stage shortens the workflow."""
    text = SKILL_FILE.read_text(encoding="utf-8")

    removed = _remove_workflow_stage(text, 7)

    assert len(_workflow_stages(removed)) == len(WORKFLOW_STAGES) - 1
    assert _workflow_stage_titles(removed) != WORKFLOW_STAGES


def test_drafting_stages_name_their_output_documents() -> None:
    """Ensure each drafting stage names the document it owns."""
    text = SKILL_FILE.read_text(encoding="utf-8")

    assert _missing_stage_outputs(text) == ()


def test_drafting_stage_output_requirement_is_enforced() -> None:
    """Ensure a placeholder drafting stage loses its document ownership."""
    text = SKILL_FILE.read_text(encoding="utf-8")
    mutated = _rename_workflow_stage(text, 3, "Placeholder stage")

    assert _missing_stage_outputs(mutated) != ()


def test_drafting_stage_body_must_be_substantive() -> None:
    """Ensure a filled-in heading cannot hide placeholder body text."""
    text = SKILL_FILE.read_text(encoding="utf-8")
    mutated = _replace_workflow_stage_body(text, 4, "Placeholder guidance.")

    assert _missing_stage_outputs(mutated) != ()


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


def test_discovery_documentation_names_the_skill_and_references() -> None:
    """Ensure the README and users' guide advertise the skill and references."""
    gaps = _discovery_gaps(
        README_FILE.read_text(encoding="utf-8"),
        USERS_GUIDE_FILE.read_text(encoding="utf-8"),
    )

    assert gaps == ()


@pytest.mark.parametrize("placeholder", ["placeholder-skill", "skill-docs"])
def test_discovery_check_rejects_placeholder_skill_names(placeholder: str) -> None:
    """Ensure replacing the skill name with placeholder text is detected."""
    readme = README_FILE.read_text(encoding="utf-8").replace(
        "localization-docs",
        placeholder,
    )
    guide = USERS_GUIDE_FILE.read_text(encoding="utf-8").replace(
        "localization-docs",
        placeholder,
    )

    assert _discovery_gaps(readme, guide) != ()


@pytest.mark.parametrize("reference", REFERENCE_FILES)
def test_discovery_check_requires_each_reference_in_the_users_guide(
    reference: str,
) -> None:
    """Ensure the users' guide names every bundled reference file."""
    readme = README_FILE.read_text(encoding="utf-8")
    guide = USERS_GUIDE_FILE.read_text(encoding="utf-8").replace(
        reference,
        "reference.md",
    )

    assert _discovery_gaps(readme, guide) != ()


@pytest.mark.parametrize("reference", REFERENCE_FILES)
def test_discovery_check_requires_each_reference_in_the_readme(
    reference: str,
) -> None:
    """Ensure the README catalogue names every bundled reference file."""
    readme = README_FILE.read_text(encoding="utf-8").replace(
        reference,
        "reference.md",
    )
    guide = USERS_GUIDE_FILE.read_text(encoding="utf-8")

    assert _discovery_gaps(readme, guide) != ()
