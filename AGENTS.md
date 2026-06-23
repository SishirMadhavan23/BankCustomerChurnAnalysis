# AGENTS.md

## Overview

This document describes the coding agents and automated tools used in this repository.

## Automated Agents

### CI/CD Pipeline
- GitHub Actions workflow (`.github/workflows/ci.yml`)
- Runs on: push to main/develop, pull requests, version tags
- Jobs:
  - Test (Python 3.10, 3.11)
  - Lint (Ruff, Pylint, Flake8, Pyupgrade, Vulture)
  - Format check (Ruff, Pyupgrade)
  - Type check (Mypy)
  - Security scan (Bandit, Semgrep, Gitleaks, TruffleHog)
  - Dependency audit (pip-audit)
  - Coverage report
  - Changelog generation (git-cliff)
  - Release automation

### Pre-commit Hooks
- Configured in `.pre-commit-config.yaml`
- Includes: Ruff, Black, isort, mypy, bandit, trailing whitespace, end-of-file fixes

### Code Quality Agents
- **Ruff**: Fast Python linter and formatter
- **Mypy**: Static type checker
- **Pylint**: Code analysis and quality checker
- **Flake8**: Style guide enforcement
- **Bandit**: Security linting
- **Semgrep**: Static analysis for security and code patterns
- **Vulture**: Dead code detection

### Dependency Management
- **pip-audit**: Vulnerability scanning for Python dependencies
- **pip-upgrader**: Automated dependency updates
- **pipdeptree**: Dependency tree visualization

## Local Development

```bash
# Install pre-commit hooks
pre-commit install

# Run all quality checks
ruff check app/ tests/
ruff format --check app/
mypy app/
pylint app/ --fail-under=7.0
flake8 app/ --max-line-length=100
bandit -r app/ -x tests
vulture app/ --min-confidence 80
```

## Branch Protection

- `main` branch requires:
  - All CI checks passing
  - At least 1 review approval
  - No merge conflicts

- `develop` branch:
  - All CI checks passing

## Issue Templates

- Bug reports
- Feature requests
- Documentation improvements
- Security vulnerabilities

## Security Policy

See [SECURITY.md](SECURITY.md) for responsible disclosure process.