# Blueprint Roadmap & Technical Debt

This document tracks upcoming architectural patterns, infrastructure enhancements, and automated security upgrades for this project skeleton.

**Priority Scale:**
- **[P1]** High impact / Essential foundation.
- **[P2]** Medium impact / Architectural evolution.
- **[P3]** DevSecOps maturity / Day-2 operations.

---

## 🚧 Pending Architectural Evolution

- **[P1] Database Engine & Migration Toolkit Integration**
  - **Context:** Establish the default Object-Relational Mapping (ORM) and migration tracks.
  - **Action Items:** Choose database driver, re-integrate `sqlfluff` with the specific SQL dialect, and configure `alembic` for database versioning.

- **[P2] Resource Exhaustion & Concurrency Controls (Rate Limiting)**
  - **Context:** Protect entrypoints from Denial of Service (DoS) attacks and traffic spikes.
  - **Action Items:** Implement token-bucket rate-limiting middleware or asynchronous message queuing patterns (e.g., Celery/RabbitMQ or AWS SQS).

## 🔒 Security & CI/CD Enhancements

- **[P1] Service-to-Service (S2S) Authentication**
  - **Context:** Enforce Zero-Trust network communication between internal microservices.
  - **Action Items:** Implement static API Key verification or short-lived asymmetric JWT token validation hooks.

- **[P2] Security Headers & Environment Hardening**
  - **Context:** Reduce the application's attack surface in production (OWASP Top 10).
  - **Action Items:** Strip technology-revealing headers (e.g., `Server: uvicorn`) and enforce mandatory HTTP security headers (HSTS, CSP, X-Content-Type-Options) via framework middleware.

- **[P3] CI Pipeline Vulnerability Gate (Trivy)**
  - **Context:** Block vulnerable supply-chain code or container base layers from moving to production registries.
  - **Action Items:** Embed `trivy fs` and `trivy image` scans inside GitHub Actions / GitLab CI, failing builds automatically on `CRITICAL` vulnerability thresholds.