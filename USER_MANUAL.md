# Bank Customer Churn Analysis - User Manual

## Getting Started

Welcome to the Bank Customer Churn Analysis platform! This guide will help you navigate and use all features of the application.

## 📋 Table of Contents

1. [Accessing the Application](#accessing-the-application)
2. [Language Selection](#language-selection)
3. [Making Predictions](#making-predictions)
4. [Understanding Results](#understanding-results)
5. [Dashboard Overview](#dashboard-overview)
6. [Charts and Analytics](#charts-and-analytics)
7. [About Section](#about-section)

## Accessing the Application

1. Ensure the application is running (see [README.md](README.md) for installation)
2. Open your web browser and navigate to `http://localhost:5000`
3. The home page will display with an overview of the platform

## Language Selection

The platform supports three languages:

1. **English** (English)
2. **Hindi** (हिंदी)
3. **Telugu** (తెలుగు)

To switch languages:
- Click the language dropdown in the top-right navigation bar
- Select your preferred language
- The entire interface will update immediately

Your language preference is saved and will be remembered on your next visit.

## Making Predictions

1. Navigate to the **Predict** section using the navigation bar
2. Fill in the customer details form:

| Field | Description | Example |
|-------|-------------|---------|
| Credit Score | Customer's credit score (300-900) | 650 |
| Geography | Country of residence | France, Spain, Germany |
| Gender | Customer's gender | Male, Female |
| Age | Customer's age (18-100) | 35 |
| Tenure | Years with the bank (0-10) | 5 |
| Balance | Account balance in USD | 50000 |
| Number of Products | Banking products used | 1-4 |
| Has Credit Card | Whether customer has credit card | Yes/No |
| Is Active Member | Whether customer is active | Yes/No |
| Estimated Salary | Customer's estimated annual salary | 75000 |

3. Click **Predict Churn** to get the prediction
4. View the results on the right panel

## Understanding Results

The prediction result shows:

- **Churn Probability Gauge**: Visual indicator of churn risk (0-100%)
- **Risk Badge**: "High Risk" (red) or "Low Risk" (green)
- **Confidence Score**: Model's confidence in the prediction
- **Risk Message**: Clear explanation of the prediction

### Risk Levels

- **High Risk (>50%)**: Customer is likely to churn. Consider retention actions.
- **Low Risk (<50%)**: Customer is likely to stay with the bank.

Click **Predict Again** to make another prediction.

## Dashboard Overview

The Dashboard section provides comprehensive analytics:

### KPI Cards
- **Total Customers**: Total number of customers in the dataset
- **Churned**: Number of customers who have left
- **Retained**: Number of customers who stayed
- **Churn Rate**: Percentage of customers who churned
- **Active Members**: Number of active customers
- **Avg Age**: Average customer age

### Charts and Analytics

1. **Churn Distribution** (Doughnut Chart)
   - Visual representation of churned vs retained customers

2. **Geographic Distribution** (Bar Chart)
   - Customer distribution by country
   - See churn rates across different regions

3. **Age Distribution** (Line Chart)
   - Churn rate across different age groups
   - Identify which age segments have higher churn

4. **Feature Importance** (Horizontal Bar Chart)
   - Shows which factors most influence churn predictions
   - Higher percentages = more influential factors

## About Section

The About section provides:
- Platform overview and purpose
- Key features list
- Model technical details (algorithm, parameters)
- Team credit

## Troubleshooting

**Q: The prediction isn't working.**
A: Ensure the model is trained by running `python -m app.model` first.

**Q: Can't see any charts.**
A: Check your internet connection - Chart.js is loaded from CDN.

**Q: Language isn't switching.**
A: Try refreshing the page after switching languages.

## Support

For additional help, please open an issue on the GitHub repository or contact the development team.