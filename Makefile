# Makefile for current library.

# Global variables.
PROJECT_NAME = project_template
PYTHON_INTERPRETER = python3
CHECK_DIRS := tests project_template *.py

.PHONY: clean-build
clean-build: ## Remove build artifacts.
	@echo "+ $@"
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

.PHONY: clean-pyc
clean-pyc: ## Remove Python file artifacts.
	@echo "+ $@"
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name '*.py[co]' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

.PHONY: docs
docs: ## Rebuild docs automatically and display locally.
	mkdocs serve --config-file docs/mkdocs.yml

.PHONY: servedocs
servedocs: ## Rebuild docs automatically and push to github.
	mkdocs gh-deploy --config-file docs/mkdocs.yml

.PHONY: help
help: ## Display make help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'