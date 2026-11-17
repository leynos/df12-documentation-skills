"""Contract: architecture-contract guidance ships with its skill.

The terms-of-reference and technical-design skills hand their downstream
contract through named reference files. A reference that is deleted, renamed,
or never named by its own skill silently removes that guidance from an
installing agent, so these checks assert that each contract reference is
shipped inside its skill and named somewhere in that skill's Markdown other
than the reference itself.

They also retain the rules the contract rests on: the reading order, the
independent compatibility prohibitions, baseline/target/gap records,
dependency and stale-blocker handling, evidence expiry, stakeholder decision
rights, the ``BLOCKED``/``COMPLETE`` reconciliation, and the traceable handoff
records. The rule checks read the shipped Markdown and fail when wording is
deleted. One further check rejects a permissive sentence that would grant the
compatibility machinery the prohibitions deny. Whether an agent obeys that
guidance is the subject of the fresh-agent scenarios in
``docs/architecture-contract-validation.md``, not of a phrase assertion here.
"""

from __future__ import annotations

import dataclasses as dc
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
CONTRACT_REFERENCES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("tech-design-doc", ("architecture-contract.md", "field-evidence.md")),
    ("terms-of-reference-doc", ("problem-contract.md",)),
)


@dc.dataclass(frozen=True)
class _RetainedRule:
    """Describe one contract rule and the document that must state it."""

    rule: str
    document: Path
    text: str


