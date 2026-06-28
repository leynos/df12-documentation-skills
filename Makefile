DIFF_BASE ?= origin/main

.PHONY: markdownlint nixie

markdownlint:
	@files="$$(git diff --name-only --diff-filter=ACMRT "$(DIFF_BASE)"...HEAD -- '*.md')"; \
	if [ -n "$$files" ]; then \
		markdownlint-cli2 $$files; \
	else \
		echo "No changed Markdown files to lint."; \
	fi

nixie:
	@files="$$(git diff --name-only --diff-filter=ACMRT "$(DIFF_BASE)"...HEAD -- '*.md')"; \
	if [ -n "$$files" ]; then \
		nixie $$files; \
	else \
		echo "No changed Markdown files to validate with nixie."; \
	fi
