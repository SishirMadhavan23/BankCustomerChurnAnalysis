"""Tests for the model training module."""

import os

import numpy as np
import pandas as pd

from app.model import DATASET_PATH, generate_sample_data, get_full_customer_dataset, preprocess_data


class TestModelTraining:
    """Test suite for model training functionality."""

    def test_generate_sample_data_shape(self):
        """Test that sample data has correct shape."""
        df = generate_sample_data(5000)
        assert 0 < len(df) <= 5000
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
        assert pd.api.types.is_string_dtype(df['Geography'])
        assert pd.api.types.is_string_dtype(df['Gender'])

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
        assert X.shape[0] == len(df)
        assert X.shape[1] == 10
        assert len(y) == len(df)
        assert scaler is not None
        assert le_geo is not None
        assert le_gender is not None

    def test_preprocess_data_encoding(self):
        """Test that categorical encoding works correctly."""
        df = generate_sample_data(100)
        _unused_X, _unused_y, _unused_scaler, le_geo, le_gender = preprocess_data(df)
        assert 'Geography_Encoded' in df.columns
        assert 'Gender_Encoded' in df.columns
        assert set(le_geo.classes_) == {'France', 'Spain', 'Germany'}
        assert set(le_gender.classes_) == {'Female', 'Male'}

    def test_get_full_customer_dataset(self):
        """Test that the full dataset loader returns all real rows when available."""
        df = get_full_customer_dataset()
        assert 'CustomerName' in df.columns

        if os.path.exists(DATASET_PATH):
            expected = len(pd.read_csv(DATASET_PATH))
            assert len(df) == expected
