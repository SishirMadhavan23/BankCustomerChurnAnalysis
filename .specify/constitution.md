.venv/
venv/
env/
__pycache__/
*.pyc
.git/
.gitignore
.vscode/
.idea/
.env
*.env.local
.DS_Store
Thumbs.db
README.md
tests/
.github/
k8s/
.specify/
specs/
</content>
<write_to_file>
<path>d:\BCCA\.specify\constitution.md</path>
<content># Project Constitution

## Mission
Accurately predict bank customer churn using machine learning to enable proactive customer retention strategies.

## Core Principles
1. **Accuracy First**: Models must be trained and validated for reliable predictions
2. **Accessibility**: Multi-language support for diverse user base
3. **Transparency**: Feature importance analysis to explain predictions
4. **Performance**: Fast response times for real-time predictions

## Tech Stack
- Backend: Python 3.10+, Flask 3.0
- ML: scikit-learn, pandas, numpy
- Frontend: HTML5, CSS3, JavaScript (ES6+)
- Charts: Chart.js 4.x
- Testing: pytest with coverage

## Quality Standards
- Code coverage: 80% minimum
- All API endpoints must have tests
- Multi-language support for UI text
- Responsive design for all screen sizes

## Development Workflow
1. Feature branch from main
2. Write tests first (TDD approach)
3. Implement feature
4. Run full test suite
5. Code review required
6. Merge to main
</content>
<write_to_file>
<path>d:\BCCA\.specify\templates\feature.md</path>
<content># Feature: {{feature_name}}

## Description
{{description}}

## Acceptance Criteria
- [ ] {{criterion_1}}
- [ ] {{criterion_2}}
- [ ] {{criterion_3}}

## Technical Notes
{{technical_notes}}

## Dependencies
{{dependencies}}

## Testing Strategy
{{testing_strategy}}
</content>
<write_to_file>
<path>d:\BCCA\specs\index.md</path>
<content># Specifications

## Bank Customer Churn Analysis Platform

### Overview
An AI-powered platform for predicting customer churn in the banking sector, supporting English, Hindi, and Telugu.

### Core Features

1. **Churn Prediction** ( Priority: P0 )
   - Real-time prediction via REST API
   - Input: 10 customer features
   - Output: Churn probability, risk level, confidence

2. **Analytics Dashboard** ( Priority: P0 )
   - KPI cards showing key metrics
   - 4 charts: churn distribution, geographic, age, feature importance

3. **Multi-language Support** ( Priority: P0 )
   - English, Hindi, Telugu
   - Persistent language selection via localStorage

4. **Model Management** ( Priority: P1 )
   - Retrain with `python -m app.model`
   - Model artifacts stored in `model/`

### Architecture
- Flask backend serving REST APIs
- Jinja2 template rendering
- Client-side JS with Chart.js
- Server-side i18n translation dictionaries

### API Specifications
See [API Reference](README.md) for full API documentation.
</content>
<write_to_file>
<path>d:\BCCA\k8s\deployment.yaml</path>
<content>apiVersion: apps/v1
kind: Deployment
metadata:
  name: bcca
  labels:
    app: bcca
spec:
  replicas: 2
  selector:
    matchLabels:
      app: bcca
  template:
    metadata:
      labels:
        app: bcca
    spec:
      containers:
      - name: bcca
        image: bcca:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 5000
        env:
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: bcca-secret
              key: secret-key
        - name: FLASK_DEBUG
          value: "0"
        - name: PORT
          value: "5000"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 15
          periodSeconds: 20
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 10
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: bcca-service
spec:
  selector:
    app: bcca
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
</content>
<write_to_file>
<path>d:\BCCA\.pre-commit-config.yaml</path>
<content>repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.8
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        args: [--ignore-missing-imports]
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.55.0
    hooks:
      - id: eslint
        files: \.[jt]sx?$
        types: [file]