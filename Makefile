SHELL := /usr/bin/env
.SHELLFLAGS := bash -c

CODEX_HOME ?= $(HOME)/.codex
SKILL_CREATOR_CANDIDATES := \
    $(CODEX_HOME)/skills/.system/skill-creator \
    $(HOME)/.agents/skills/.system/skill-creator
SKILL_CREATOR ?= $(firstword $(wildcard $(SKILL_CREATOR_CANDIDATES)))
QUICK_VALIDATE := $(SKILL_CREATOR)/scripts/quick_validate.py
DIFF_BASE ?= origin/main
CHANGED_MARKDOWN := $(sort $(shell \
	{ git diff --name-only --diff-filter=ACMRT "$(DIFF_BASE)"...HEAD -- '*.md'; \
	  git diff --name-only --diff-filter=ACMRT -- '*.md'; } | sort -u))
CHANGED_SKILLS := $(sort $(shell \
	{ git diff --name-only --diff-filter=ACMRT "$(DIFF_BASE)"...HEAD -- 'skills/*'; \
	  git diff --name-only --diff-filter=ACMRT -- 'skills/*'; } \
	| awk -F/ 'NF >= 3 { print $$1 "/" $$2 }' | sort -u))

SKILL_DIRS ?= $(sort $(dir $(wildcard skills/*/SKILL.md)))
SKILLS_REF := uv run --group dev skills-ref
YAMLLINT := uv run --group dev yamllint
SKILL_YAMLLINT_CONFIG := {extends: default, rules: {line-length: disable}}

PYTHON_TESTS := tests

# `make fmt` and `make check-fmt` call mdtablefix directly. `--git` selects the
# Markdown files Git tracks and `--include-untracked` adds the untracked files
# Git does not ignore, so a new document is formatted before it is staged.
# Both modes need mdtablefix 0.6.1 or later.
MDLINT ?= markdownlint-cli2
MDTABLEFIX ?= mdtablefix
MDTABLEFIX_SELECT = --git --include-untracked
MDTABLEFIX_RULES = --wrap --renumber --breaks --ellipsis --fences

.PHONY: markdownlint nixie check-fmt lint skill-frontmatter-lint skill-manifest-validate skill-manifest-check skill-creator-validate typecheck test fmt

markdownlint:
	@if [ -n "$(CHANGED_MARKDOWN)" ]; then \
		markdownlint-cli2 $(CHANGED_MARKDOWN); \
	else \
		echo "No changed Markdown files to lint."; \
	fi

nixie:
	@if [ -n "$(CHANGED_MARKDOWN)" ]; then \
		nixie $(CHANGED_MARKDOWN); \
	else \
		echo "No changed Markdown files to validate with nixie."; \
	fi

check-fmt:
	git diff --check
	uv run --group dev ruff format --check $(PYTHON_TESTS)
	$(MAKE) markdownlint
	$(MDTABLEFIX) --check $(MDTABLEFIX_SELECT) $(MDTABLEFIX_RULES)

lint: nixie skill-manifest-check
	uv run --group dev ruff check $(PYTHON_TESTS)
	uv run --group dev interrogate --fail-under 100 $(PYTHON_TESTS)

skill-frontmatter-lint:
	@set -euo pipefail; for skill_dir in $(SKILL_DIRS); do \
		skill_file="$${skill_dir%/}/SKILL.md"; \
		echo "yamllint $$skill_file frontmatter"; \
		awk 'NR == 1 { if ($$0 != "---") exit 1; print; next } $$0 == "---" { found = 1; print; exit } { print } END { if (!found) exit 1 }' "$$skill_file" | $(YAMLLINT) -d '$(SKILL_YAMLLINT_CONFIG)' -; \
	done

skill-manifest-validate:
	@set -eu; for skill_dir in $(SKILL_DIRS); do \
		echo "skills-ref validate $$skill_dir"; \
		$(SKILLS_REF) validate "$$skill_dir"; \
	done

skill-manifest-check: skill-frontmatter-lint skill-manifest-validate

typecheck: skill-creator-validate
	uv run --group dev ty check $(PYTHON_TESTS)

skill-creator-validate:
	@set -eu; \
	if [ ! -f "$(QUICK_VALIDATE)" ]; then \
		echo "WARNING: skill-creator not found; skipping quick_validate.py."; \
		echo "Searched: $(SKILL_CREATOR_CANDIDATES)"; \
		echo "Set SKILL_CREATOR=<skill-creator directory> to run it."; \
		exit 0; \
	fi; \
	if [ -z "$(CHANGED_SKILLS)" ]; then \
		echo "No changed skills to validate."; \
		exit 0; \
	fi; \
	for skill in $(CHANGED_SKILLS); do \
		echo "quick_validate $$skill"; \
		uv run --with pyyaml python "$(QUICK_VALIDATE)" "$$skill"; \
	done

test: typecheck
	uv run --group dev pytest -v $(PYTHON_TESTS)

fmt: ## Format Markdown sources
	$(MDTABLEFIX) --in-place $(MDTABLEFIX_SELECT) $(MDTABLEFIX_RULES)
	$(MDLINT) --fix "**/*.md"