_RETAINED_RULES: tuple[_RetainedRule, ...] = (
    _RetainedRule(
        rule="design reading order before intake, outlining, and handoff",
        document=Path("skills/tech-design-doc/SKILL.md"),
        text=(
            "Read `references/architecture-contract.md` before intake, "
            "outlining, and handoff."
        ),
    ),
    _RetainedRule(
        rule="design compatibility prohibition summary",
        document=Path("skills/tech-design-doc/SKILL.md"),
        text=(
            "Designs MUST NOT prescribe source-API compatibility machinery for "
            "private APIs (including application-internal public surfaces), "
            "test-only APIs, pre-1.0 APIs, or unreleased API changes ahead of "
            "the latest formal release tag."
        ),
    ),
    _RetainedRule(
        rule="design separates released contracts from prohibited surfaces",
        document=Path("skills/tech-design-doc/SKILL.md"),
        text=(
            "Assess existing released 1.0+ contracts and deployed-data or "
            "wire-format obligations separately."
        ),
    ),
    _RetainedRule(
        rule="design reconciler blocks and awaits explicit acceptance",
        document=Path("skills/tech-design-doc/SKILL.md"),
        text=(
            "An executing ExecPlan records the deviation in `Decision log`, "
            "enters `BLOCKED`, and awaits explicit acceptance. Update the ToR, "
            "design, or ADR with the approved resolution before `COMPLETE`;"
        ),
    ),
    _RetainedRule(
        rule="design reference prohibition governs its list",
        document=Path("skills/tech-design-doc/references/architecture-contract.md"),
        text="Designs MUST NOT prescribe source-API compatibility machinery for:",
    ),
    _RetainedRule(
        rule="design prohibits compatibility for private APIs",
        document=Path("skills/tech-design-doc/references/architecture-contract.md"),
        text=(
            "- private APIs, including application-internal interfaces declared public;"
        ),
    ),
    _RetainedRule(
        rule="design prohibits compatibility for test-only APIs",
        document=Path("skills/tech-design-doc/references/architecture-contract.md"),
        text="- test-only APIs and support surfaces;",
    ),
    _RetainedRule(
        rule="design prohibits compatibility for pre-1.0 APIs",
        document=Path("skills/tech-design-doc/references/architecture-contract.md"),
        text="- pre-1.0 APIs; or",
    ),
    _RetainedRule(
        rule="design prohibits compatibility for unreleased API changes",
        document=Path("skills/tech-design-doc/references/architecture-contract.md"),
        text=(
            "- unreleased API changes ahead of the latest applicable formal "
            "release tag."
        ),
    ),
    _RetainedRule(
        rule="design prohibitions are independent, not preferences",
        document=Path("skills/tech-design-doc/references/architecture-contract.md"),
        text=(
            "These are independent prohibitions, not preferences. Naming a "
            "consumer or citing an older ADR does not create an exception "
            "within these categories."
        ),
    ),
    _RetainedRule(
        rule="design reference blocks a deviation until accepted",
        document=Path("skills/tech-design-doc/references/architecture-contract.md"),
        text=(
            "the executing plan records a proposed deviation in `Decision log`, "
            "identifies impacted IDs, enters `BLOCKED`, and awaits explicit "
            "acceptance. Reconcile the approved resolution into the ToR, design, "
            "ADRs, roadmap links, and ExecPlan as applicable before `COMPLETE`."
        ),
    ),
    _RetainedRule(
        rule="design hands a traceable record to the ExecPlan",
        document=Path("skills/tech-design-doc/references/architecture-contract.md"),
        text=(
            "At delivery, provide the receiving ExecPlan with the conformance "
            "basis, selected requirement/design/gap IDs, verification "
            "obligations and axioms, compatibility assessment, acceptance "
            "boundaries, resource constraints, and unresolved decisions."
        ),
    ),
    _RetainedRule(
        rule="ExecPlan records milestones, gaps, and acceptance evidence",
        document=Path("skills/tech-design-doc/references/architecture-contract.md"),
        text=(
            "The ExecPlan chooses the work breakdown and records milestone IDs, "
            "assigned gaps, validated end states, acceptance evidence, "
            "conformance checks, recovery paths, and remaining gaps."
        ),
    ),
    _RetainedRule(
        rule="design records baseline, target, and gap evidence",
        document=Path("skills/tech-design-doc/references/architecture-contract.md"),
        text=(
            "A useful gap record contains ID, upstream requirement, baseline "
            "evidence, target state, missing capability or mismatch, "
            "disposition, resolution owner, unblock condition, and verification "
            "obligation."
        ),
    ),
    _RetainedRule(
        rule="design records each dependency and its unblock condition",
        document=Path("skills/tech-design-doc/references/architecture-contract.md"),
        text=(
            "Each dependency needs a provider, consumer, required capability, "
            "scope, linked evidence, and exact unblock condition. Separate a "
            "prerequisite for one milestone from a release blocker or a later "
            "outcome-validation dependency."
        ),
    ),
    _RetainedRule(
        rule="design expires evidence at rebases and upstream change",
        document=Path("skills/tech-design-doc/references/architecture-contract.md"),
        text=(
            "Record evidence expiry triggers: rebases, changed external "
            "contracts, upstream merges, moved symbols, altered benchmark "
            "paths, and release/deployment changes. Re-check affected claims "
            "before downstream work uses them."
        ),
    ),
    _RetainedRule(
        rule="design marks handoff readiness by scope",
        document=Path("skills/tech-design-doc/references/architecture-contract.md"),
        text=(
            "Mark readiness by scope: ready for an implementation plan, bounded "
            "discovery only, or blocked. Design acceptance does not bypass the "
            "ExecPlan's approval gate."
        ),
    ),
    _RetainedRule(
        rule="design requires non-vacuous verification obligations",
        document=Path("skills/tech-design-doc/references/architecture-contract.md"),
        text=(
            "Non-vacuity is local to each obligation. Show that preconditions "
            "admit a witness, generators reach material classes, and model "
            "states and transitions are reachable."
        ),
    ),
    _RetainedRule(
        rule="design requires a model to correspond to repository logic",
        document=Path("skills/tech-design-doc/references/architecture-contract.md"),
        text="A model must correspond to the repository's actual logic.",
    ),
    _RetainedRule(
        rule="terms reading order before intake and at handoff",
        document=Path("skills/terms-of-reference-doc/SKILL.md"),
        text=(
            "Read `references/problem-contract.md` before intake and again at handoff."
        ),
    ),
    _RetainedRule(
        rule="terms compatibility prohibition summary",
        document=Path("skills/terms-of-reference-doc/SKILL.md"),
        text=(
            "Terms of reference MUST NOT create source-API compatibility "
            "requirements for private APIs (including application-internal "
            "public surfaces), test-only APIs, pre-1.0 APIs, or unreleased API "
            "changes ahead of the latest formal release tag."
        ),
    ),
    _RetainedRule(
        rule="terms keeps released contracts as a separate assessment",
        document=Path("skills/terms-of-reference-doc/SKILL.md"),
        text=(
            "Existing released 1.0+ contracts and deployed-data or wire-format "
            "obligations require separate, sourced assessment; an internal "
            "change does not erase a released contract."
        ),
    ),
    _RetainedRule(
        rule="terms reference prohibition governs its list",
        document=Path("skills/terms-of-reference-doc/references/problem-contract.md"),
        text=(
            "Terms of reference MUST NOT impose source-API compatibility machinery on:"
        ),
    ),
    _RetainedRule(
        rule="terms prohibits compatibility for private APIs",
        document=Path("skills/terms-of-reference-doc/references/problem-contract.md"),
        text=(
            "- private APIs, including public declarations used only within an "
            "application;"
        ),
    ),
    _RetainedRule(
        rule="terms prohibits compatibility for test-only APIs",
        document=Path("skills/terms-of-reference-doc/references/problem-contract.md"),
        text="- test-only APIs and support surfaces;",
    ),
    _RetainedRule(
        rule="terms prohibits compatibility for pre-1.0 APIs",
        document=Path("skills/terms-of-reference-doc/references/problem-contract.md"),
        text="- pre-1.0 APIs; or",
    ),
    _RetainedRule(
        rule="terms prohibits compatibility for unreleased API changes",
        document=Path("skills/terms-of-reference-doc/references/problem-contract.md"),
        text=(
            "- unreleased API changes ahead of the latest applicable formal "
            "release tag."
        ),
    ),
    _RetainedRule(
        rule="terms exclusions are independent of a named consumer",
        document=Path("skills/terms-of-reference-doc/references/problem-contract.md"),
        text=(
            "These exclusions are independent. A named consumer does not create "
            "an exception for a pre-1.0 or test-only API."
        ),
    ),
    _RetainedRule(
        rule="terms blocks until the resolution reaches upstream artefacts",
        document=Path("skills/terms-of-reference-doc/references/problem-contract.md"),
        text=(
            "The ExecPlan's `Decision log` records deviations; architectural "
            "deviations enter `BLOCKED` until explicitly accepted. Before it "
            "reaches `COMPLETE`, the approved resolution must appear in the "
            "authoritative upstream artefacts and all affected links."
        ),
    ),
    _RetainedRule(
        rule="terms handoff names the accepted revision and its material IDs",
        document=Path("skills/terms-of-reference-doc/references/problem-contract.md"),
        text=(
            "Before handoff, identify the accepted revision, material IDs, "
            "stakeholder concerns, success criteria, governing constraints, "
            "assumption expiry triggers, and dependency conditions."
        ),
    ),
    _RetainedRule(
        rule="terms keeps evidence status separate from approval",
        document=Path("skills/terms-of-reference-doc/references/problem-contract.md"),
        text=(
            "Keep the existing `[KNOWN]`, `[ASSUMED]`, and `[OPEN]` evidence "
            "labels, but record approval separately when the claim directs work."
        ),
    ),
    _RetainedRule(
        rule="terms keeps identifiers stable across editorial changes",
        document=Path("skills/terms-of-reference-doc/references/problem-contract.md"),
        text="Keep IDs stable across editorial changes.",
    ),
    _RetainedRule(
        rule="terms denies self-approval by repetition",
        document=Path("skills/terms-of-reference-doc/references/problem-contract.md"),
        text=(
            "Agent summaries, reviewer suggestions, and generated documents do "
            "not approve themselves by repetition. Identify the actual decision "
            "authority, or leave it unknown."
        ),
    ),
    _RetainedRule(
        rule="terms separates a recommendation from delegated approval",
        document=Path("skills/terms-of-reference-doc/references/problem-contract.md"),
        text=(
            "A discovery agent may recommend a change without approving it or "
            "completing the parent goal."
        ),
    ),
    _RetainedRule(
        rule="terms keeps decision rights distinct from advisory review",
        document=Path("skills/terms-of-reference-doc/references/problem-contract.md"),
        text=(
            "Ask who may accept a scope change, resolve an assumption, or "
            "accept residual risk. Advisory review, technical approval, release "
            "authority, and product prioritization are not interchangeable."
        ),
    ),
    _RetainedRule(
        rule="terms reconciles stale blocker edges",
        document=Path("skills/terms-of-reference-doc/references/problem-contract.md"),
        text=(
            "Reconcile stale blocker edges against their actual unblock "
            "condition, not only a recent activity window."
        ),
    ),
)

