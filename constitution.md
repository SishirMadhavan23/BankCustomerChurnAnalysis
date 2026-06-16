# Spec-Kit Constitution

## Purpose
This repository uses Spec-Kit to make product and engineering decisions explicit, traceable, and reviewable in the form of feature specifications.

## Scope
- Feature specs live in `specs/`
- Spec scaffolding and templates live in `.specify/`
- At least one tracked spec must exist for each new feature or major change

## Principles
- Write specs before implementation whenever possible
- Keep acceptance criteria concrete and testable
- Use behavior-focused stakeholder language
- Link specs to issue or feature identifiers when applicable

## Spec Naming
Feature spec files should use the pattern:
- `BCCA-FEAT-XXX-short-title.md`

Where `XXX` is a sequential feature ID.

## Spec Structure
Each feature spec should include:
- Title
- Summary
- Motivation
- Stakeholders
- Acceptance Criteria
- Success Metrics
- Implementation Notes
- Non-Goals
- Related Docs / References

## Review Pattern
- Add new specs in `specs/`
- Keep `.specify/` templates and guidance under source control
- Update specs as requirements evolve

## Templates
Use `.specify/templates/feature-spec-template.md` as the canonical template for new feature specifications.
