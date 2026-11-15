"""Contract: architecture-contract guidance ships with its skill.

The terms-of-reference and technical-design skills hand their downstream
contract through named reference files. A reference that is deleted, renamed,
or never named by its own skill silently removes that guidance from an
installing agent, so these checks assert that each contract reference is
shipped inside its skill and mentioned somewhere in that skill's Markdown.

They assert packaging reachability only. Whether an agent obeys the semantic
policy in those files is the subject of the fresh-agent scenarios in
``docs/architecture-contract-validation.md``, not of a phrase assertion here.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
CONTRACT_REFERENCES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("tech-design-doc", ("architecture-contract.md", "field-evidence.md")),
    ("terms-of-reference-doc", ("problem-contract.md",)),
)


def _validate_contract_references(skills_root: Path) -> list[str]:
    """Return one problem per contract reference that is missing or unnamed."""
    problems: list[str] = []
    for skill, names in CONTRACT_REFERENCES:
        skill_root = skills_root / skill
        texts = [
            path.read_text(encoding="utf-8")
            for path in sorted(skill_root.rglob("*.md"))
        ]
        for name in names:
            reference = skill_root / "references" / name
            if not reference.is_file():
                problems.append(f"{reference.relative_to(skills_root)} is not shipped")
            elif not any(name in text for text in texts):
                problems.append(f"{name} is not named inside skills/{skill}")
    return problems


def test_contract_references_are_shipped_and_named() -> None:
    """Every architecture-contract reference ships and is named by its skill."""
    assert _validate_contract_references(SKILLS_ROOT) == []


def _materialise_contract_skills(skills_root: Path) -> None:
    """Write a complete, valid fixture tree for every contract skill."""
    for skill, names in CONTRACT_REFERENCES:
        skill_root = skills_root / skill
        references = skill_root / "references"
        references.mkdir(parents=True)
        links = "\n".join(f"Read `references/{name}`." for name in names)
        (skill_root / "SKILL.md").write_text(f"{links}\n", encoding="utf-8")
        for name in names:
            (references / name).write_text("contract\n", encoding="utf-8")


def test_the_fixture_satisfies_the_contract(tmp_path: Path) -> None:
    """The complete fixture tree has no packaging problem of its own."""
    _materialise_contract_skills(tmp_path)

    assert _validate_contract_references(tmp_path) == []


def test_an_unshipped_reference_is_reported(tmp_path: Path) -> None:
    """A contract reference absent from the skill directory is reported."""
    _materialise_contract_skills(tmp_path)
    (tmp_path / "tech-design-doc/references/field-evidence.md").unlink()

    problems = _validate_contract_references(tmp_path)

    assert problems == ["tech-design-doc/references/field-evidence.md is not shipped"]


def test_an_unnamed_reference_is_reported(tmp_path: Path) -> None:
    """A shipped contract reference its skill never names is reported."""
    _materialise_contract_skills(tmp_path)
    (tmp_path / "terms-of-reference-doc/SKILL.md").write_text(
        "Read `references/elicitation-protocol.md`.\n", encoding="utf-8"
    )

    problems = _validate_contract_references(tmp_path)

    assert problems == [
        "problem-contract.md is not named inside skills/terms-of-reference-doc"
    ]
