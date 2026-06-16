# BCCA-FEAT-001 Prediction API

## Summary
Add a formal prediction API endpoint that accepts customer input and returns churn prediction results with probability and confidence metadata.

## Motivation
A predictable, machine-readable prediction endpoint is required for integrating churn analysis into external dashboards and product workflows.

## Stakeholders
- Product
- Backend engineering
- Data science
- QA

## Acceptance Criteria
- [ ] POST `/api/predict` accepts JSON payload with customer demographic and account features
- [ ] Response includes `prediction`, `probability`, `confidence`, and `risk_level`
- [ ] Input validation returns clear error messages for invalid payloads
- [ ] Endpoint is documented in the repo README and API docs

## Success Metrics
- API responds with valid prediction results for valid customer records
- Error cases return `400 Bad Request` with details
- `specs/BCCA-FEAT-001-prediction-api.md` is tracked in source control

## Implementation Notes
- Use existing `app.model` prediction logic
- Keep API contract backward-compatible for current UI usage

## Non-Goals
- Do not add UI changes in this feature spec
- Do not change existing dashboard analytics endpoints

## Related Docs / References
- `app/app.py`
- `app/model.py`
- `README.md`
