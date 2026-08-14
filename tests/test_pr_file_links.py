"""Semantic coverage for pull-request description file-link guidance."""

from __future__ import annotations

import dataclasses as dc
import re
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = REPOSITORY_ROOT / "skills/pr-creation/SKILL.md"
BRANCH_REF = "fix/file-link-rules"
COMMIT_SHA = "a1b2c3d4e5f678901234567890abcdef12345678"
_MARKDOWN_LINK = re.compile(r"^\[[^\]]+\]\((?P<url>https://[^)]+)\)$")
_COMMIT_LINK = re.compile(r"/blob/[0-9a-f]{7,40}/")
_LINE_ANCHOR = re.compile(r"#L\d+(?:-L\d+)?$")


@dc.dataclass(frozen=True)
class _FileLinkCase:
    """Describe one permitted or rejected pull-request file link."""

    name: str
    description_fragment: str
    exact_commit_issue_reference: bool
    allowed: bool


def _file_link_is_allowed(
    description_fragment: str,
    *,
    exact_commit_issue_reference: bool,
) -> bool:
    """Return whether one description fragment follows the file-link contract."""
    match = _MARKDOWN_LINK.fullmatch(description_fragment)
    if match is None:
        return False
    url = match.group("url")
    branch_prefix = f"https://github.com/OWNER/REPO/blob/{BRANCH_REF}/"
    if url.startswith(branch_prefix):
        return _LINE_ANCHOR.search(url) is not None
    return (
        exact_commit_issue_reference
        and _COMMIT_LINK.search(url) is not None
        and _LINE_ANCHOR.search(url) is not None
    )


def _file_link_guidance() -> str:
    """Return the File links section from the canonical pull-request skill."""
    skill_text = SKILL_PATH.read_text(encoding="utf-8")
    match = re.search(
        r"^## File links\n(?P<section>.*?)(?=^## )",
        skill_text,
        re.DOTALL | re.MULTILINE,
    )
    if match is None:
        msg = "The pull-request skill must contain a File links section"
        raise AssertionError(msg)
    return match.group("section")


def test_file_link_guidance_requires_the_documented_contract() -> None:
    """Ensure the canonical guidance retains each rule under test."""
    guidance = _file_link_guidance()

    assert "not bare paths" in guidance, "guidance must reject bare file paths"
    assert "GFM line anchor" in guidance, "guidance must require line anchors"
    assert "branch ref" in guidance, "guidance must require branch refs"
    assert "specific commit SHA only" in guidance, (
        "guidance must limit commit SHA links to exact-commit issue references"
    )


FILE_LINK_CASES = [
    _FileLinkCase(
        name="branch-anchor",
        description_fragment=(
            "[guide](https://github.com/OWNER/REPO/blob/"
            "fix/file-link-rules/docs/guide.md#L12-L18)"
        ),
        exact_commit_issue_reference=False,
        allowed=True,
    ),
    _FileLinkCase(
        name="bare",
        description_fragment="docs/guide.md",
        exact_commit_issue_reference=False,
        allowed=False,
    ),
    _FileLinkCase(
        name="anchorless",
        description_fragment=(
            "[guide](https://github.com/OWNER/REPO/blob/"
            "fix/file-link-rules/docs/guide.md)"
        ),
        exact_commit_issue_reference=False,
        allowed=False,
    ),
    _FileLinkCase(
        name="commit-without-issue",
        description_fragment=(
            f"[guide](https://github.com/OWNER/REPO/blob/{COMMIT_SHA}/docs/guide.md#L12)"
        ),
        exact_commit_issue_reference=False,
        allowed=False,
    ),
    _FileLinkCase(
        name="commit-issue",
        description_fragment=(
            f"[issue](https://github.com/OWNER/REPO/blob/{COMMIT_SHA}/docs/guide.md#L12)"
        ),
        exact_commit_issue_reference=True,
        allowed=True,
    ),
]


@pytest.mark.parametrize("case", FILE_LINK_CASES, ids=lambda case: case.name)
def test_file_link_rules(case: _FileLinkCase) -> None:
    """Verify branch, anchor, and exact-commit exception semantics."""
    assert (
        _file_link_is_allowed(
            case.description_fragment,
            exact_commit_issue_reference=case.exact_commit_issue_reference,
        )
        is case.allowed
    ), "file-link rule must match its documented exception context"
