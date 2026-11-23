"""Contract: the workflow-boundary validator decides the documented boundaries.

The two skills state boundaries that a record can be decided against rather
than judged: a plan that carries an unaccepted deviation must not claim
`ACTIVE` or `COMPLETE` until a later Decision log entry accepts it, a plan that
claims `BLOCKED` must still carry a pending deviation, and a handoff must state
its approval state, its readiness, the stable identifiers downstream work
inherits, and the route back when an assumption fails.
``scripts/check_workflow_boundary.py`` decides those boundaries; this module
drives it through its command line, so the test depends only on the interface a
contributor uses. One parametrised table covers every documented status against
every Decision log condition, and another covers each required handoff element
present and absent.

The same validator runs two phrase checks over the published output. No record
for a private, test-only, pre-1.0, or unreleased surface may permit
compatibility machinery, and the released-contract record must keep its
positive control: an affirmative statement that a layer or migration is
admissible. These are phrase checks. They show that the recorded proposals
contain no permissive sentence for a prohibited surface; they do not show that
a plan implements nothing else.

The fixtures are derived from the forms the skills document. The record
fixtures use the `Status` line and `Decision log` section the ExecPlan contract
defines; the handoff fixtures use the revision, approval state, stable IDs,
readiness classification, and feedback route that `terms-of-reference-doc`
requires. One test copies the two skills, deletes a governing sentence from the
copy, and asserts that the validator then fails, so the check cannot pass by
forgetting the rule it is deciding. The shim-injection controls copy a
published artefact, append a permissive sentence in each documented form, and
require its diagnostic. The Hypothesis properties load the shipped module and
exercise `compatibility_problems` directly, so the generated cases test the one
implementation the command line runs.

They do not execute either skill. Whether an agent obeys the guidance remains
the subject of the scenarios themselves, which are manual evidence; a passing
check here says only that the recorded output satisfies the stated boundary.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from hypothesis import assume, given, settings
from hypothesis import strategies as st

if TYPE_CHECKING:
    from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/check_workflow_boundary.py"
SKILLS = ROOT / "skills"
ARTEFACTS = ROOT / "docs/validation/2026-11-19-agent-scenarios"
PROHIBITED_SETS = ("c1", "c2", "c3-271b0f8", "c3-29cd658", "c4", "c6")
PERMISSION_MISSING = (
    "no record states that a compatibility layer or migration is admissible"
)


def _run(
    check: str, *records: Path, skills_root: Path = SKILLS
) -> subprocess.CompletedProcess[str]:
    """Return the validator's result for the given records."""
    return subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--skills-root",
            str(skills_root),
            check,
            *(str(record) for record in records),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def _load_validator() -> ModuleType:
    """Return the shipped validator loaded as a module."""
    spec = importlib.util.spec_from_file_location("check_workflow_boundary", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


COMPATIBILITY_PROBLEMS = _load_validator().compatibility_problems


def _diagnostics(result: subprocess.CompletedProcess[str]) -> str:
    """Return both captured streams for an assertion message."""
    return f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"


def _messages(result: subprocess.CompletedProcess[str]) -> list[str]:
    """Return the validator's diagnostic lines."""
    return result.stdout.splitlines()


def _artefacts(directory: str) -> list[Path]:
    """Return the published artefacts of one scenario in name order."""
    return sorted((ARTEFACTS / directory).iterdir())


def _fixture(tmp_path: Path, text: str) -> Path:
    """Write one record fixture and return its path."""
    path = tmp_path / "record.md"
    path.write_text(text, encoding="utf-8")
    return path


def _published(*parts: str) -> Path:
    """Return the path of one published artefact."""
    return ARTEFACTS.joinpath(*parts)


def test_the_published_plan_blocks_on_its_recorded_deviation(
    tmp_path: Path,
) -> None:
    """The C3 plan is blocked, and claiming completion is reported."""
    plan = _published("c3-271b0f8", "execplan-library-api-rename.md.txt")

    accepted = _run("status", plan)

    assert accepted.returncode == 0, _diagnostics(accepted)
    assert accepted.stdout == "", _diagnostics(accepted)
    assert accepted.stderr == "", _diagnostics(accepted)

    completed = _fixture(
        tmp_path,
        plan.read_text(encoding="utf-8").replace(
            "Status: BLOCKED", "Status: COMPLETE", 1
        ),
    )
    rejected = _run("status", completed)

    assert rejected.returncode == 1, _diagnostics(rejected)
    assert (
        "COMPLETE with an unaccepted deviation in the Decision log" in rejected.stdout
    ), _diagnostics(rejected)


def test_the_published_revision_record_blocks_on_its_deviation() -> None:
    """The second C3 record is blocked for the reason its Decision log states."""
    record = _published("c3-29cd658", "execplan-record.md.txt")

    result = _run("status", record)

    assert result.returncode == 0, _diagnostics(result)
    assert result.stdout == "", _diagnostics(result)


def test_both_published_c3_handoffs_state_their_boundaries() -> None:
    """Each C3 run's handoff names approval, readiness, IDs, and feedback."""
    first = _published("c3-271b0f8", "terms-of-reference.md.txt")
    second = _published("c3-29cd658", "terms-of-reference.md.txt")

    accepted = _run("handoff", first)
    other = _run("handoff", second)

    assert accepted.returncode == 0, _diagnostics(accepted)
    assert other.returncode == 0, _diagnostics(other)


_STATUSES = ("DRAFT", "ACTIVE", "BLOCKED", "COMPLETE", "PENDING")
_BLOCKED_WITHOUT = (
    "BLOCKED without a Decision log entry recording an unaccepted deviation"
)
_DECISION_LOGS: dict[str, str] = {
    "absent": "",
    "template-only": (
        "\n## Decision log\n\n"
        "Add one entry:\n\n"
        "```plaintext\n"
        "- D-<next free>. Decision: <what was decided>.\n"
        "  Status: proposal pending acceptance.\n"
        "```\n"
    ),
    "unaccepted": (
        "\n## Decision log\n\n"
        "- D1. Decision: rename the module. "
        "Date/Author: 2026-11-19, authoring agent (proposed; not approved).\n"
    ),
    "accepted": (
        "\n## Decision log\n\n"
        "- D1. Decision: rename the module. "
        "Date/Author: 2026-11-19, authoring agent (proposed; not approved).\n\n"
        "- D2. Decision: accept D1 as the approved resolution.\n"
        "  Rationale: the policy owner approved the amended target.\n"
        "  Date/Author: 2026-11-20, policy owner.\n"
    ),
    "future-acceptance": (
        "\n## Decision log\n\n"
        "- D1. Decision: rename the module. "
        "Date/Author: 2026-11-19, authoring agent (proposed; not approved).\n\n"
        "- D2. Decision: D1 will be accepted.\n"
        "  Rationale: the policy owner has not ruled yet.\n"
        "  Date/Author: 2026-11-20, authoring agent.\n"
    ),
    "partial-acceptance": (
        "\n## Decision log\n\n"
        "- D1. Decision: rename the module. "
        "Date/Author: 2026-11-19, authoring agent (proposed; not approved).\n\n"
        "- D2. Decision: replace the module. "
        "Date/Author: 2026-11-19, authoring agent (proposed; not approved).\n\n"
        "- D3. Decision: approve D2; retain D1 for separate review.\n"
        "  Rationale: the policy owner approved only the second proposal.\n"
        "  Date/Author: 2026-11-20, policy owner.\n"
    ),
    "unrelated-anaphor": (
        "\n## Decision log\n\n"
        "- D1. Decision: rename the module. "
        "Date/Author: 2026-11-19, authoring agent (proposed; not approved).\n\n"
        "- D2. Decision: accept the proposal D99.\n"
        "  Rationale: a different proposal was approved.\n"
        "  Date/Author: 2026-11-20, policy owner.\n"
    ),
    "none": "\n## Decision log\n\n- D1. Renamed the module.\n",
}


def _expected_status_problems(status: str, condition: str) -> list[str]:
    """Return the diagnostics the documented rules require for one cell."""
    problems: list[str] = []
    if status not in {"DRAFT", "ACTIVE", "BLOCKED", "COMPLETE"}:
        problems.append(f"unknown status {status}")
    if condition == "absent":
        problems.append("no Decision log")
    elif condition in {
        "unaccepted",
        "future-acceptance",
        "partial-acceptance",
        "unrelated-anaphor",
    }:
        if status in {"ACTIVE", "COMPLETE"}:
            problems.append(
                f"{status} with an unaccepted deviation in the Decision log"
            )
    elif status == "BLOCKED":
        problems.append(_BLOCKED_WITHOUT)
    return problems


@pytest.mark.parametrize("condition", tuple(_DECISION_LOGS))
@pytest.mark.parametrize("status", _STATUSES)
def test_every_status_is_decided_against_every_decision_log(
    tmp_path: Path, status: str, condition: str
) -> None:
    """Each status and Decision log condition receives its documented verdict."""
    record = _fixture(tmp_path, f"Status: {status}\n{_DECISION_LOGS[condition]}")
    expected = [
        f"{record}: {message}"
        for message in _expected_status_problems(status, condition)
    ]

    result = _run("status", record)

    assert result.returncode == (1 if expected else 0), _diagnostics(result)
    assert _messages(result) == expected, _diagnostics(result)


def test_an_unnamed_acceptance_clears_the_only_pending_deviation(
    tmp_path: Path,
) -> None:
    """Identifier-free acceptance of the sole pending deviation clears it."""
    record = _fixture(
        tmp_path,
        "Status: COMPLETE\n"
        "\n## Decision log\n\n"
        "- D1. Decision: rename the module. "
        "Date/Author: 2026-11-19, authoring agent (proposed; not approved).\n\n"
        "- D2. Decision: accept the proposal.\n"
        "  Rationale: the owner approved it.\n"
        "  Date/Author: 2026-11-20, policy owner.\n",
    )

    result = _run("status", record)

    assert result.returncode == 0, _diagnostics(result)
    assert result.stdout == "", _diagnostics(result)


def test_one_decision_accepts_every_deviation_it_names(tmp_path: Path) -> None:
    """A coordinated acceptance clears each deviation the same clause names."""
    record = _fixture(
        tmp_path,
        "Status: COMPLETE\n"
        "\n## Decision log\n\n"
        "- D1. Decision: rename the module. "
        "Date/Author: 2026-11-19, authoring agent (proposed; not approved).\n\n"
        "- D2. Decision: replace the module. "
        "Date/Author: 2026-11-19, authoring agent (proposed; not approved).\n\n"
        "- D3. Decision: accept D1 and D2 as the approved resolution.\n"
        "  Rationale: the policy owner approved both proposals.\n"
        "  Date/Author: 2026-11-20, policy owner.\n",
    )

    result = _run("status", record)

    assert result.returncode == 0, _diagnostics(result)
    assert result.stdout == "", _diagnostics(result)


_HANDOFF_ELEMENTS: dict[str, str] = {
    "approval state": "Accepted revision: none.",
    "readiness classification": "Ready for design.",
    "stable identifier": "TOR-GOAL-001 is inherited.",
    "feedback route": "Feedback route: the ToR decision authority.",
}


def _handoff(omit: str = "") -> str:
    """Return a handoff statement that omits at most one required element."""
    statements = " ".join(
        statement for label, statement in _HANDOFF_ELEMENTS.items() if label != omit
    )
    return f"## Handoff\n\n{statements}\n"


@pytest.mark.parametrize("omit", ["", *_HANDOFF_ELEMENTS])
def test_every_handoff_element_is_decided_present_and_absent(
    tmp_path: Path, omit: str
) -> None:
    """Each required handoff element is accepted when present and reported when not."""
    record = _fixture(tmp_path, _handoff(omit))
    expected = [] if not omit else [f"{record}: handoff does not state its {omit}"]

    result = _run("handoff", record)

    assert result.returncode == (1 if expected else 0), _diagnostics(result)
    assert _messages(result) == expected, _diagnostics(result)


def test_a_handoff_without_a_route_back_is_reported(tmp_path: Path) -> None:
    """A label naming an absent route does not state a route."""
    record = _fixture(
        tmp_path,
        (
            "## Handoff\n\n"
            "Accepted revision: none. Ready for design. TOR-GOAL-001 is inherited.\n"
            "Feedback route: none.\n"
        ),
    )

    result = _run("handoff", record)

    assert result.returncode == 1, _diagnostics(result)
    assert "handoff does not state its feedback route" in result.stdout, _diagnostics(
        result
    )


def test_a_missing_handoff_section_is_reported(tmp_path: Path) -> None:
    """A record with no handoff section is reported as such."""
    record = _fixture(tmp_path, "No handoff is recorded here.\n")

    result = _run("handoff", record)

    assert result.returncode == 1, _diagnostics(result)
    assert _messages(result) == [f"{record}: no handoff section"], _diagnostics(result)


def test_a_skill_that_drops_its_rule_fails_the_check(tmp_path: Path) -> None:
    """Deleting the BLOCKED rule from a copied skill fails the validator."""
    skills_root = tmp_path / "skills"
    for name in ("tech-design-doc", "terms-of-reference-doc"):
        (skills_root / name).mkdir(parents=True)
        source = SKILLS / name / "SKILL.md"
        (skills_root / name / "SKILL.md").write_text(
            source.read_text(encoding="utf-8"), encoding="utf-8"
        )
    record = _fixture(
        tmp_path,
        (
            "## Handoff\n\n"
            "Accepted revision: 7. Ready for design. TOR-GOAL-001 is inherited.\n"
            "Feedback route: the ToR decision authority.\n"
        ),
    )

    intact = _run("handoff", record, skills_root=skills_root)

    assert intact.returncode == 0, _diagnostics(intact)
    assert intact.stdout == "", _diagnostics(intact)

    drifted = skills_root / "tech-design-doc/SKILL.md"
    drifted.write_text(
        drifted.read_text(encoding="utf-8").replace(
            "enters `BLOCKED`", "enters a blocked state"
        ),
        encoding="utf-8",
    )

    rejected = _run("handoff", record, skills_root=skills_root)

    assert rejected.returncode == 1, _diagnostics(rejected)
    assert "no longer states that an executing ExecPlan enters BLOCKED" in (
        rejected.stdout
    ), _diagnostics(rejected)


def test_the_published_proposals_permit_no_compatibility_machinery() -> None:
    """No artefact for a prohibited surface proposes compatibility machinery."""
    records = [path for name in PROHIBITED_SETS for path in _artefacts(name)]

    result = _run("prohibitions", *records)

    assert result.returncode == 0, _diagnostics(result)
    assert result.stdout == "", _diagnostics(result)


_PERMISSION_FORMS = (
    "may",
    "can",
    "should",
    "might",
    "is permitted to",
    "are permitted to",
    "is allowed to",
    "are allowed to",
)


@pytest.mark.parametrize("form", _PERMISSION_FORMS)
@pytest.mark.parametrize("directory", PROHIBITED_SETS)
def test_injecting_a_shim_into_an_artefact_set_is_reported(
    tmp_path: Path, directory: str, form: str
) -> None:
    """A permissive sentence in each documented form is reported."""
    source = _artefacts(directory)[0]
    mutated = tmp_path / source.name
    mutated.write_text(
        source.read_text(encoding="utf-8")
        + f"\nThe design team {form} add a compatibility shim for the old name.\n",
        encoding="utf-8",
    )

    result = _run("prohibitions", mutated)

    assert result.returncode == 1, _diagnostics(result)
    assert "permits compatibility machinery" in result.stdout, _diagnostics(result)


@pytest.mark.parametrize(
    ("sentence", "reported"),
    [
        pytest.param(
            "Designs should not add compatibility shims for private APIs.",
            False,
            id="negated-modality",
        ),
        pytest.param(
            "The design may proceed without a compatibility shim.",
            False,
            id="negated-surface",
        ),
        pytest.param(
            "Designs should not prescribe obsolete behaviour and may add "
            "compatibility shims for private APIs.",
            True,
            id="contrastive-modality",
        ),
        pytest.param(
            "The design may retain the old name, or add compatibility shims.",
            True,
            id="coordinated-verbs",
        ),
        pytest.param(
            "The authority may resolve the conflict, and is the alias owner.",
            False,
            id="independent-clause",
        ),
        pytest.param(
            "A private API can retain compatibility wrappers.",
            True,
            id="can-grant",
        ),
        pytest.param(
            "A maintainer can then read each call site and see the contract, "
            "without an obsolete overload or wrapper.",
            False,
            id="can-capability",
        ),
        pytest.param(
            "The design team might add compatibility shims for private APIs.",
            True,
            id="might",
        ),
        pytest.param(
            "Each module is permitted a compatibility shim.",
            True,
            id="permitted-without-to",
        ),
        pytest.param(
            "Each module is allowed a compatibility shim.",
            True,
            id="allowed-without-to",
        ),
        pytest.param(
            "Designs may add compatibility wrappers for released 2.1 APIs with an "
            "explicit compatibility commitment and a deployed external consumer.",
            False,
            id="released-contract",
        ),
        pytest.param(
            "Designs may add compatibility wrappers for released 0.8 APIs.",
            True,
            id="released-prohibited-surface",
        ),
        pytest.param(
            "Designs may add compatibility shims for API changes that have not "
            "yet been released.",
            True,
            id="unreleased-surface",
        ),
    ],
)
def test_the_prohibition_scan_decides_each_permission_form(
    tmp_path: Path, sentence: str, *, reported: bool
) -> None:
    """The command reports a permission and accepts a sentence that grants none."""
    record = _fixture(tmp_path, f"{sentence}\n")

    result = _run("prohibitions", record)

    assert result.returncode == (1 if reported else 0), _diagnostics(result)
    if reported:
        assert "permits compatibility machinery" in result.stdout, _diagnostics(result)
    else:
        assert result.stdout == "", _diagnostics(result)


@pytest.mark.parametrize(
    ("sentence", "missing"),
    [
        pytest.param("A layer or migration is admissible.", False, id="layer"),
        pytest.param("A deliberate migration is admissible.", False, id="migration"),
        pytest.param("No compatibility layer is admissible.", True, id="negated-layer"),
        pytest.param(
            "No layer or migration is admissible.", True, id="negated-migration"
        ),
        pytest.param(
            "Compatibility or a deliberate migration is forbidden.",
            True,
            id="forbidden-migration",
        ),
        pytest.param(
            "Do not use compatibility or a deliberate migration.",
            True,
            id="negated-imperative",
        ),
        pytest.param(
            "The design rejects compatibility or a deliberate migration.",
            True,
            id="rejecting-design",
        ),
        pytest.param(
            "A compatibility layer or a deliberate migration is not admissible.",
            True,
            id="negated-predicate",
        ),
        pytest.param(
            "A compatibility layer is not admissible, but the design is admissible.",
            True,
            id="negated-then-affirmative",
        ),
        pytest.param(
            "A compatibility layer is required, but the design is admissible.",
            True,
            id="predicate-in-another-clause",
        ),
        pytest.param(
            "A compatibility layer for released 2.1 APIs is admissible.",
            False,
            id="version-number-in-statement",
        ),
        pytest.param(
            "No compatibility layer for released 2.1 APIs is admissible.",
            True,
            id="version-number-negated",
        ),
    ],
)
def test_the_permission_scan_requires_an_affirmative_statement(
    tmp_path: Path, sentence: str, *, missing: bool
) -> None:
    """Only an affirmative admissibility statement satisfies the positive control."""
    record = _fixture(tmp_path, f"{sentence}\n")

    result = _run("permission", record)

    assert result.returncode == (1 if missing else 0), _diagnostics(result)
    if missing:
        assert PERMISSION_MISSING in result.stdout, _diagnostics(result)
    else:
        assert result.stdout == "", _diagnostics(result)


def test_the_released_contract_positive_control_is_kept() -> None:
    """The C5 records still state that a layer or migration is admissible."""
    result = _run("permission", *_artefacts("c5"))

    assert result.returncode == 0, _diagnostics(result)
    assert result.stdout == "", _diagnostics(result)


def test_a_prohibited_category_states_no_released_permission() -> None:
    """A private-surface record never states the released-contract permission."""
    result = _run("permission", *_artefacts("c1"))

    assert result.returncode == 1, _diagnostics(result)
    assert PERMISSION_MISSING in result.stdout, _diagnostics(result)


_NEUTRAL_WORDS = (
    "the",
    "design",
    "records",
    "evidence",
    "scope",
    "reviewers",
    "note",
    "that",
    "for",
    "private",
    "and",
    "its",
)
_COMPATIBILITY_TERMS = (
    "compatibility",
    "compatible",
    "shim",
    "alias",
    "facade",
    "wrapper",
    "entrypoint",
)
_CLAUSE_SEPARATORS = ("; ", ", and ", ", but ", ", or ", ", then ", ", so ")
_CLAUSE_SUBJECTS = ("the policy owner", "the release authority", "its maintainer")


@given(
    form=st.sampled_from(_PERMISSION_FORMS),
    words=st.lists(st.sampled_from(_NEUTRAL_WORDS), max_size=30),
    term=st.sampled_from(_COMPATIBILITY_TERMS),
)
@settings(max_examples=50, deadline=None)
def test_a_generated_permission_is_always_reported(
    form: str, words: list[str], term: str
) -> None:
    """Every permission paired with a compatibility term is reported."""
    sentence = f"The design team {form} retain {' '.join(words)} {term} machinery."

    problems = COMPATIBILITY_PROBLEMS(sentence)

    assert problems, sentence
    assert any(term in problem for problem in problems), sentence


@given(
    form=st.sampled_from(_PERMISSION_FORMS),
    words=st.lists(st.sampled_from(_NEUTRAL_WORDS), max_size=8),
    term=st.sampled_from(_COMPATIBILITY_TERMS),
)
@settings(max_examples=50, deadline=None)
def test_a_generated_negation_is_never_reported(
    form: str, words: list[str], term: str
) -> None:
    """A negated permission is never reported, however it is worded."""
    sentence = f"The design team {form} not retain {' '.join(words)} {term} machinery."

    problems = COMPATIBILITY_PROBLEMS(sentence)

    assert problems == [], sentence


@given(
    form=st.sampled_from(_PERMISSION_FORMS),
    separator=st.sampled_from(_CLAUSE_SEPARATORS),
    subject=st.sampled_from(_CLAUSE_SUBJECTS),
    term=st.sampled_from(_COMPATIBILITY_TERMS),
)
@settings(max_examples=50, deadline=None)
def test_a_generated_clause_boundary_ends_the_permission(
    form: str, separator: str, subject: str, term: str
) -> None:
    """An independent clause after the permission is not part of it."""
    sentence = (
        f"The design team {form} retain the old name{separator}"
        f"{subject} records the {term} decision."
    )

    problems = COMPATIBILITY_PROBLEMS(sentence)

    assert problems == [], sentence


@given(
    major=st.integers(min_value=1, max_value=99),
    minor=st.integers(min_value=0, max_value=99),
)
@settings(max_examples=50, deadline=None)
def test_a_generated_version_number_stays_inside_the_permission(
    major: int, minor: int
) -> None:
    """A version number's full stop does not end the released permission."""
    with tempfile.TemporaryDirectory() as directory:
        record = _fixture(
            Path(directory),
            f"A compatibility layer for released {major}.{minor} APIs is admissible.\n",
        )

        result = _run("permission", record)

    assert result.returncode == 0, _diagnostics(result)
    assert result.stdout == "", _diagnostics(result)


@given(
    first=st.integers(min_value=1, max_value=9),
    second=st.integers(min_value=1, max_value=9),
)
@settings(max_examples=50, deadline=None)
def test_a_generated_partial_acceptance_leaves_the_other_deviation_pending(
    first: int, second: int
) -> None:
    """The named deviation clears while the retained one stays pending."""
    assume(first != second)
    entries = (
        f"- D{first}. Decision: rename the module. "
        "Date/Author: 2026-11-19, authoring agent (proposed; not approved).\n\n"
        f"- D{second}. Decision: replace the module. "
        "Date/Author: 2026-11-19, authoring agent (proposed; not approved).\n\n"
        f"- D10. Decision: approve D{second}; retain D{first} for separate review.\n"
        "  Rationale: only one proposal was approved.\n"
        "  Date/Author: 2026-11-20, policy owner.\n"
    )
    later = (
        f"\n- D11. Decision: accept D{first} as the approved resolution.\n"
        "  Rationale: the remaining proposal was approved.\n"
        "  Date/Author: 2026-11-21, policy owner.\n"
    )
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        partial = root / "partial.md"
        partial.write_text(
            f"Status: ACTIVE\n\n## Decision log\n\n{entries}", encoding="utf-8"
        )
        complete = root / "complete.md"
        complete.write_text(
            f"Status: COMPLETE\n\n## Decision log\n\n{entries}{later}",
            encoding="utf-8",
        )

        partial_result = _run("status", partial)
        complete_result = _run("status", complete)

    assert partial_result.returncode == 1, _diagnostics(partial_result)
    assert "ACTIVE with an unaccepted deviation" in partial_result.stdout, _diagnostics(
        partial_result
    )
    assert complete_result.returncode == 0, _diagnostics(complete_result)


_ACCEPTANCE_FORMS = ("named", "unrelated", "anaphoric", "hedged", "placeholder")


def _acceptance_entry(index: int, form: str, target: int) -> str:
    """Return one Decision log entry of the requested acceptance form."""
    if form == "named":
        decision = f"Decision: accept D{target} as the approved resolution."
        rationale = "  Rationale: the owner approved it.\n"
    elif form == "unrelated":
        decision = "Decision: accept the unrelated proposal."
        rationale = "  Rationale: the owner approved it.\n"
    elif form == "anaphoric":
        decision = "Decision: accept the deviation."
        rationale = "  Rationale: the owner approved it.\n"
    elif form == "hedged":
        decision = f"Decision: D{target} will be accepted."
        rationale = "  Rationale: the owner has not ruled yet.\n"
    else:
        decision = "Decision: record the outcome."
        rationale = (
            "  ```plaintext\n"
            "  - D-<next free>. Decision: <what was decided>.\n"
            "    Status: proposal pending acceptance.\n"
            "  ```\n"
        )
    return (
        f"- D{index}. {decision}\n"
        f"{rationale}  Date/Author: 2026-11-21, policy owner.\n\n"
    )


@given(
    actions=st.lists(
        st.tuples(
            st.sampled_from(_ACCEPTANCE_FORMS),
            st.integers(min_value=1, max_value=2),
        ),
        min_size=1,
        max_size=3,
    )
)
@settings(max_examples=50, deadline=None)
def test_a_generated_decision_log_clears_only_the_named_deviations(
    actions: list[tuple[str, int]],
) -> None:
    """Generated acceptance forms clear exactly the deviations they name."""
    pending = {1, 2}
    entries = (
        "- D1. Decision: rename the module. "
        "Date/Author: 2026-11-19, authoring agent (proposed; not approved).\n\n"
        "- D2. Decision: replace the module. "
        "Date/Author: 2026-11-19, authoring agent (proposed; not approved).\n\n"
    )
    for index, (form, target) in enumerate(actions, start=3):
        entries += _acceptance_entry(index, form, target)
        if form == "named":
            pending.discard(target)
        elif form == "anaphoric" and len(pending) == 1:
            pending.clear()
    with tempfile.TemporaryDirectory() as directory:
        record = _fixture(
            Path(directory),
            f"Status: ACTIVE\n\n## Decision log\n\n{entries}",
        )

        result = _run("status", record)

    message = "ACTIVE with an unaccepted deviation"
    assert (message in result.stdout) == bool(pending), _diagnostics(result)
    assert result.returncode == (1 if pending else 0), _diagnostics(result)
