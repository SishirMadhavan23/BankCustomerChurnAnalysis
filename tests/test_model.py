"""Tests for the model training module."""

import numpy as np
from app.model import generate_sample_data, preprocess_data


class TestModelTraining:
    """Test suite for model training functionality."""

    def test_generate_sample_data_shape(self):
        """Test that sample data has correct shape."""
        df = generate_sample_data(5000)
        assert len(df) == 5000
        assert 'Exited' in df.columns
        assert 'CreditScore' in df.columns
        assert 'Geography' in df.columns
        assert 'Gender' in df.columns
        assert 'Age' in df.columns
        assert 'Tenure' in df.columns
        assert 'Balance' in df.columns
        assert 'NumOfProducts' in df.columns
        assert 'HasCrCard' in df.columns
        assert 'IsActiveMember' in df.columns
        assert 'EstimatedSalary' in df.columns

    def test_generate_sample_data_types(self):
        """Test that sample data has correct dtypes."""
        df = generate_sample_data(1000)
        assert df['CreditScore'].dtype in [np.int64, np.int32]
        assert df['Age'].dtype in [np.int64, np.int32]
        assert df['Balance'].dtype == np.float64
        assert df['EstimatedSalary'].dtype == np.float64
        assert df['Geography'].dtype == 'object'
        assert df['Gender'].dtype == 'object'

    def test_generate_sample_data_values(self):
        """Test that sample data has reasonable value ranges."""
        df = generate_sample_data(1000)
        assert df['CreditScore'].between(350, 850).all()
        assert df['Age'].between(18, 92).all()
        assert df['Tenure'].between(0, 10).all()
        assert df['Balance'].between(0, 250000).all()
        assert df['NumOfProducts'].between(1, 4).all()
        assert df['HasCrCard'].isin([0, 1]).all()
        assert df['IsActiveMember'].isin([0, 1]).all()
        assert df['Exited'].isin([0, 1]).all()

    def test_preprocess_data(self):
        """Test that preprocessing returns correct shapes."""
        df = generate_sample_data(1000)
        X, y, scaler, le_geo, le_gender = preprocess_data(df)
        assert X.shape[0] == 1000
        assert X.shape[1] == 10
        assert len(y) == 1000
        assert scaler is not None
        assert le_geo is not None
        assert le_gender is not None

    def test_preprocess_data_encoding(self):
        """Test that categorical encoding works correctly."""
        df = generate_sample_data(100)
        X, y, scaler, le_geo, le_gender = preprocess_data(df)
        assert 'Geography_Encoded' in df.columns
        assert 'Gender_Encoded' in df.columns
        assert set(le_geo.classes_) == {'France', 'Spain', 'Germany'}
        assert set(le_gender.classes_) == {'Female', 'Male'}