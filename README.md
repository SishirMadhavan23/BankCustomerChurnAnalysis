# Bank Customer Churn Analysis (BCCA)

AI-powered Bank Customer Churn Analysis platform with multi-language support (English, Hindi, Telugu), Random Forest ML predictions, and interactive dashboards.

## Features

- Real-time AI churn predictions
- Multi-language support (English, Hindi, Telugu)
- Comprehensive analytics dashboard
- Feature importance analysis
- Customer directory with search & filter
- Dataset upload for custom analysis

## Requirements

- Python >= 3.10
- See `requirements.txt` for dependencies

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
streamlit run streamlit_app.py
```

## Model Training

```bash
python -m app.model
```

## Running Tests

```bash
pytest tests/
```

## License

AGPL-3.0-only