_PERMISSIVE_COMPATIBILITY = re.compile(
    r"\b(?:may|should|is permitted to|are permitted to|is allowed to|"
    r"are allowed to)\b[^.]{0,80}?\b(?:compatibility|compatible|shims?|"
    r"aliases?|facades?|wrappers?|entrypoints?)\b",
    re.IGNORECASE,
)


def _normalised(path: Path) -> str:
    """Return one document's prose with each run of whitespace collapsed."""
    return " ".join(path.read_text(encoding="utf-8").split())


def _validate_contract_references(skills_root: Path) -> list[str]:
    """Return one problem per contract reference that is missing or unnamed."""
    problems: list[str] = []
    for skill, names in CONTRACT_REFERENCES:
        skill_root = skills_root / skill
        for name in names:
            reference = skill_root / "references" / name
            if not reference.is_file():
                problems.append(f"{reference.relative_to(skills_root)} is not shipped")
                continue
            named_elsewhere = any(
                name in path.read_text(encoding="utf-8")
                for path in sorted(skill_root.rglob("*.md"))
                if path != reference
            )
            if not named_elsewhere:
                problems.append(f"{name} is not named inside skills/{skill}")
    return problems


def _missing_rules(root: Path) -> list[str]:
    """Return the rules whose required wording is absent from their document."""
    missing: list[str] = []
    for rule in _RETAINED_RULES:
        path = root / rule.document
        if not path.is_file() or rule.text not in _normalised(path):
            missing.append(rule.rule)
    return missing


