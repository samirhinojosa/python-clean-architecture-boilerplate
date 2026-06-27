# Python Clean Architecture Boilerplate

A production-ready enterprise skeleton for high-performance Python applications. Designed strictly under Clean Architecture (Ports & Adapters) and Domain-Driven Design (DDD) principles, this boilerplate provides a fully containerized, type-safe, and secure foundation to eliminate day-zero technical debt.

## Architecture & Design

This repository adheres to Clean Architecture (Ports & Adapters) to remain cloud-agnostic, testable, and easy to refactor.<br/> Each layer has a single responsibility:

- `src/adapters/`: Concrete implementations of ports (Infrastructure, specific databases, external HTTP clients).
- `src/core/`: Global application utilities and shared mechanics (e.g., configuration settings, logging setup, error handling).
- `src/domain/`: Pure enterprise entities, value objects, domain logic, and states. Completely free of external framework dependencies.
- `src/entrypoints/`: Triggers and process starters (FastAPI, CLI, queue consumers, cron batch jobs).
- `src/interfaces/`: Abstract contracts (ports) driving database, storage, and external service definitions.
- `src/pipelines/`: Orchestration recipes (use cases) coordinating domain interactions, data streams, and ports.

### 📁 Project Structure

```text
.
├── docker/                      # Local dev infrastructure (docker-compose, scripts)
├── src/
│   ├── adapters/                # EXTERNAL IMPLEMENTATIONS (database_repositories, client_extensions)
│   ├── core/                    # FOUNDATIONS
│   │   ├── config/              # Dynamic settings & structlog setup
│   │   └── constants.py         # Immutable application metadata
│   ├── domain/                  # PURE BUSINESS LÓGICA (Entities, Value Objects)
│   ├── entrypoints/             # TRIGGERS (api, jobs, cli.py)
│   ├── interfaces/              # THE PORTS (Abstract contracts)
│   └── pipelines/               # ORCHESTRATION (Use cases / Recipes)
├── tests/                       # Pytest suite
├── .env.example                 # Configuration contract template
├── .gitattributes
├── .gitignore
├── .pre-commit-config.yaml      # Git hooks configuration (Ruff, Mypy, Semgrep, etc.)
├── .python-version
├── LICENSE.md
├── Makefile
├── pyproject.toml
├── README.md
├── ROADMAP.md                   # Technical debt and blueprint enhancements tracking
├── semgrep.yml                  # Custom SAST rules to enforce Clean Architecture
└── uv.lock
```

## 📋 Prerequisites

- Python `>=3.12,<3.13` (recommended)
- UV `0.11.x`
- Git LFS required for tracking model weights in the `models/` directory
- Docker
- make

## Local Setup & Installation

1. Setup the local environment variables. The application uses a strict fail-fast configuration model.
```bash
cp .env.example .env
# Edit .env with your local credentials if necessary
```

2. Create a `uv` virtual environment (example) with all packages :

```bash
# For development
uv sync

# For production
uv sync --no-dev
```

### ☁️ Configuration & Auto-Cloud Detection

This project strictly adheres to the **12-Factor App methodology**, eliminating the need for a `.env.prod` file entirely.

The configuration layer (`src/core/config/settings.py`) automatically detects the runtime environment by inspecting OS variables injected by the infrastructure (e.g., `AWS_EXECUTION_ENV` for **AWS**, or `KUBERNETES_SERVICE_HOST` for **K8s/GCP**).

---

#### 🚀 Automated Cloud Behaviors
When a cloud environment is detected, the application dynamically triggers the following mechanisms:

* **Structured Logging:** Switches output to strict **JSON (`structlog`)** optimized for cloud indexers (CloudWatch, Google Cloud Logging).
* **Path Resolution:** Re-anchors the root execution path strictly to `/app` (Docker standard).
* **Secret Isolation:** Ignores local `.env` files entirely, relying purely on native infrastructure secret injection.

### 🔒 Git Hooks & Code Quality

This project strictly enforces Clean Architecture and code quality via Git hooks. 

After running `make install-dev`, you must run `make install-hooks`. Once installed:
- **On `git commit`:** Fast formatting (Ruff), architecture rules (Semgrep), and automated secret detection (Gitleaks) are executed. The commit will be blocked if you import Adapters into the Domain layer, or if you accidentally hardcode sensitive credentials (API keys, AWS tokens).
- **On `git push`:** Heavier checks (mypy, bandit, pip-audit, tests) will run to ensure remote branch integrity.

## 🛠️ Development commands

Use these `make` commands for common development tasks:

| Command | Description |
|---------|-------------|
| `make install` | Install only main production dependencies (runs `uv sync --no-dev` for clean CI/CD builds) |
| `make install-dev` | Install main dependencies + all development tools (runs `uv sync`) |
| `make install-hooks` | Install Git pre-commit and pre-push hooks (required for local development) |
| `make test` | Run pytest suite with coverage report |
| `make sast` | Run Semgrep static application security and architecture testing |
| `make quality` | Run linting, SAST, type checking, and code quality checks |
| `make clean` | Remove Python caches (.pytest_cache, .mypy_cache, __pycache__, etc.) |
| `make trivy-scan` | Run Trivy via Docker to scan for IaC misconfigurations and OS/dependency vulnerabilities |

### ⚙️ Viewing available commands
You can run make help to see all available commands, which act as shortcuts for common or repetitive tasks.
```bash
make help
```

## Code Standards

As you write clean code Python, ensure strict adherence to docstring requirements:

```python
from typing import Any

def execute_use_case(payload: dict[str, Any]) -> bool:
    """
    A concise summary of the function/method purpose.

    Args:
        payload (dict[str, Any]): Description of the incoming data structure.

    Returns:
        bool: True if the operation succeeded, False otherwise.

    Raises:
        ValueError: Description of conditions under which this error is raised.
    """
    # Business logic implementation here
    return True
```

## 🗺️ Roadmap & Technical Debt
For planned features, pending architectural decisions (like database selection), and technical debt, please refer to the [ROADMAP.md](ROADMAP.md).