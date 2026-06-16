---
title: "BATCH PREDICTION API"
summary: "Add an endpoint to accept a CSV of customer records and return batch churn predictions."
owner: "@data-team"
related: [BCCA-FEAT-001]
---

## Background

Users want to score many customers at once (bulk uploads) rather than calling the single-record predict endpoint repeatedly.

## Feature

Add `POST /api/predict/batch` that accepts a CSV file or compressed CSV and returns prediction results and per-row probabilities.

## Acceptance Criteria
- [ ] Accept CSV (header row) with the same feature columns as the single-predict API
- [ ] Return per-row `prediction`, `probability`, and an `error` field when a row cannot be parsed
- [ ] Support `Content-Type: text/csv` and `multipart/form-data` file uploads
- [ ] Validate file size and return 413 if too large (configurable)

## API Contract (example)

Request (multipart/form-data):

```
POST /api/predict/batch
file: customers.csv
```

Response:

```
{
  "success": true,
  "results": [
    {"row": 1, "prediction": 0, "probability": 0.12},
    {"row": 2, "error": "missing field: Age"}
  ],
  "summary": {"rows": 2, "succeeded": 1, "failed": 1}
}
```

## Notes

- Implement server-side streaming or chunked processing for large files.
- Add tests covering CSV parsing, feature validation, and performance bounds.
