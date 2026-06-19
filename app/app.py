"""Bank Customer Churn Analysis - Main Flask Application"""

import os
import sys

# Ensure the project root is in sys.path when running directly
if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, session, send_from_directory

from app.translations import get_text, get_supported_languages
from app.model import generate_sample_data, preprocess_data
from app.ollama_model import explain_prediction, analyze_dashboard_insights, is_ollama_available

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'bcca-secret-key-change-in-production')

# Model paths
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model')
MODEL_PATH = os.path.join(MODEL_DIR, 'churn_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')
LABEL_GEO_PATH = os.path.join(MODEL_DIR, 'label_geo.pkl')
LABEL_GENDER_PATH = os.path.join(MODEL_DIR, 'label_gender.pkl')
FEATURE_IMPORTANCES_PATH = os.path.join(MODEL_DIR, 'feature_importances.csv')

# Global model variables
_model = None
_scaler = None
_label_geo = None
_label_gender = None
_dash_data = None
_customer_df = None


def load_model():
    """Load the trained model and preprocessing artifacts."""
    global _model, _scaler, _label_geo, _label_gender
    try:
        _model = joblib.load(MODEL_PATH)
        _scaler = joblib.load(SCALER_PATH)
        _label_geo = joblib.load(LABEL_GEO_PATH)
        _label_gender = joblib.load(LABEL_GENDER_PATH)
        return True
    except FileNotFoundError:
        # Model not trained yet
        return False


def get_dashboard_data():
    """Generate dashboard analytics data."""
    global _dash_data
    if _dash_data is not None:
        return _dash_data

    df = generate_sample_data(5000)
    churned = df[df['Exited'] == 1]
    retained = df[df['Exited'] == 0]

    geo_counts = df['Geography'].value_counts().to_dict()
    churn_by_geo = df.groupby('Geography')['Exited'].mean().to_dict()
    age_bins = pd.cut(df['Age'], bins=[0, 30, 40, 50, 60, 100], labels=['18-30', '31-40', '41-50', '51-60', '60+'])
    age_dist = df.groupby(age_bins, observed=True)['Exited'].agg(['count', 'mean']).to_dict('index')

    churn_by_age = {}
    for key, val in age_dist.items():
        churn_by_age[str(key)] = {'count': int(val['count']), 'rate': float(val['mean'])}

    _dash_data = {
        'total_customers': len(df),
        'churned': int(len(churned)),
        'retained': int(len(retained)),
        'churn_rate': float(len(churned) / len(df) * 100),
        'active_members': int(df['IsActiveMember'].sum()),
        'avg_age': float(round(df['Age'].mean(), 1)),
        'avg_balance': float(round(df['Balance'].mean(), 2)),
        'avg_credit_score': float(round(df['CreditScore'].mean(), 1)),
        'churn_distribution': {
            'churned': int(len(churned)),
            'retained': int(len(retained))
        },
        'geo_distribution': geo_counts,
        'churn_by_geo': churn_by_geo,
        'age_distribution': churn_by_age,
        'has_credit_card': int(df['HasCrCard'].sum()),
        'no_credit_card': int(len(df) - df['HasCrCard'].sum()),
    }

    return _dash_data


@app.route('/')
def index():
    """Serve the main application page."""
    lang = request.args.get('lang', 'en')
    if lang not in get_supported_languages():
        lang = 'en'
    session['lang'] = lang
    return render_template('index.html', lang=lang)


