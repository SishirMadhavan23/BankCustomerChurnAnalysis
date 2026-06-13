# Agents.md - AI/LLM Agent Guide for Bank Customer Churn Analysis

## Project Overview

This project is a Bank Customer Churn Analysis platform built with Flask (Python backend), scikit-learn (ML), and Chart.js (frontend visualizations). It supports English, Hindi, and Telugu.

## Architecture

### Backend (Flask)
- **app/app.py**: Flask app with REST API endpoints for prediction, dashboard, translations
- **app/model.py**: Random Forest classifier trained on synthetic bank customer data
- **app/translations.py**: i18n dictionary with English, Hindi, Telugu translations

### Frontend (HTML/CSS/JS)
- **Single-page application** with hash-based navigation (home, predict, dashboard, about)
- **Chart.js** for visualizations (doughnut, bar, line, horizontal bar charts)
- **Client-side i18n** with language persistence via localStorage and URL params

## Key Technical Decisions

1. **Synthetic Data Generation**: Model trains on generated data for demo purposes
   - 10 features: CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary
   - Churn simulated using weighted feature combinations with random noise

2. **Multi-language Architecture**: Server-side translations stored in Python dict, served via `/api/translations` endpoint, applied client-side via `data-i18n` attributes

3. **Model Serialization**: joblib for model, scaler, and label encoders

## API Contract

### POST /api/predict
```json
{
  "credit_score": int,
  "geography": "France|Spain|Germany",
  "gender": "Male|Female",
  "age": int,
  "tenure": int,
  "balance": float,
  "num_products": int,
  "has_cr_card": 0|1,
  "is_active_member": 0|1,
  "estimated_salary": float
}
```
Response:
```json
{
  "success": true,
  "prediction": 0|1,
  "probability": float,
  "confidence": float,
  "risk_level": "high|low"
}
```

## Code Conventions

- Python: Type hints, Google-style docstrings, PEP 8 via Ruff
- JS: ES6+ with async/await, Chart.js v4
- CSS: Custom properties for theming, dark mode default, responsive breakpoints at 992px/768px/480px

## Testing Approach

- pytest for Python backend tests
- Test model training, prediction API, dashboard data generation
- Mock model loading for API tests

## Common Tasks

### Adding a New Language
1. Add translation dictionary in `app/translations.py`
2. Add option in HTML language selector (`index.html`)
3. Add to `get_supported_languages()` return

### Retraining the Model
```bash
python -m app.model
```
This regenerates the model artifacts in the `model/` directory.

### Docker Deployment
```bash
docker build -t bcca .
docker run -p 5000:5000 bcca