# Bank Customer Churn Analysis (BCCA)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green)](https://flask.palletsprojects.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-orange)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

An AI-powered Bank Customer Churn Analysis platform that leverages machine learning to predict customer churn probability. Built with Flask, scikit-learn, and Chart.js, with multi-language support for English, Hindi, and Telugu.

## 🌟 Features

- **🔮 AI-Powered Predictions**: Real-time churn prediction using Random Forest classifier
- **📊 Interactive Dashboard**: Comprehensive analytics with KPI cards and charts
- **🌐 Multi-Language Support**: UI available in English, Hindi (हिंदी), and Telugu (తెలుగు)
- **📈 Feature Importance Analysis**: Understand which factors most influence churn
- **🎯 High Accuracy**: Trained on 5000+ synthetic customer records
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bank-customer-churn-analysis.git
cd bank-customer-churn-analysis
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Train the model:
```bash
python -m app.model
```

5. Run the application:
```bash
python -m app.app
```

6. Open your browser and navigate to:
```
http://localhost:5000
```

## 🏗️ Project Structure

```
bcca/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── app.py               # Flask application & API routes
│   ├── model.py             # ML model training & data generation
│   ├── translations.py      # i18n translations (EN/HI/TE)
│   ├── templates/
│   │   └── index.html       # Main HTML template
│   └── static/
│       ├── css/
│       │   └── styles.css   # Application styles
│       └── js/
│           ├── i18n.js      # Internationalization module
│           └── app.js       # Main application logic
├── model/                   # Trained model artifacts (generated)
├── tests/                   # Test suite
├── .github/workflows/       # CI/CD pipelines
├── k8s/                     # Kubernetes manifests
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
├── .env.example             # Environment variables template
└── README.md               # This file
```

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application page |
| `/api/predict` | POST | Submit customer data for churn prediction |
| `/api/dashboard` | GET | Retrieve dashboard analytics data |
| `/api/feature-importances` | GET | Get feature importance rankings |
| `/api/translations` | GET | Get i18n translations for a language |
| `/api/languages` | GET | List supported languages |
| `/health` | GET | Health check endpoint |

### Prediction API Example

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "credit_score": 650,
    "geography": "France",
    "gender": "Male",
    "age": 35,
    "tenure": 5,
    "balance": 50000,
    "num_products": 2,
    "has_cr_card": 1,
    "is_active_member": 1,
    "estimated_salary": 75000
  }'
```

## 🧪 Running Tests

```bash
pytest tests/ --cov=app --cov-report=term
```

## 🐳 Docker Deployment

```bash
# Build the image
docker build -t bcca .

# Run the container
docker run -p 5000:5000 bcca
```

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:

```env
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=1
PORT=5000
```

## 📊 Model Performance

- **Algorithm**: Random Forest Classifier
- **Estimators**: 200
- **Max Depth**: 15
- **Training Data**: 5,000 synthetic samples
- **Features**: 10 customer attributes

## 🌐 Language Support

The platform supports three languages:
- 🇺🇸 English (en)
- 🇮🇳 Hindi (hi) - हिंदी
- 🇮🇳 Telugu (te) - తెలుగు

Switch languages using the dropdown in the navigation bar.

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Machine Learning with [scikit-learn](https://scikit-learn.org/)
- Charts powered by [Chart.js](https://www.chartjs.org/)