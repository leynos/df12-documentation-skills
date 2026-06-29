SKILL_CREATOR ?= $(HOME)/.codex/skills/.system/skill-creator
DIFF_BASE ?= origin/main
CHANGED_MARKDOWN := $(sort $(shell \
	{ git diff --name-only --diff-filter=ACMRT "$(DIFF_BASE)"...HEAD -- '*.md'; \
	  git diff --name-only --diff-filter=ACMRT -- '*.md'; } | sort -u))
CHANGED_SKILLS := $(sort $(shell \
	{ git diff --name-only --diff-filter=ACMRT "$(DIFF_BASE)"...HEAD -- 'skills/*'; \
	  git diff --name-only --diff-filter=ACMRT -- 'skills/*'; } \
	| awk -F/ 'NF >= 3 { print $$1 "/" $$2 }' | sort -u))

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
	$(MAKE) markdownlint

lint: nixie

typecheck:
	@if [ -z "$(CHANGED_SKILLS)" ]; then \
		echo "No changed skills to validate."; \
	fi
	@for skill in $(CHANGED_SKILLS); do \
		uv run --with pyyaml python \
			"$(SKILL_CREATOR)/scripts/quick_validate.py" "$$skill"; \
	done

test: typecheck