def _permissive_compatibility_claims(root: Path) -> list[str]:
    """Return one report per sentence that permits compatibility machinery."""
    problems: list[str] = []
    documents = sorted({rule.document for rule in _RETAINED_RULES})
    for document in documents:
        path = root / document
        if not path.is_file():
            continue
        for sentence in re.split(r"(?<=[.!?])\s+", _normalised(path)):
            match = _PERMISSIVE_COMPATIBILITY.search(sentence)
            if match is not None:
                problems.append(f"{document}: {match.group(0)}")
    return problems


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


def _materialise_rule_documents(root: Path) -> None:
    """Write each rule document with all of its required wording present."""
    by_document: dict[Path, list[str]] = {}
    for rule in _RETAINED_RULES:
        by_document.setdefault(rule.document, []).append(rule.text)
    for document, texts in by_document.items():
        path = root / document
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n\n".join(texts) + "\n", encoding="utf-8")


def test_contract_references_are_shipped_and_named() -> None:
    """Every architecture-contract reference ships and is named by its skill."""
    assert _validate_contract_references(SKILLS_ROOT) == []


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
    """A reference that names only itself is still reported."""
    _materialise_contract_skills(tmp_path)
    (tmp_path / "terms-of-reference-doc/SKILL.md").write_text(
        "Read `references/elicitation-protocol.md`.\n", encoding="utf-8"
    )
    (tmp_path / "terms-of-reference-doc/references/problem-contract.md").write_text(
        "See `references/problem-contract.md`.\n", encoding="utf-8"
    )

    problems = _validate_contract_references(tmp_path)

    assert problems == [
        "problem-contract.md is not named inside skills/terms-of-reference-doc"
    ]


def test_contract_rules_are_retained() -> None:
    """Every contract rule is still stated in the document that owns it."""
    assert _missing_rules(ROOT) == []


def test_the_rule_fixture_is_complete(tmp_path: Path) -> None:
    """The rule fixture satisfies every retained-rule check."""
    _materialise_rule_documents(tmp_path)

    assert _missing_rules(tmp_path) == []


