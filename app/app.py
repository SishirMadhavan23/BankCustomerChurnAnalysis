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

        return jsonify({
            'success': True,
            'prediction': prediction,
            'probability': round(probability * 100, 2),
            'confidence': round(confidence * 100, 2),
            'risk_level': 'high' if prediction == 1 else 'low',
            'message_high': get_text(lang, 'predict_risk_high'),
            'message_low': get_text(lang, 'predict_risk_low'),
            'probability_label': get_text(lang, 'predict_probability'),
        })

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


if __name__ == '__main__':
    load_model()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)