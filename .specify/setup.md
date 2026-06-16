# Spec-Kit Setup

This repository is configured for Spec-Kit spec-driven development.

## What is included
- `constitution.md` for project spec rules
- `.specify/README.md` for spec guidance
- `.specify/templates/feature-spec-template.md` for new feature specs
- `specs/` directory for tracked feature specification files

## How to use it
1. Copy the template: `.specify/templates/feature-spec-template.md`
2. Rename it to `specs/BCCA-FEAT-XXX-short-title.md`
3. Fill in the feature details and acceptance criteria
4. Commit the file as part of the feature delivery

## Optional tooling
- If you want to enable Spec-Kit CLI tooling, run:

```powershell
npx @github/spec-kit init
```

- If the package is unavailable in npm, continue using the tracked `.specify/` templates and `specs/` folders manually.