def test_a_deleted_rule_is_reported(tmp_path: Path) -> None:
    """Deleting a rule's wording from its document is reported."""
    _materialise_rule_documents(tmp_path)
    document = tmp_path / "skills/terms-of-reference-doc/SKILL.md"
    document.write_text("Unrelated guidance only.\n", encoding="utf-8")

    missing = _missing_rules(tmp_path)

    assert "terms reading order before intake and at handoff" in missing
    assert "terms compatibility prohibition summary" in missing


def test_an_inverted_rule_is_reported(tmp_path: Path) -> None:
    """Inverting a rule's wording is reported rather than silently accepted."""
    _materialise_rule_documents(tmp_path)
    document = tmp_path / "skills/tech-design-doc/SKILL.md"
    text = document.read_text(encoding="utf-8").replace(
        "Designs MUST NOT prescribe source-API compatibility machinery",
        "Designs SHOULD prescribe source-API compatibility machinery",
    )
    document.write_text(text, encoding="utf-8")

    missing = _missing_rules(tmp_path)

    assert missing == ["design compatibility prohibition summary"]


def test_an_inverted_design_reference_prohibition_is_reported(tmp_path: Path) -> None:
    """Inverting a reference's governing prohibition is reported."""
    _materialise_rule_documents(tmp_path)
    document = tmp_path / "skills/tech-design-doc/references/architecture-contract.md"
    text = document.read_text(encoding="utf-8").replace(
        "Designs MUST NOT prescribe source-API compatibility machinery for:",
        "Designs MAY prescribe source-API compatibility machinery for:",
    )
    document.write_text(text, encoding="utf-8")

    missing = _missing_rules(tmp_path)

    assert missing == ["design reference prohibition governs its list"]


def test_an_inverted_terms_reference_prohibition_is_reported(tmp_path: Path) -> None:
    """Inverting the problem reference's governing prohibition is reported."""
    _materialise_rule_documents(tmp_path)
    document = tmp_path / "skills/terms-of-reference-doc/references/problem-contract.md"
    text = document.read_text(encoding="utf-8").replace(
        "Terms of reference MUST NOT impose source-API compatibility machinery on:",
        "Terms of reference MAY impose source-API compatibility machinery on:",
    )
    document.write_text(text, encoding="utf-8")

    missing = _missing_rules(tmp_path)

    assert missing == ["terms reference prohibition governs its list"]


def test_each_retained_rule_is_individually_detectable(tmp_path: Path) -> None:
    """Removing one rule's wording reports exactly that rule."""
    _materialise_rule_documents(tmp_path)

    for rule in _RETAINED_RULES:
        document = tmp_path / rule.document
        original = document.read_text(encoding="utf-8")
        document.write_text(original.replace(rule.text, ""), encoding="utf-8")

        assert _missing_rules(tmp_path) == [rule.rule], rule.rule

        document.write_text(original, encoding="utf-8")


def test_no_shipped_sentence_permits_compatibility_machinery() -> None:
    """No shipped contract sentence grants what the prohibitions deny."""
    assert _permissive_compatibility_claims(ROOT) == []


def test_a_permissive_compatibility_sentence_is_reported(tmp_path: Path) -> None:
    """A permissive sentence in either prohibition section is reported."""
    _materialise_rule_documents(tmp_path)
    design = tmp_path / "skills/tech-design-doc/references/architecture-contract.md"
    terms = tmp_path / "skills/terms-of-reference-doc/references/problem-contract.md"
    design.write_text(
        design.read_text(encoding="utf-8")
        + "\nDesigns may prescribe source-API compatibility machinery for private"
        " APIs.\n",
        encoding="utf-8",
    )
    terms.write_text(
        terms.read_text(encoding="utf-8")
        + "\nTerms of reference should impose compatibility requirements on"
        " test-only APIs.\n",
        encoding="utf-8",
    )

    problems = _permissive_compatibility_claims(tmp_path)

    assert len(problems) == 2
    assert problems[0].startswith("skills/tech-design-doc/")
    assert problems[1].startswith("skills/terms-of-reference-doc/")
