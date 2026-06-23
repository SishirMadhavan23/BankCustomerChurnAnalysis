# Bank Customer Churn Analysis (BCCA)

AI-powered Bank Customer Churn Analysis platform with multi-language support (English, Hindi, Telugu), Random Forest ML predictions, and interactive dashboards.

## Features

- **Real-time AI Churn Predictions**: Random Forest model with 200 estimators
- **Multi-language Support**: English, Hindi (हिंदी), Telugu (తెలుగు)
- **Interactive Dashboard**: Plotly-powered visualizations
- **Customer Directory**: Search, filter, and detailed views
- **Dataset Upload**: Analyze your own CSV data
- **Feature Importance**: Understand key churn drivers

## Screenshots

### Home Page
Overview of the platform with key features and quick navigation.

### Dashboard
- Key metrics: Total customers, churned, retained, churn rate
- Interactive charts:
  - Churn distribution (pie chart)
  - Geographic distribution (bar chart)
  - Age distribution analysis
  - Credit card ownership distribution
  - Feature importance rankings

### Predict Page
Manual customer data entry with real-time prediction:
- Credit score, geography, gender, age, tenure
- Balance, products, credit card status, activity
- Estimated salary
- Returns: churn probability, confidence level, risk factors

### Customers Page
- Full customer directory with search
- Filter by geography and churn status
- Detailed customer profiles
- Upload custom datasets for batch prediction

## Tech Stack

### Backend
- **Python 3.10+**
- **scikit-learn**: Random Forest classifier
- **pandas**: Data processing
- **numpy**: Numerical operations
- **joblib**: Model serialization

### Frontend
- **Streamlit**: Web application framework
- **Plotly**: Interactive visualizations

### Quality & CI/CD
- **Ruff**: Fast Python linter and formatter
- **Mypy**: Static type checking
- **Pylint**: Code quality analysis
- **Flake8**: Style guide enforcement
- **Bandit**: Security linting
- **Vulture**: Dead code detection
- **pytest**: Test framework with coverage reporting
- **pre-commit**: Git hooks automation
- **GitLab CI**: Continuous integration pipeline
- **Gitleaks**: Secret scanning
- **Semgrep**: Static analysis for security
- **pip-audit**: Dependency vulnerability scanning
- **git-cliff**: Automated changelog generation

## Requirements

- Python >= 3.10
- See `requirements.txt` for dependencies

## Installation

```bash
# Clone the repository
git clone https://code.swecha.org/SishirMadhavan23/BCCA.git
cd BCCA

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Train the Model

```bash
python -m app.model
```

This will:
1. Load the dataset (`data/Churn_Modelling.csv` or generate synthetic data)
2. Preprocess and encode features
3. Train a Random Forest classifier
4. Save model artifacts to `model/` directory
5. Display performance metrics (accuracy, precision, recall, F1)

### Run the Streamlit App

```bash
streamlit run streamlit_app.py
```

Open your browser to `http://localhost:8501`

### Upload Your Own Data

1. Navigate to Dashboard or Customers page
2. Click "Upload Your Own Dataset"
3. Select a CSV with required columns:
   - CreditScore, Geography, Gender, Age
   - Tenure, Balance, NumOfProducts
   - HasCrCard, IsActiveMember, EstimatedSalary

The app will process the data and generate predictions automatically.

## Model Details

- **Algorithm**: Random Forest Classifier
- **Estimators**: 200
- **Max Depth**: 15
- **Min Samples Split**: 10
- **Min Samples Leaf**: 4
- **Class Weight**: balanced
- **Test Size**: 20%
- **Random State**: 42

### Performance Metrics

The model is evaluated on:
- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

## Running Tests

```bash
# Run pytest with coverage
pytest tests/ --cov=app --cov-report=term --cov-report=xml

# Current coverage: ~39%
```

## Code Quality

### Linting and Formatting

```bash
# Check code with Ruff
ruff check app/ tests/

# Format check
ruff format --check app/

# Type check with Mypy
mypy app/

# Pylint analysis
pylint app/ --fail-under=7.0

# Flake8 style check
flake8 app/ --max-line-length=100

# Dead code detection
vulture app/ --min-confidence 80
```

### Security Scanning

