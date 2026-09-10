"""Contract coverage for the shipped Agent Skills manifests."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SHIPPED_MANIFESTS = sorted((REPOSITORY_ROOT / "skills").glob("*/SKILL.md"))


def _run_make(
    target: str,
    *skill_dirs: Path,
    variables: tuple[str, ...] = (),
) -> subprocess.CompletedProcess[str]:
    """Run a Makefile manifest target over shipped skills or given fixtures."""
    arguments = ["make", target, *variables]
    if skill_dirs:
        directories = " ".join(f"{directory}/" for directory in skill_dirs)
        arguments.append(f"SKILL_DIRS={directories}")
    return subprocess.run(
        arguments,
        cwd=REPOSITORY_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def _run_manifest_check(
    skill_dir: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run the Makefile contract check for shipped skills or one fixture."""
    fixtures = [skill_dir] if skill_dir is not None else []
    return _run_make("skill-manifest-check", *fixtures)


def _frontmatter(manifest: Path) -> dict[str, object]:
    """Parse the YAML frontmatter block of a skill manifest."""
    lines = manifest.read_text(encoding="utf-8").splitlines()
    assert lines, f"{manifest} is empty"
    assert lines[0] == "---", f"{manifest} does not open with a frontmatter fence"
    closing = lines.index("---", 1)
    return yaml.safe_load("\n".join(lines[1:closing])) or {}


def _write_manifest(skill_dir: Path, body: str) -> Path:
    """Create a skill directory containing the given manifest text."""
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")
    return skill_dir


def _install_skill_creator(root: Path, log: Path) -> None:
    """Install a skill-creator fixture that records the skills it validates."""
    scripts = root / "scripts"
    scripts.mkdir(parents=True)
    (scripts / "quick_validate.py").write_text(
        f"import pathlib\nimport sys\n\n"
        f"log = pathlib.Path({str(log)!r})\n"
        f'with log.open("a", encoding="utf-8") as handle:\n'
        f'    handle.write("\\n".join(sys.argv[1:]) + "\\n")\n',
        encoding="utf-8",
    )


def test_shipped_skill_manifests_satisfy_the_contract() -> None:
    """Ensure every shipped skill passes YAML and schema validation."""
    result = _run_manifest_check()

    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    ("case", "frontmatter"),
    [
        ("missing", "description: A fixture that lacks the discovery name.\n"),
        ("empty", 'name: ""\ndescription: A fixture with an empty name.\n'),
    ],
)
def test_manifest_check_rejects_an_unusable_name(
    tmp_path: Path,
    case: str,
    frontmatter: str,
) -> None:
    """Reject a manifest whose discovery name is absent or empty.

    A strict loader cannot discover a skill without a usable discovery name.
    An absent ``name`` and an empty ``name`` fail discovery identically, so the
    contract must reject both rather than only the absent case.
    """
    skill_dir = _write_manifest(
        tmp_path / f"{case}-name",
        f"---\n{frontmatter}---\n\n# Fixture\n",
    )

    result = _run_manifest_check(skill_dir)

    assert result.returncode != 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    "manifest",
    SHIPPED_MANIFESTS,
    ids=lambda path: path.parent.name,
)
def test_shipped_metadata_values_are_strings(manifest: Path) -> None:
    """Reject the non-string metadata values that ``skills-ref`` coerces.

    ``skills_ref.parser`` rewrites every metadata value with ``str(v)``, so a
    YAML sequence survives validation but reaches consumers as a Python repr.
    The specification permits string keys and string values only, so reject the
    non-conformant shapes here rather than shipping a silently mangled value.
    """
    metadata = _frontmatter(manifest).get("metadata", {})

    assert isinstance(metadata, dict), (
        f"metadata must be a mapping, got {type(metadata).__name__}"
    )
    non_strings = {
        key: value for key, value in metadata.items() if not isinstance(value, str)
    }
    assert not non_strings, f"metadata values must be strings: {non_strings}"


