"""Tests for the Flask application."""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    from app.app import create_app
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestAppRoutes:
    """Test suite for Flask application routes."""

    def test_health_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'languages' in data
        assert 'model' in data

    def test_languages_endpoint(self, client):
        """Test the languages API endpoint."""
        response = client.get('/api/languages')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'en' in data['languages']
        assert 'hi' in data['languages']
        assert 'te' in data['languages']

    def test_translations_endpoint_en(self, client):
        """Test translations for English."""
        response = client.get('/api/translations?lang=en')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['app_title'] == 'Bank Customer Churn Analysis'

    def test_translations_endpoint_hi(self, client):
        """Test translations for Hindi."""
        response = client.get('/api/translations?lang=hi')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'बैंक' in data['data']['app_title']

    def test_translations_endpoint_te(self, client):
        """Test translations for Telugu."""
        response = client.get('/api/translations?lang=te')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'బ్యాంకు' in data['data']['app_title']

    def test_dashboard_endpoint(self, client):
        """Test the dashboard API endpoint."""
        response = client.get('/api/dashboard')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'total_customers' in data['data']
        assert 'churned' in data['data']
        assert 'retained' in data['data']
        assert 'churn_rate' in data['data']
        assert 'churn_distribution' in data['data']
        assert 'geo_distribution' in data['data']
        assert 'age_distribution' in data['data']

    def test_dashboard_data_values(self, client):
        """Test dashboard data has reasonable values."""
        response = client.get('/api/dashboard')
        data = json.loads(response.data)['data']
        assert data['total_customers'] > 0
        assert data['churned'] + data['retained'] == data['total_customers']
        assert 0 <= data['churn_rate'] <= 100


class TestPredictionAPI:
    """Test suite for prediction API."""

    def test_prediction_with_valid_data(self, client):
        """Test prediction with valid customer data."""
        payload = {
            'credit_score': 650,
            'geography': 'France',
            'gender': 'Male',
            'age': 35,
            'tenure': 5,
            'balance': 50000,
            'num_products': 2,
            'has_cr_card': 1,
            'is_active_member': 1,
            'estimated_salary': 75000
        }
        response = client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code in [200, 503]
        if response.status_code == 200:
            data = json.loads(response.data)
            assert data['success'] is True
            assert 'prediction' in data
            assert 'probability' in data
            assert 'confidence' in data
            assert 'risk_level' in data

    def test_prediction_with_empty_data(self, client):
        """Test prediction with no data returns 400."""
        response = client.post(
            '/api/predict',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code in [400, 503]

    def test_feature_importances(self, client):
        """Test the feature importances endpoint."""
        response = client.get('/api/feature-importances')
        assert response.status_code in [200, 503]
        if response.status_code == 200:
            data = json.loads(response.data)
            assert data['success'] is True
            assert len(data['data']) > 0
            for item in data['data']:
                assert 'feature' in item
                assert 'importance' in item