```bash
# Python security linting
bandit -r app/ -x tests

# Secret scanning
gitleaks detect --source . --config=.gitleaks.toml

# Dependency audit
pip-audit -r requirements.txt --desc --strict
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

## Docker

### Build Image

```bash
docker build -t bcca .
```

### Run Container

```bash
docker run -p 8501:8501 bcca
```

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── model.py              # Model training and prediction
│   └── translations.py       # i18n support (EN, HI, TE)
├── data/
│   └── Churn_Modelling.csv   # Training dataset
├── deployment/               # Deployment configurations
├── docs/                     # Documentation
├── model/                    # Saved model artifacts
├── specs/                    # Feature specifications
│   └── churn-prediction/
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
├── tests/
│   ├── __init__.py
│   └── test_model.py         # Model tests
├── .gitlab-ci.yml           # GitLab CI pipeline
├── .gitleaks.toml           # Gitleaks configuration
├── .pre-commit-config.yaml  # Pre-commit hooks
├── cliff.toml               # git-cliff changelog config
├── pyproject.toml           # Python project metadata and tool configs
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container image
├── LICENSE                  # AGPLv3 License
├── README.md                # This file
├── CONTRIBUTING.md          # Contribution guidelines
├── USER_MANUAL.md           # User guide
├── SECURITY.md              # Security policy
├── CODE_OF_CONDUCT.md       # Community guidelines
├── CHANGELOG.md             # Version history
└── streamlit_app.py         # Main application
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Application
APP_NAME=Bank Customer Churn Analysis
APP_VERSION=1.0.0

# Model paths
MODEL_PATH=model/churn_model.pkl
SCALER_PATH=model/scaler.pkl
LABEL_GEO_PATH=model/label_geo.pkl
LABEL_GENDER_PATH=model/label_gender.pkl

# Dataset
DATASET_PATH=data/Churn_Modelling.csv

# Streamlit
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

## CI/CD Pipeline

### GitLab CI Stages

1. **Lint**: Code quality checks (Ruff, Pylint, Flake8, Pyupgrade, Vulture)
2. **Format**: Code formatting verification (Ruff format)
3. **Type Check**: Static type analysis (Mypy)
4. **Test**: Unit tests with coverage reporting (pytest)
5. **Security**: Security scanning (Bandit, Semgrep, Gitleaks, TruffleHog)
6. **Build**: Docker image build
7. **Deploy**: Release automation with changelog

### GitHub Actions

Configuration available in `deployment/ci.yml`.

## GitLab Runner

This project includes automated runner setup for CI/CD execution.

### Setup Script

A ready-to-use setup script is provided at:
- `deployment/setup-gitlab-runner.sh`

This script automates runner registration and startup.

### Requirements

- GitLab Personal Access Token with `api` scope
- Runner can use `shell` or `docker` executor
- Supports Linux (apt/dnf/zypper/pacman), macOS (Homebrew)
- Windows users should run under WSL or Git Bash

### Configuration

Environment variables:
- `GITLAB_PAT` - Personal Access Token with api scope
- `GITLAB_HOST` - GitLab instance host (default: https://gitlab.com)
- `RUNNER_EXECUTOR` - `shell` or `docker`
- `RUNNER_DOCKER_IMAGE` - Docker image for docker executor
- `RUNNER_TAG_LIST` - Comma-separated runner tags

### Quick Start

```bash
# Set required PAT
export GITLAB_PAT="your-pat-here"

# Run setup script
bash deployment/setup-gitlab-runner.sh

# Or with explicit options
bash deployment/setup-gitlab-runner.sh \
  --executor docker \
  --image docker:stable \
  --tags "linux,x64,docker"
```

### Runner Management

```bash
# Check runner status
gitlab-runner list

# Restart runner service
sudo systemctl restart gitlab-runner  # systemd
brew services restart gitlab-runner  # macOS

# Stop background runner
kill $(cat ~/.gitlab-runner/runner.pid)

# View logs
tail -f ~/.gitlab-runner/runner.log
```

### Runner Configuration

After registration, the runner config is saved to:
- `~/.gitlab-runner/config.toml`

To modify executor or tags, edit this file and restart the runner.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: See [USER_MANUAL.md](USER_MANUAL.md)
- **Issues**: Report bugs via GitLab issues
- **Security**: See [SECURITY.md](SECURITY.md)

## Acknowledgments

Built with:
- scikit-learn for machine learning
- Streamlit for the web interface
- Plotly for data visualization
- The open-source community for amazing tools

---

**Version**: 1.0.0  
**Last Updated**: June 2026