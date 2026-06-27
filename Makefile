UV ?= uv
WITH ?= dev

# --- Code Quality Settings ---
SRC := src tests
PKG := src
COV_FAIL_UNDER := 75 # same values in pyproject.toml for pytest-cov, keep in sync
# -----------------------------

NOTEBOOKS_DIR := notebooks

# Variable to silence the SyntaxWarning from 3.12 (e.g., \d in docstrings)
PY_WARN_FILTER := PYTHONWARNINGS="ignore::SyntaxWarning"

# ---------------------------------------------
# Pretty help (auto-generates from '##' docs)
# ---------------------------------------------
# Disable color with: NO_COLOR=1 make help
ifeq ($(NO_COLOR),1)
	CYAN :=
	NC :=
else
	CYAN := \033[36m
	NC   := \033[0m
endif

define CLEAN
	@echo " Cleaning caches..."
	@find . -type d \( \
		-name '__pycache__' -o \
		-name '.mypy_cache' -o \
		-name '.pytest_cache' -o \
		-name '.ruff_cache' -o \
		-name '.ipynb_checkpoints' -o \
		-name '__marimo__' \
	\) -prune -exec rm -rf {} +
	@find . -type f \( -name '*.pyc' -o -name '*.pyo' -o -name '*.py[co]' \) -exec rm -f {} +
	@echo " All caches removed."
endef

.PHONY: help check-uv install install-dev install-hooks clean clean-all \
	jupyterlab check-imports pre-commit format lint test quality quality-fast \
	trivy-scan cli

# --- Pre-flight Checks ---

check-uv:
	@command -v $(UV) >/dev/null 2>&1 || { echo " Error: uv is not installed. Please install it first."; exit 1; }

# --- Pre-commit Hooks Management ---

install-hooks: check-uv ## Install git pre-commit and pre-push hooks
	@$(UV) run pre-commit install
	@$(UV) run pre-commit install --hook-type pre-push
	@echo " Git hooks installed successfully."

# --- Project Management ---

install: check-uv ## Install only main dependencies (lean: for CI compile/submit)
	@echo " Installing main dependencies only"
	@$(UV) sync --no-dev

install-dev: check-uv ## Install main + dev tools
	@echo " Installing main + dev + component groups"
	@$(UV) sync --group dev
# 	@$(UV) sync --group component-data --group component-ml

clean: ## Remove Python and tool caches (mypy, pytest, ruff, notebooks)
	@$(CLEAN)

clean-all: clean ## Remove all caches and .venv (Warning: Deactivate environment first)
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		echo "  Warning: Virtual environment is currently active."; \
		echo "Please run 'deactivate' in your terminal first, then run 'make clean-all' again."; \
		exit 1; \
	fi
	@if [ -d ".venv" ]; then \
		echo " Removing .venv..."; \
		rm -rf .venv; \
		echo " .venv removed."; \
	else \
		echo " No .venv directory to remove."; \
	fi

# --- Utilities ---

jupyterlab: check-uv ## Run Jupyter Lab on notebooks folder
	@$(UV) run jupyter lab $(NOTEBOOKS_DIR)

check-imports: check-uv ## Ensure package import works natively
	@$(UV) run python -c "import $(PKG); print(' Package $(PKG) imported successfully as a namespace package. Paths:', list($(PKG).__path__))"

# --- Code Quality Targets ---

pre-commit: check-uv ## Run all pre-commit hooks manually on all files
	@echo " Running all pre-commit checks..."
	@$(UV) run pre-commit run --all-files

format: check-uv ## Format code only
	@echo " Formatting code..."
	@$(UV) run ruff format $(SRC)

lint: check-uv ## Lint and apply safe autofixes
	@echo " Linting and fixing..."
	@$(UV) run ruff check --fix $(SRC)

test: check-uv ## Run unit tests and generate coverage report
	@echo " Running unit tests..."
	@$(UV) run pytest --cov=$(PKG) --cov-report=term-missing --cov-fail-under=$(COV_FAIL_UNDER)

sast: check-uv ## Run Semgrep static application security testing
	@echo " Running Semgrep security scan..."
	@$(UV) run semgrep scan --config auto --config semgrep.yml $(SRC)	

quality-fast: check-uv format lint ## Fast local validation
	@echo " Running fast quality checks..."
	@$(UV) run mypy $(SRC)

quality: check-uv format lint sast ## Full checks: type-check + sast + tests
	@echo "  Type checking..."
	@$(UV) run mypy $(SRC)
	@echo " Running unit tests..."
	@$(UV) run pytest --cov=$(PKG) --cov-report=term-missing --cov-fail-under=$(COV_FAIL_UNDER)	

# --- Local Execution & Entrypoints ---	

cli: ## Run the CLI to verify configuration and core setup
	@$(UV) run python -m src.entrypoints.cli verify-config

# --- Security & Auditing ---	

trivy-scan: ## Run Trivy vulnerability scanner on the project filesystem
	@echo "Running Trivy security scan..."
	docker run --rm \
	  -v $(PWD):/workspace \
	  aquasec/trivy fs \
	  --skip-dirs .venv \
	  --scanners vuln,config,secret \
	  --severity HIGH,CRITICAL \
	  --format table \
	  --output /workspace/trivy-report.txt \
	  /workspace
	@echo "Scan complete! Check trivy-report.txt for details."

help: ## Show this help
	@echo "Makefile commands:"
	@grep -E '^[a-zA-Z0-9_.-]+:.*## ' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'