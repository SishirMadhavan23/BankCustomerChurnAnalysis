# User Manual - Bank Customer Churn Analysis

## Getting Started

### Launching the Application

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Train the model (first run only):
   ```bash
   python -m app.model
   ```

3. Start the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

4. Open your browser to `http://localhost:8501`

## Using the Application

### Home Page

- Overview of the platform and its key features
- Quick access to all sections via the sidebar

### Dashboard

- View key metrics: total customers, churned, retained, churn rate
- Upload your own CSV dataset for analysis
- Explore interactive charts:
  - Churn distribution pie chart
  - Geographic distribution bar chart
  - Age distribution analysis
  - Credit card distribution
  - Feature importance analysis

### Predict

- Enter customer details manually
- Get real-time churn prediction with probability
- View risk factors and confidence level

### Customers

- Browse the complete customer directory
- Search by customer name
- Filter by geography and status
- Upload custom datasets
- View detailed customer information

### About

- Learn about the application
- View model details (Random Forest, 200 estimators, max depth 15)
- See team information

## Language Support

Change the application language using the sidebar:
- English
- Hindi (हिंदी)
- Telugu (తెలుగు)

## Uploading Your Own Dataset

1. Go to Dashboard or Customers page
2. Click "Upload Your Own Dataset"
3. Select a CSV file with required columns:
   - CreditScore
   - Geography
   - Gender
   - Age
   - Tenure
   - Balance
   - NumOfProducts
   - HasCrCard
   - IsActiveMember
   - EstimatedSalary

4. The app will process the data and run predictions automatically

## Model Information

- Algorithm: Random Forest
- Estimators: 200
- Max Depth: 15
- Training Data: Churn_Modelling.csv or synthetic data

## Troubleshooting

### Model Not Loading

If you see "Model could not be loaded":
1. Ensure you have run `python -m app.model` at least once
2. Check that the `model/` directory contains:
   - churn_model.pkl
   - scaler.pkl
   - label_geo.pkl
   - label_gender.pkl

### Dataset Upload Fails

- Verify your CSV has all required columns
- Ensure data types are correct (numeric fields should be numbers)
- Check file encoding (use UTF-8)

### Performance Issues

- For large datasets (>10,000 rows), processing may take time
- Consider using the provided dataset for best performance