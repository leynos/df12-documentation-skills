CODEX_HOME ?= $(HOME)/.codex
SKILL_CREATOR ?= $(CODEX_HOME)/skills/.system/skill-creator
DIFF_BASE ?= origin/main
CHANGED_MARKDOWN := $(sort $(shell \
	{ git diff --name-only --diff-filter=ACMRT "$(DIFF_BASE)"...HEAD -- '*.md'; \
	  git diff --name-only --diff-filter=ACMRT -- '*.md'; } | sort -u))
CHANGED_SKILLS := $(sort $(shell \
	{ git diff --name-only --diff-filter=ACMRT "$(DIFF_BASE)"...HEAD -- 'skills/*'; \
	  git diff --name-only --diff-filter=ACMRT -- 'skills/*'; } \
	| awk -F/ 'NF >= 3 { print $$1 "/" $$2 }' | sort -u))

PYTHON_TESTS := tests

.PHONY: markdownlint nixie check-fmt lint typecheck test

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

lint: nixie
	uv run --group dev ruff check $(PYTHON_TESTS)
	uv run --group dev interrogate --fail-under 100 $(PYTHON_TESTS)

typecheck:
	@if [ -z "$(CHANGED_SKILLS)" ]; then \
		echo "No changed skills to validate."; \
	fi
	@for skill in $(CHANGED_SKILLS); do \
		uv run --with pyyaml python \
			"$(SKILL_CREATOR)/scripts/quick_validate.py" "$$skill"; \
	done
	uv run --group dev ty check $(PYTHON_TESTS)

test: typecheck
	uv run --group dev pytest -v $(PYTHON_TESTS)
