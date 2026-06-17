"""Bank Customer Churn Analysis - Streamlit Application"""

import os
import sys
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.model import generate_sample_data, preprocess_data, train_model

# Model directory path
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model')
from app.translations import TRANSLATIONS, get_supported_languages


# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Bank Customer Churn Analysis",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================================
# INITIALIZATION & CACHE
# ============================================================================
@st.cache_resource
def load_model_artifacts():
    """Load trained model and preprocessing artifacts."""
    try:
        model_path = os.path.join(MODEL_DIR, 'churn_model.pkl')
        scaler_path = os.path.join(MODEL_DIR, 'scaler.pkl')
        label_geo_path = os.path.join(MODEL_DIR, 'label_geo.pkl')
        label_gender_path = os.path.join(MODEL_DIR, 'label_gender.pkl')
        
        if not all(os.path.exists(p) for p in [model_path, scaler_path, label_geo_path, label_gender_path]):
            st.warning("🔄 Training model for the first time...")
            train_model()
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        label_geo = joblib.load(label_geo_path)
        label_gender = joblib.load(label_gender_path)
        
        return model, scaler, label_geo, label_gender
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None, None, None


@st.cache_data
def get_dashboard_data():
    """Generate dashboard analytics data."""
    df = generate_sample_data(5000)
    churned = df[df['Exited'] == 1]
    retained = df[df['Exited'] == 0]

    geo_counts = df['Geography'].value_counts()
    churn_by_geo = df.groupby('Geography')['Exited'].mean() * 100
    age_bins = pd.cut(df['Age'], bins=[0, 30, 40, 50, 60, 100], labels=['18-30', '31-40', '41-50', '51-60', '60+'])
    age_dist = df.groupby(age_bins, observed=True)['Exited'].agg(['count', ('rate', lambda x: (x.sum() / len(x) * 100))]).to_dict('index')

    return {
        'df': df,
        'total_customers': len(df),
        'churned': len(churned),
        'retained': len(retained),
        'churn_rate': len(churned) / len(df) * 100,
        'active_members': int(df['IsActiveMember'].sum()),
        'avg_age': float(df['Age'].mean()),
        'avg_balance': float(df['Balance'].mean()),
        'avg_credit_score': float(df['CreditScore'].mean()),
        'geo_counts': geo_counts,
        'churn_by_geo': churn_by_geo,
        'age_dist': age_dist,
        'has_credit_card': int(df['HasCrCard'].sum()),
        'no_credit_card': int(len(df) - df['HasCrCard'].sum()),
    }


def get_text(lang, key):
    """Get translated text."""
    if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
        return TRANSLATIONS[lang][key]
    return TRANSLATIONS['en'].get(key, key)


# ============================================================================
# SIDEBAR - LANGUAGE SELECTION
# ============================================================================
st.sidebar.title("⚙️ Settings")

languages = {lang: get_text(lang, 'language_name') for lang in get_supported_languages()}
selected_lang = st.sidebar.selectbox(
    "Language / भाषा / భాష",
    options=list(languages.keys()),
    format_func=lambda x: languages[x],
    key='language'
)

# Store language in session state
st.session_state.lang = selected_lang


# ============================================================================
# NAVIGATION
# ============================================================================
st.sidebar.divider()
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "📊 Dashboard", "🔮 Predict", "ℹ️ About"],
    index=0
)

page_map = {
    "🏠 Home": "home",
    "📊 Dashboard": "dashboard",
    "🔮 Predict": "predict",
    "ℹ️ About": "about",
}

current_page = page_map[page]


