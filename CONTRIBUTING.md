# Contributing to Bank Customer Churn Analysis

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/<your-username>/bank-customer-churn-analysis.git
   cd bank-customer-churn-analysis
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Install development tools:
   ```bash
   pip install ruff mypy pylint flake8 bandit pytest pytest-cov
   ```

## Code Quality

Before committing, please run:

```bash
# Lint with Ruff
ruff check app/ tests/

# Format check
ruff format --check app/

# Type check
mypy app/

# Security scan
bandit -r app/ -x tests

# Tests
pytest tests/ --cov=app --cov-report=term
```

## Commit Convention

- Use clear, descriptive messages
- Reference issue numbers where applicable

## Pull Request Process

1. Update documentation if needed
2. Ensure all checks pass
3. Create a pull request with a clear description

Thank you for contributing!