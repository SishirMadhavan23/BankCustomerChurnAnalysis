# Contributing to Bank Customer Churn Analysis

We love your input! We want to make contributing to this project as easy and transparent as possible.

## Development Process

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Code of Conduct

Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details on our code of conduct.

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/bank-customer-churn-analysis.git
cd bank-customer-churn-analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train the model
python -m app.model

# Run the app
python -m app.app
```

## Code Style

- Use [Ruff](https://github.com/astral-sh/ruff) for Python linting
- Follow PEP 8 conventions
- Use type hints for all function signatures
- Write descriptive docstrings in Google-style format

## Testing

- Write tests using pytest
- Aim for 80%+ code coverage
- Run tests with: `pytest tests/`

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the CHANGELOG.md with any notable changes
3. The PR will be merged once you have the sign-off of maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.