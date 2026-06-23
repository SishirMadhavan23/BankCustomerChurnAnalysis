# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of Bank Customer Churn Analysis seriously. If you have discovered a security vulnerability, please follow these steps:

1. **Do not** open a public GitHub issue for security vulnerabilities.
2. Send an email to [bcca-security@example.com](mailto:bcca-security@example.com) with:
   - A description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact assessment
   - Suggested fixes (if any)

3. We will acknowledge your email within 3 business days.
4. We will provide a detailed response within 7 business days outlining our plan to address the issue.
5. We will keep you informed of the progress and credit you for the discovery (unless you prefer anonymity).

## Security Best Practices

When contributing to this project:

- Never commit secrets, API keys, or credentials to the repository
- Use environment variables for sensitive configuration
- Report security issues in private, not in public forums
- Keep dependencies up to date
- Follow secure coding practices

## Automated Security Checks

This repository includes automated security scanning:
- Bandit for Python security linting
- Semgrep for static analysis
- Gitleaks for secret scanning
- TruffleHog for comprehensive secret detection
- pip-audit for dependency vulnerability scanning

## Disclosure Policy

- We request 90 days to address reported vulnerabilities before public disclosure
- Coordinated disclosure is preferred
- We appreciate responsible security researchers

Thank you for helping keep this project and our users safe!