def test_frontmatter_lint_reports_an_early_failure(tmp_path: Path) -> None:
    """Fail on an early malformed skill, not only a malformed final one.

    The shell ``for`` loop otherwise exits with the status of its last
    iteration, letting a conformant trailing skill mask a malformed earlier
    one.
    """
    broken = _write_manifest(
        tmp_path / "a-broken",
        "---\nname: [unclosed\n---\n\n# Broken\n",
    )
    valid = _write_manifest(
        tmp_path / "z-valid",
        "---\nname: z-valid\n"
        "description: A conformant trailing fixture.\n"
        "---\n\n# Valid\n",
    )

    result = _run_make("skill-frontmatter-lint", broken, valid)

    assert result.returncode != 0, result.stdout + result.stderr


def test_lint_runs_the_manifest_contract(tmp_path: Path) -> None:
    """Fail ``make lint`` on a malformed manifest, proving the wiring holds.

    The contract is only enforced because ``lint`` depends on
    ``skill-manifest-check``; without this test, dropping that prerequisite
    would silently disable manifest validation while every other test still
    passed. ``CHANGED_MARKDOWN`` is cleared so that ``nixie`` cannot fail on
    an unrelated changed diagram and mask the manifest failure.
    """
    skill_dir = _write_manifest(
        tmp_path / "unlintable",
        "---\n"
        "description: A fixture that lacks the required discovery name.\n"
        "---\n\n# Fixture\n",
    )

    result = _run_make("lint", skill_dir, variables=("CHANGED_MARKDOWN=",))

    assert result.returncode != 0, result.stdout + result.stderr


def test_frontmatter_lint_reports_an_unreadable_manifest(tmp_path: Path) -> None:
    """Fail on a manifest that cannot be read rather than skipping it.

    ``awk`` fails to read a missing ``SKILL.md``, a distinct failure path from
    ``yamllint`` rejecting parsed content, and one that only ``pipefail``
    surfaces.
    """
    absent = tmp_path / "absent"
    absent.mkdir()
    valid = _write_manifest(
        tmp_path / "z-valid",
        "---\nname: z-valid\n"
        "description: A conformant trailing fixture.\n"
        "---\n\n# Valid\n",
    )

    result = _run_make("skill-frontmatter-lint", absent, valid)

    assert result.returncode != 0, result.stdout + result.stderr


def test_typecheck_skips_an_absent_skill_creator(tmp_path: Path) -> None:
    """Skip the skill-creator check rather than failing without the tool.

    ``quick_validate.py`` ships with the Codex skill-creator, which is not
    installed on every host and moved between Codex home layouts. Failing the
    ``typecheck`` gate there would block every commit for a reason unrelated
    to the change under test, so the target warns and continues. The check
    runs through ``typecheck`` because that is the gate a contributor runs.
    """
    absent = tmp_path / "absent-skill-creator"

    result = _run_make("typecheck", variables=(f"SKILL_CREATOR={absent}",))

    assert result.returncode == 0, result.stdout + result.stderr
    assert "skipping quick_validate.py" in result.stdout


@pytest.mark.parametrize("layout", ["CODEX_HOME", "HOME"])
def test_typecheck_uses_each_skill_creator_layout(
    tmp_path: Path,
    layout: str,
) -> None:
    """Validate every changed skill from either supported Codex layout.

    Candidate one is ``$CODEX_HOME/skills/.system/skill-creator`` and candidate
    two is ``$HOME/.agents/skills/.system/skill-creator``. Either layout must
    be able to supply the tool on its own, so a host that uses only one of them
    validates each changed skill instead of silently skipping the check.
    """
    codex_home = tmp_path / "codex-home"
    home = tmp_path / "home"
    relative = Path("skills/.system/skill-creator")
    if layout == "HOME":
        relative = Path(".agents") / relative
    log = tmp_path / "validated.log"
    _install_skill_creator(
        (codex_home if layout == "CODEX_HOME" else home) / relative,
        log,
    )

    result = _run_make(
        "typecheck",
        variables=(
            f"HOME={home}",
            f"CODEX_HOME={codex_home}",
            "CHANGED_SKILLS=skills/changelog skills/commit-message",
        ),
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert log.read_text(encoding="utf-8").split() == [
        "skills/changelog",
        "skills/commit-message",
    ]
