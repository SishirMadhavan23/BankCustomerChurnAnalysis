# Specification Constitution

Project: Bank Customer Churn Analysis (BCCA)

Purpose: Establish minimal Spec-Kit conventions for spec-driven development in this repo.

Scope:
- All new features and public API changes should include a spec under `specs/`.
- Specs should reference templates stored in `.specify/templates/`.

Owners:
- Product: Product Owner
- Engineering: Repo maintainers

Definition of Done for a spec:
- `spec.md` describing behavior and acceptance criteria
- `plan.md` outlining milestones and timeline
- `tasks.md` listing implementation tasks and owners

Templates: `.specify/templates/spec-template.md`, `.specify/templates/plan-template.md`, `.specify/templates/tasks-template.md`

Notes:
- Use `npx @github/spec-kit init` to initialize additional tooling if desired.