@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for churn prediction."""
    if _model is None and not load_model():
        return jsonify({'error': 'Model not trained. Please run train.py first.'}), 503

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        # Prepare input features
        geo_encoded = _label_geo.transform([data['geography']])[0]
        gender_encoded = _label_gender.transform([data['gender']])[0]

        features = np.array([[
            float(data['credit_score']),
            geo_encoded,
            gender_encoded,
            float(data['age']),
            float(data['tenure']),
            float(data['balance']),
            float(data['num_products']),
            float(data['has_cr_card']),
            float(data['is_active_member']),
            float(data['estimated_salary'])
        ]])

        # Scale features
        features_scaled = _scaler.transform(features)

        # Predict
        probability = float(_model.predict_proba(features_scaled)[0][1])
        prediction = int(_model.predict(features_scaled)[0])

        # Get confidence
        confidence = max(probability, 1 - probability)

        lang = request.args.get('lang', session.get('lang', 'en'))

        # Build response
        response_data = {
            'success': True,
            'prediction': prediction,
            'probability': round(probability * 100, 2),
            'confidence': round(confidence * 100, 2),
            'risk_level': 'high' if prediction == 1 else 'low',
            'message_high': get_text(lang, 'predict_risk_high'),
            'message_low': get_text(lang, 'predict_risk_low'),
            'probability_label': get_text(lang, 'predict_probability'),
        }

        # If Ollama is available, add AI explanation
        if is_ollama_available():
            customer_data = {
                'credit_score': data['credit_score'],
                'geography': data['geography'],
                'gender': data['gender'],
                'age': data['age'],
                'tenure': data['tenure'],
                'balance': data['balance'],
                'num_products': data['num_products'],
                'has_cr_card': data['has_cr_card'],
                'is_active_member': data['is_active_member'],
                'estimated_salary': data['estimated_salary'],
            }
            ai_insights = explain_prediction(customer_data, prediction, probability, lang)
            response_data['ai'] = ai_insights

        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/dashboard')
def dashboard():
    """API endpoint for dashboard analytics data."""
    lang = request.args.get('lang', session.get('lang', 'en'))
    data = get_dashboard_data()
    return jsonify({
        'success': True,
        'data': data,
        'labels': {
            'total': get_text(lang, 'dashboard_total'),
            'churned': get_text(lang, 'dashboard_churned'),
            'retained': get_text(lang, 'dashboard_retained'),
            'churn_rate': get_text(lang, 'dashboard_churn_rate'),
        }
    })


@app.route('/api/feature-importances')
def feature_importances():
    """API endpoint for feature importance data."""
    try:
        if os.path.exists(FEATURE_IMPORTANCES_PATH):
            df = pd.read_csv(FEATURE_IMPORTANCES_PATH)
            return jsonify({
                'success': True,
                'data': df.to_dict('records')
            })
        elif _model is not None:
            # Fallback: compute from model
            importances = _model.feature_importances_
            feature_names = [
                'CreditScore', 'Geography', 'Gender', 'Age',
                'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard',
                'IsActiveMember', 'EstimatedSalary'
            ]
            data = [
                {'feature': name, 'importance': float(imp)}
                for name, imp in sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)
            ]
            return jsonify({'success': True, 'data': data})
        else:
            return jsonify({'success': False, 'error': 'No model loaded'}), 503
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/translations')
def get_translations():
    """API endpoint for frontend i18n."""
    lang = request.args.get('lang', 'en')
    from app.translations import TRANSLATIONS
    if lang in TRANSLATIONS:
        return jsonify({'success': True, 'data': TRANSLATIONS[lang]})
    return jsonify({'success': True, 'data': TRANSLATIONS['en']})


def get_customer_dataframe():
    """Generate or retrieve the cached customer dataframe with names."""
    global _customer_df
    if _customer_df is not None:
        return _customer_df
    _customer_df = generate_sample_data(500)
    return _customer_df


@app.route('/api/customers')
def customers_list():
    """API endpoint to list all customers."""
    df = get_customer_dataframe()
    geo = request.args.get('geo', '')
    status = request.args.get('status', '')
    
    result_df = df.copy()
    if geo and geo in ['France', 'Spain', 'Germany']:
        result_df = result_df[result_df['Geography'] == geo]
    if status == 'churned':
        result_df = result_df[result_df['Exited'] == 1]
    elif status == 'retained':
        result_df = result_df[result_df['Exited'] == 0]
    
    customers = []
    for _, row in result_df.iterrows():
        customers.append({
            'name': row['CustomerName'],
            'credit_score': int(row['CreditScore']),
            'geography': row['Geography'],
            'gender': row['Gender'],
            'age': int(row['Age']),
            'tenure': int(row['Tenure']),
            'balance': float(row['Balance']),
            'num_products': int(row['NumOfProducts']),
            'has_cr_card': int(row['HasCrCard']),
            'is_active_member': int(row['IsActiveMember']),
            'estimated_salary': float(row['EstimatedSalary']),
            'exited': int(row['Exited']),
        })
    
    return jsonify({
        'success': True,
        'total': len(result_df),
        'customers': customers
    })


@app.route('/api/customers/search')
def customers_search():
    """API endpoint to search customers by name."""
    df = get_customer_dataframe()
    query = request.args.get('q', '').strip().lower()
    geo = request.args.get('geo', '')
    status = request.args.get('status', '')
    
    if not query and not geo and not status:
        return jsonify({'success': True, 'total': 0, 'customers': []})
    
    matching = df.copy()
    if query:
        matching = matching[matching['CustomerName'].str.lower().str.contains(query, na=False)]
    if geo and geo in ['France', 'Spain', 'Germany']:
        matching = matching[matching['Geography'] == geo]
    if status == 'churned':
        matching = matching[matching['Exited'] == 1]
    elif status == 'retained':
        matching = matching[matching['Exited'] == 0]
    
    customers = []
    for _, row in matching.iterrows():
        customers.append({
            'name': row['CustomerName'],
            'credit_score': int(row['CreditScore']),
            'geography': row['Geography'],
            'gender': row['Gender'],
            'age': int(row['Age']),
            'tenure': int(row['Tenure']),
            'balance': float(row['Balance']),
            'num_products': int(row['NumOfProducts']),
            'has_cr_card': int(row['HasCrCard']),
            'is_active_member': int(row['IsActiveMember']),
            'estimated_salary': float(row['EstimatedSalary']),
            'exited': int(row['Exited']),
        })
    
    return jsonify({
        'success': True,
        'total': len(matching),
        'query': query,
        'customers': customers
    })


@app.route('/api/upload-dataset', methods=['POST'])
def upload_dataset():
    """Upload a CSV dataset and run batch predictions on it."""
    global _customer_df, _dash_data

    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({'success': False, 'error': 'Only CSV files are supported'}), 400

    try:
        df = pd.read_csv(file)

        # Validate required columns
        required_cols = ['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure',
                         'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            return jsonify({
                'success': False,
                'error': f'Missing required columns: {", ".join(missing)}. Required: {", ".join(required_cols)}'
            }), 400

        # Add CustomerName if not present
        if 'CustomerName' not in df.columns:
            from app.model import generate_customer_names
            df['CustomerName'] = generate_customer_names(len(df))

        # Compute churn predictions for all rows
        if _model is None and not load_model():
            return jsonify({'error': 'Model not trained. Please run train.py first.'}), 503

        predictions = []
        for _, row in df.iterrows():
            try:
                geo_encoded = _label_geo.transform([row['Geography']])[0]
                gender_encoded = _label_gender.transform([row['Gender']])[0]

                features = np.array([[
                    float(row['CreditScore']), geo_encoded, gender_encoded,
                    float(row['Age']), float(row['Tenure']), float(row['Balance']),
                    float(row['NumOfProducts']), float(row['HasCrCard']),
                    float(row['IsActiveMember']), float(row['EstimatedSalary'])
                ]])
                features_scaled = _scaler.transform(features)
                prob = float(_model.predict_proba(features_scaled)[0][1])
                pred = int(_model.predict(features_scaled)[0])
                predictions.append({
                    'name': row.get('CustomerName', f'Customer {_}'),
                    'credit_score': int(row['CreditScore']),
                    'geography': row['Geography'],
                    'gender': row['Gender'],
                    'age': int(row['Age']),
                    'tenure': int(row['Tenure']),
                    'balance': float(row['Balance']),
                    'num_products': int(row['NumOfProducts']),
                    'has_cr_card': int(row['HasCrCard']),
                    'is_active_member': int(row['IsActiveMember']),
                    'estimated_salary': float(row['EstimatedSalary']),
                    'exited': pred,
                    'probability': round(prob * 100, 2),
                    'risk_level': 'high' if pred == 1 else 'low',
                })
            except Exception as e:
                predictions.append({
                    'name': row.get('CustomerName', f'Customer {_}'),
                    'error': str(e)
                })

        # Replace the cached customer dataframe with uploaded data
        df['Exited'] = [p.get('exited', 0) for p in predictions]
        _customer_df = df

        # Reset dashboard cache so it regenerates from new data
        _dash_data = None

        churned_count = sum(1 for p in predictions if p.get('exited') == 1)
        retained_count = sum(1 for p in predictions if p.get('exited') == 0)

        return jsonify({
            'success': True,
            'total': len(predictions),
            'churned': churned_count,
            'retained': retained_count,
            'predictions': predictions,
            'message': f'Dataset loaded! {len(predictions)} customers processed. '
                       f'{churned_count} at risk of churn ({round(churned_count/len(predictions)*100, 1)}%).'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': f'Failed to process file: {str(e)}'}), 500


@app.route('/api/ai/health')
def ai_health():
    """Check if Ollama AI backend is available."""
    return jsonify({
        'success': True,
        'ollama_available': is_ollama_available(),
        'ollama_host': os.environ.get('OLLAMA_HOST', 'http://localhost:11434'),
        'ollama_model': os.environ.get('OLLAMA_MODEL', 'llama3.2:1b'),
    })


@app.route('/api/ai/dashboard-insights')
def ai_dashboard_insights():
    """AI-generated insights from dashboard data."""
    if not is_ollama_available():
        return jsonify({
            'success': False,
            'error': 'Ollama AI backend is not available. Start Ollama and pull a model.',
            'setup_instructions': 'Install Ollama from https://ollama.com, then run: ollama pull llama3.2:1b'
        }), 503

    lang = request.args.get('lang', session.get('lang', 'en'))
    data = get_dashboard_data()
    insights = analyze_dashboard_insights(data, lang)
    return jsonify({
        'success': True,
        'insights': insights,
        'ollama_model': os.environ.get('OLLAMA_MODEL', 'llama3.2:1b')
    })


@app.route('/api/languages')
def languages():
    """API endpoint for supported languages."""
    return jsonify({
        'success': True,
        'languages': get_supported_languages()
    })


@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files."""
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'static'), filename)


@app.route('/health')
def health():
    """Health check endpoint."""
    model_status = 'loaded' if _model is not None else 'not_loaded'
    return jsonify({
        'status': 'healthy',
        'model': model_status,
        'languages': get_supported_languages()
    })


def create_app():
    """Application factory for testing."""
    load_model()
    return app


# Load model at startup
load_model()

# Export app for WSGI servers (Gunicorn, etc.)
wsgi_app = app

if __name__ == '__main__':
    # Only run dev server if not in production
    if os.environ.get('FLASK_ENV') == 'production':
        # In production, use: gunicorn --bind 0.0.0.0:$PORT app.app:app
        pass
    else:
        port = int(os.environ.get('PORT', 5000))
        debug = os.environ.get('FLASK_DEBUG', '1') == '1'
        # Use use_reloader=False to avoid signal handler issues in containers
        app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)