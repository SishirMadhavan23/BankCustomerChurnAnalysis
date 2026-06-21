"""Bank Customer Churn Prediction Model - Training Script"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


# Path to the real dataset
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
DATASET_PATH = os.path.join(DATA_DIR, 'Churn_Modelling.csv')


def load_real_dataset():
    """Load the real Churn_Modelling.csv dataset if available."""
    if os.path.exists(DATASET_PATH):
        df = pd.read_csv(DATASET_PATH)
        # Build a CustomerName column from the Surname (and optionally CustomerId for uniqueness)
        if 'Surname' in df.columns:
            df['CustomerName'] = df['Surname']
        else:
            # Generate names as a fallback
            df['CustomerName'] = generate_customer_names(len(df))
        return df
    return None


def generate_customer_names(n_samples=5000, seed=99):
    """Generate synthetic customer names."""
    np.random.seed(seed)
    first_names = [
        'James', 'Emma', 'Oliver', 'Sophia', 'William', 'Isabella', 'Lucas', 'Mia',
        'Henry', 'Charlotte', 'Alexander', 'Amelia', 'Daniel', 'Harper', 'Matthew', 'Evelyn',
        'Sebastian', 'Abigail', 'Jack', 'Emily', 'Owen', 'Ella', 'Samuel', 'Scarlett',
        'Ryan', 'Grace', 'Nathan', 'Chloe', 'Carter', 'Victoria', 'Luke', 'Riley',
        'Dylan', 'Aria', 'Andrew', 'Lily', 'Isaac', 'Aurora', 'Thomas', 'Zoey',
        'Ethan', 'Nora', 'Noah', 'Camila', 'Liam', 'Penelope', 'Mason', 'Layla',
        'Arjun', 'Priya', 'Raj', 'Ananya', 'Vikram', 'Neha', 'Ravi', 'Deepika',
        'Suresh', 'Kavita', 'Amit', 'Pooja', 'Rahul', 'Anjali', 'Sanjay', 'Meera',
        'Carlos', 'Maria', 'Jose', 'Ana', 'Luis', 'Carmen', 'Jorge', 'Rosa',
        'Pedro', 'Elena', 'Miguel', 'Beatriz', 'Rafael', 'Lucia', 'Fernando', 'Sofia'
    ]
    last_names = [
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
        'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas',
        'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White',
        'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young',
        'Sharma', 'Verma', 'Patel', 'Singh', 'Kumar', 'Gupta', 'Reddy', 'Nair',
        'Fernandez', 'Luis', 'Garcia', 'Moreno', 'Alvarez', 'Romero', 'Ruiz', 'Torres'
    ]
    names = []
    for _ in range(n_samples):
        first = np.random.choice(first_names)
        last = np.random.choice(last_names)
        names.append(f"{first} {last}")
    return names


def generate_sample_data(n_samples=5000):
    """Generate a realistic synthetic bank customer churn dataset.
    Falls back to synthetic generation if the real CSV is not available.
    """
    # Try to load the real dataset first
    real_df = load_real_dataset()
    if real_df is not None and len(real_df) >= n_samples:
        # Return the requested number of samples from the real dataset
        return real_df.head(n_samples).copy()
    elif real_df is not None:
        # Use what we have but it's smaller than requested
        print(f"Note: Real dataset has {len(real_df)} rows, using all of them.")
        return real_df.copy()

    # Fallback: synthetic data generation
    print("No real dataset found at", DATASET_PATH, "- generating synthetic data.")
    np.random.seed(42)

    data = {
        'CustomerName': generate_customer_names(n_samples),
        'CreditScore': np.random.randint(350, 850, n_samples),
        'Geography': np.random.choice(['France', 'Spain', 'Germany'], n_samples, p=[0.5, 0.25, 0.25]),
        'Gender': np.random.choice(['Male', 'Female'], n_samples),
        'Age': np.random.randint(18, 92, n_samples),
        'Tenure': np.random.randint(0, 11, n_samples),
        'Balance': np.round(np.random.uniform(0, 250000, n_samples), 2),
        'NumOfProducts': np.random.randint(1, 5, n_samples),
        'HasCrCard': np.random.randint(0, 2, n_samples),
        'IsActiveMember': np.random.randint(0, 2, n_samples),
        'EstimatedSalary': np.round(np.random.uniform(0, 200000, n_samples), 2),
    }

    df = pd.DataFrame(data)

    # Simulate churn probability based on features
    churn_prob = (
        (df['Age'] > 50) * 0.15 +
        (df['Balance'] > 100000) * 0.10 +
        (df['IsActiveMember'] == 0) * 0.20 +
        (df['NumOfProducts'] > 2) * 0.10 +
        (df['CreditScore'] < 500) * 0.10 +
        (df['Geography'] == 'Germany') * 0.08 +
        np.random.uniform(-0.1, 0.1, n_samples)
    )
    churn_prob = np.clip(churn_prob, 0, 1)
    df['Exited'] = (churn_prob > 0.35).astype(int)

    return df


def preprocess_data(df):
    """Preprocess the dataset: encode categoricals, scale features."""
    le_geo = LabelEncoder()
    le_gender = LabelEncoder()

    df['Geography_Encoded'] = le_geo.fit_transform(df['Geography'])
    df['Gender_Encoded'] = le_gender.fit_transform(df['Gender'])

    feature_cols = [
        'CreditScore', 'Geography_Encoded', 'Gender_Encoded', 'Age',
        'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard',
        'IsActiveMember', 'EstimatedSalary'
    ]

    X = df[feature_cols]
    y = df['Exited']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler, le_geo, le_gender


def train_model():
    """Train and save the churn prediction model using the real dataset if available."""
    print("Loading data...")
    df = generate_sample_data()

    print(f"Dataset loaded: {len(df)} samples")
    if os.path.exists(DATASET_PATH):
        print(f"Source: {DATASET_PATH}")
    else:
        print("Source: Synthetic data (real dataset not found)")

    print("Preprocessing data...")
    X, y, scaler, le_geo, le_gender = preprocess_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=4,
        random_state=42,
        class_weight='balanced',
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print(f"Confusion Matrix:\n{cm}")

    # Save artifacts
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'model')
    os.makedirs(model_dir, exist_ok=True)

    joblib.dump(model, os.path.join(model_dir, 'churn_model.pkl'))
    joblib.dump(scaler, os.path.join(model_dir, 'scaler.pkl'))
    joblib.dump(le_geo, os.path.join(model_dir, 'label_geo.pkl'))
    joblib.dump(le_gender, os.path.join(model_dir, 'label_gender.pkl'))

    # Save feature importances
    feature_names = [
        'CreditScore', 'Geography', 'Gender', 'Age',
        'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard',
        'IsActiveMember', 'EstimatedSalary'
    ]
    importances = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    importances.to_csv(os.path.join(model_dir, 'feature_importances.csv'), index=False)
    print(f"\nFeature Importances:\n{importances}")

    return {
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1)
    }


if __name__ == '__main__':
    metrics = train_model()
    print(f"\nTraining complete! Metrics: {metrics}")