# ============================================================================
# PAGE: HOME
# ============================================================================
def show_home():
    """Home page."""
    lang = st.session_state.get('lang', 'en')
    
    st.title(f"🏦 {get_text(lang, 'app_title')}")
    st.markdown(f"### {get_text(lang, 'app_subtitle')}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        ### {get_text(lang, 'hero_title')}
        {get_text(lang, 'hero_desc')}
        """)
        
        if st.button(f"🚀 {get_text(lang, 'cta_start')}", use_container_width=True):
            st.session_state.page = 'predict'
            st.rerun()
    
    with col2:
        st.info("""
        ✨ **Key Features:**
        - 🤖 Real-time AI churn predictions
        - 🌍 Multi-language support (English, Hindi, Telugu)
        - 📈 Comprehensive analytics dashboard
        - 🎯 Feature importance analysis
        """)
    
    st.markdown("---")
    st.markdown(f"<p style='text-align: center; color: gray;'>{get_text(lang, 'footer_text')}</p>", unsafe_allow_html=True)


# ============================================================================
# PAGE: DASHBOARD
# ============================================================================
def show_dashboard():
    """Dashboard page."""
    lang = st.session_state.get('lang', 'en')
    
    st.title(f"📊 {get_text(lang, 'dashboard_title')}")
    
    # Load data
    data = get_dashboard_data()
    df = data['df']
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(get_text(lang, 'dashboard_total'), f"{data['total_customers']:,}")
    
    with col2:
        st.metric(get_text(lang, 'dashboard_churned'), f"{data['churned']:,}")
    
    with col3:
        st.metric(get_text(lang, 'dashboard_retained'), f"{data['retained']:,}")
    
    with col4:
        st.metric(get_text(lang, 'dashboard_churn_rate'), f"{data['churn_rate']:.1f}%")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Churn distribution
        churn_data = pd.DataFrame({
            'Status': [get_text(lang, 'dashboard_retained'), get_text(lang, 'dashboard_churned')],
            'Count': [data['retained'], data['churned']]
        })
        fig = px.pie(churn_data, values='Count', names='Status', 
                     title=get_text(lang, 'chart_churn_dist'),
                     color_discrete_map={'Retained': '#2ecc71', 'Churned': '#e74c3c'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Geographic distribution
        geo_data = pd.DataFrame({
            'Geography': data['geo_counts'].index,
            'Count': data['geo_counts'].values
        })
        fig = px.bar(geo_data, x='Geography', y='Count',
                     title=get_text(lang, 'chart_geo_dist'),
                     color='Count', color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Age distribution
        age_data = pd.DataFrame({
            'Age Group': list(data['age_dist'].keys()),
            'Churn Rate': [v.get('rate', 0) if isinstance(v, dict) else 0 for v in data['age_dist'].values()]
        })
        if not age_data.empty:
            fig = px.bar(age_data, x='Age Group', y='Churn Rate',
                         title=get_text(lang, 'chart_age_dist'),
                         color='Churn Rate', color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Credit card distribution
        cc_data = pd.DataFrame({
            'Status': [get_text(lang, 'yes'), get_text(lang, 'no')],
            'Count': [data['has_credit_card'], data['no_credit_card']]
        })
        fig = px.pie(cc_data, values='Count', names='Status',
                     title="Credit Card Distribution")
        st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# PAGE: PREDICT
# ============================================================================
def show_predict():
    """Prediction page."""
    lang = st.session_state.get('lang', 'en')
    
    st.title(f"🔮 {get_text(lang, 'predict_title')}")
    st.markdown(get_text(lang, 'predict_desc'))
    
    model, scaler, label_geo, label_gender = load_model_artifacts()
    
    if model is None:
        st.error("⚠️ Model could not be loaded. Please check the logs.")
        return
    
    # Input form
    col1, col2, col3 = st.columns(3)
    
    with col1:
        credit_score = st.number_input(
            get_text(lang, 'predict_credit_score'),
            min_value=300, max_value=850, value=650, step=10
        )
        
        age = st.number_input(
            get_text(lang, 'predict_age'),
            min_value=18, max_value=100, value=35, step=1
        )
        
        balance = st.number_input(
            get_text(lang, 'predict_balance'),
            min_value=0.0, value=50000.0, step=1000.0
        )
    
    with col2:
        geography = st.selectbox(
            get_text(lang, 'predict_geography'),
            ['France', 'Spain', 'Germany']
        )
        
        tenure = st.number_input(
            get_text(lang, 'predict_tenure'),
            min_value=0, max_value=50, value=5, step=1
        )
        
        num_products = st.number_input(
            get_text(lang, 'predict_num_products'),
            min_value=1, max_value=4, value=1, step=1
        )
    
    with col3:
        gender = st.selectbox(
            get_text(lang, 'predict_gender'),
            ['Male', 'Female']
        )
        
        has_cr_card = st.selectbox(
            get_text(lang, 'predict_has_cr_card'),
            [0, 1],
            format_func=lambda x: get_text(lang, 'yes') if x == 1 else get_text(lang, 'no')
        )
        
        is_active_member = st.selectbox(
            get_text(lang, 'predict_is_active'),
            [0, 1],
            format_func=lambda x: get_text(lang, 'yes') if x == 1 else get_text(lang, 'no')
        )
    
    salary = st.number_input(
        get_text(lang, 'predict_salary'),
        min_value=0.0, value=100000.0, step=5000.0
    )
    
    # Predict button
    if st.button(f"🔮 {get_text(lang, 'predict_btn')}", use_container_width=True):
        try:
            # Encode categorical features
            geo_encoded = label_geo.transform([geography])[0]
            gender_encoded = label_gender.transform([gender])[0]
            
            # Prepare features
            features = np.array([[
                float(credit_score),
                geo_encoded,
                gender_encoded,
                float(age),
                float(tenure),
                float(balance),
                float(num_products),
                float(has_cr_card),
                float(is_active_member),
                float(salary)
            ]])
            
            # Scale features
            features_scaled = scaler.transform(features)
            
            # Predict
            probability = float(model.predict_proba(features_scaled)[0][1])
            prediction = int(model.predict(features_scaled)[0])
            confidence = max(probability, 1 - probability)
            
            st.markdown("---")
            st.subheader(get_text(lang, 'predict_result'))
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    get_text(lang, 'predict_probability'),
                    f"{probability * 100:.1f}%"
                )
            
            with col2:
                st.metric(
                    get_text(lang, 'predict_confidence'),
                    f"{confidence * 100:.1f}%"
                )
            
            with col3:
                risk_text = get_text(lang, 'predict_risk_high') if prediction == 1 else get_text(lang, 'predict_risk_low')
                st.metric(
                    "Risk Level",
                    "🔴 HIGH" if prediction == 1 else "🟢 LOW"
                )
            
            # Display message
            if prediction == 1:
                st.warning(get_text(lang, 'predict_risk_high'))
            else:
                st.success(get_text(lang, 'predict_risk_low'))
        
        except Exception as e:
            st.error(f"Error making prediction: {e}")


# ============================================================================
# PAGE: ABOUT
# ============================================================================
def show_about():
    """About page."""
    lang = st.session_state.get('lang', 'en')
    
    st.title(f"ℹ️ {get_text(lang, 'about_title')}")
    
    st.markdown(f"""
    {get_text(lang, 'about_desc')}
    
    ### {get_text(lang, 'about_features')}
    - ✅ {get_text(lang, 'about_feature1')}
    - ✅ {get_text(lang, 'about_feature2')}
    - ✅ {get_text(lang, 'about_feature3')}
    - ✅ {get_text(lang, 'about_feature4')}
    
    ---
    
    {get_text(lang, 'about_team')}
    """)


# ============================================================================
# PAGE ROUTING
# ============================================================================
if current_page == "home":
    show_home()
elif current_page == "dashboard":
    show_dashboard()
elif current_page == "predict":
    show_predict()
elif current_page == "about":
    show_about()
