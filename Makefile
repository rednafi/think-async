path := .

.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: lint
lint: black isort flake mypy	## Apply all the linters


.PHONY: lint-check
lint-check:
	@echo
	@echo "Checking linter rules..."
	@echo "========================"
	@echo
	@black --check $(path)
	@isort --check $(path)
	@flake8 $(path)


.PHONY: black
black: ## Apply black
	@echo
	@echo "Applying black..."
	@echo "================="
	@echo
	@ # --fast was added to circumnavigate a black bug
	@black --fast $(path)
	@echo


.PHONY: isort
isort: ## Apply isort
	@echo "Applying isort..."
	@echo "================="
	@echo
	@isort $(path)


.PHONY: flake
flake: ## Apply flake8
	@echo
	@echo "Applying flake8..."
	@echo "================="
	@echo
	@flake8 $(path)


.PHONY: mypy
mypy: ## Apply mypy
	@echo
	@echo "Applying mypy..."
	@echo "================="
	@echo
	@mypy $(path)


.PHONY: trim-imports
trim-imports: ## Remove unused imports
	@autoflake --remove-all-unused-imports \
	--ignore-init-module-imports \
	--in-place \
	--recursive \
	$(path)


.PHONY: dep-lock
dep-lock: ## Freeze deps in 'requirements.txt' file.
	@pip-compile requirements.in -o requirements.txt --no-emit-options
	@pip-compile requirements-dev.in -o requirements-dev.txt --no-emit-options

.PHONY: dep-sync
dep-sync: ## Sync venv installation with `requirements.txt`
	@pip-sync


.PHONY: test
test: ## Run the tests with pytest.
	@export PYTHONWARNINGS="ignore" && pytest -v


.PHONY: install-deps
install-deps: ## Install the dependencies.
	@pip install -r requirements.txt && \
	pip install -r requirements-dev.txt
