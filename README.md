# Python Clean Architecture Boilerplate

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Security: Trivy](https://img.shields.io/badge/security-Trivy-blueviolet)](https://aquasecurity.github.io/trivy/)
[![Architecture: Clean](https://img.shields.io/badge/Architecture-Clean%20Architecture-success)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
[![Build Status](https://github.com/TU_USUARIO/python-clean-architecture-boilerplate/actions/workflows/ci.yml/badge.svg)](https://github.com/TU_USUARIO/python-clean-architecture-boilerplate/actions)

A production-ready enterprise skeleton for high-performance Python applications...

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
│   │   └── metadata.py          # Immutable application metadata
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
- Docker
- make

## 🚀 Local Setup & Quickstart

Follow these steps in order to set up your local development environment and activate automated security gates.

### 1. Environment Configuration
The application uses a strict fail-fast configuration model. Create your local environment file:
```bash
cp .env.example .env
# Open .env and adjust your local DATABASE_URL if necessary
```

### 2. Dependency & Git Hooks Installation
Instead of running loose commands, use the provided infrastructure shortcuts to sync your environment and arm your local Git security guards in one go:
```bash
# Step A: Install the project and all development tools using uv
make install-dev

# Step B: MANDATORY - Activate local pre-commit & pre-push security hooks
make install-hooks
```
> ⚠️ **CRITICAL SECURITY NOTE:** If you skip running make install-hooks, your local Git commits will NOT be audited by Gitleaks, Semgrep, or Ruff. Always ensure hooks are armed before writing any code to prevent leaking credentials or pushing architectural debt to remote branches.

### 3. 🧪 Verifying the Setup
To ensure your chassis is fully operational and all quality gates are working perfectly, run the global health check command:
```bash
make quality
```
If everything returns in green, your environment is completely secured and ready for development.

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