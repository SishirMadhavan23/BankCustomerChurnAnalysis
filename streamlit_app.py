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
from io import StringIO

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.model import generate_sample_data, preprocess_data, train_model, DATASET_PATH, generate_customer_names

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

# Premium dark theme colors - charcoal black, slate gray, electric blue
DARK_BG = "#1a1a1a"
DARK_CARD = "#2d2d2d"
DARK_CARD_HOVER = "#3a3a3a"
ELECTRIC_BLUE = "#0077b6"
ELECTRIC_BLUE_LIGHT = "#48cae4"
CYAN = "#00b4d8"
TEXT_WHITE = "#ffffff"
TEXT_GRAY = "#e2e8f0"
TEXT_MUTED = "#94a3b8"

# Custom CSS for dark theme
st.markdown(f"""
<style>
    /* Main background */
    .stApp {{
        background-color: {DARK_BG};
    }}

    /* Sidebar */
    .css-1d391kg, .css-1wrcr25, [data-testid="stSidebar"] {{
        background-color: {DARK_CARD} !important;
    }}

    /* Headers */
    h1, h2, h3 {{
        color: {TEXT_WHITE} !important;
    }}

    /* Metric cards */
    [data-testid="stMetric"] {{
        background-color: rgba(30, 30, 50, 0.85);
        border: 1px solid rgba(0, 119, 182, 0.2);
        border-radius: 12px;
        padding: 16px;
        backdrop-filter: blur(10px);
    }}

    [data-testid="stMetric"]:hover {{
        border-color: rgba(0, 119, 182, 0.4);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }}

    [data-testid="stMetric"] label {{
        color: {TEXT_GRAY} !important;
    }}

    [data-testid="stMetric"] [data-testid="stMetricValue"] {{
        color: {TEXT_WHITE} !important;
    }}

    /* Buttons */
    .stButton button {{
        background: linear-gradient(135deg, {ELECTRIC_BLUE}, {CYAN}) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}

    .stButton button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0, 119, 182, 0.4) !important;
    }}

    /* Select boxes and inputs */
    .stSelectbox div[data-baseweb="select"] {{
        background-color: rgba(18, 18, 26, 0.8) !important;
        border-color: rgba(0, 119, 182, 0.2) !important;
        color: {TEXT_WHITE} !important;
        border-radius: 8px !important;
    }}

    .stNumberInput input {{
        background-color: rgba(18, 18, 26, 0.8) !important;
        border-color: rgba(0, 119, 182, 0.2) !important;
        color: {TEXT_WHITE} !important;
        border-radius: 8px !important;
    }}

    .stTextInput input {{
        background-color: rgba(18, 18, 26, 0.8) !important;
        border-color: rgba(0, 119, 182, 0.2) !important;
        color: {TEXT_WHITE} !important;
        border-radius: 8px !important;
    }}

    .stFileUploader {{
        background-color: rgba(30, 30, 50, 0.85) !important;
        border: 1px solid rgba(0, 119, 182, 0.2) !important;
        border-radius: 12px !important;
    }}

    /* Info/success/warning boxes */
    .stInfo {{
        background-color: rgba(0, 119, 182, 0.1) !important;
        border: 1px solid rgba(0, 119, 182, 0.2) !important;
        color: {TEXT_GRAY} !important;
    }}

    .stSuccess {{
        background-color: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        color: #10b981 !important;
    }}

    .stWarning {{
        background-color: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        color: #ef4444 !important;
    }}

    /* Expander */
    .st-expander {{
        background-color: rgba(30, 30, 50, 0.85) !important;
        border: 1px solid rgba(0, 119, 182, 0.2) !important;
        border-radius: 12px !important;
    }}

    /* Dividers */
    hr {{
        border-color: rgba(0, 119, 182, 0.2) !important;
    }}

    /* Markdown text */
    p, li {{
        color: {TEXT_GRAY} !important;
    }}

    /* Dataframes */
    .stDataFrame {{
        background-color: rgba(30, 30, 50, 0.85) !important;
        border: 1px solid rgba(0, 119, 182, 0.2) !important;
        border-radius: 12px !important;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: {DARK_CARD} !important;
        border-bottom: 1px solid rgba(0, 119, 182, 0.2) !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        color: {TEXT_GRAY} !important;
    }}

    .stTabs [aria-selected="true"] {{
        color: {ELECTRIC_BLUE_LIGHT} !important;
    }}

    /* Footer override */
    footer {{
        color: {TEXT_MUTED} !important;
    }}

    /* Data table styling */
    .dataframe {{
        color: {TEXT_WHITE} !important;
    }}

    /* File uploader text */
    .stFileUploader p {{
        color: {TEXT_GRAY} !important;
    }}

    /* Spinner override */
    .stSpinner > div {{
        border-top-color: {ELECTRIC_BLUE} !important;
    }}

    /* Text area */
    .stTextArea textarea {{
        background-color: rgba(18, 18, 26, 0.8) !important;
        border-color: rgba(0, 119, 182, 0.2) !important;
        color: {TEXT_WHITE} !important;
    }}
</style>
""", unsafe_allow_html=True)


# ============================================================================
# SESSION STATE INIT
# ============================================================================
if 'customer_df' not in st.session_state:
    st.session_state.customer_df = None
if 'uploaded_filename' not in st.session_state:
    st.session_state.uploaded_filename = None


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
    """Generate dashboard analytics data using the real dataset if available."""
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
        'churned': int(len(churned)),
        'retained': int(len(retained)),
        'churn_rate': round(len(churned) / len(df) * 100, 1),
        'active_members': int(df['IsActiveMember'].sum()),
        'avg_age': float(round(df['Age'].mean(), 1)),
        'avg_balance': float(round(df['Balance'].mean(), 2)),
        'avg_credit_score': float(round(df['CreditScore'].mean(), 1)),
        'geo_counts': geo_counts,
        'churn_by_geo': churn_by_geo,
        'age_dist': age_dist,
        'has_credit_card': int(df['HasCrCard'].sum()),
        'no_credit_card': int(len(df) - df['HasCrCard'].sum()),
        'dataset_source': 'Churn_Modelling.csv' if os.path.exists(DATASET_PATH) else 'Synthetic',
    }


@st.cache_data
def get_feature_importances():
    """Get feature importances from the trained model."""
    model, _, _, _ = load_model_artifacts()
    if model is None:
        return None
    feature_names = [
        'CreditScore', 'Geography', 'Gender', 'Age',
        'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard',
        'IsActiveMember', 'EstimatedSalary'
    ]
    fi_path = os.path.join(MODEL_DIR, 'feature_importances.csv')
    if os.path.exists(fi_path):
        df = pd.read_csv(fi_path)
        return df.to_dict('records')
    importances = model.feature_importances_
    data = [
        {'feature': name, 'importance': float(imp)}
        for name, imp in sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)
    ]
    return data


def predict_customer(model, scaler, label_geo, label_gender, row):
    """Run prediction on a single customer row."""
    geo_encoded = label_geo.transform([row['Geography']])[0]
    gender_encoded = label_gender.transform([row['Gender']])[0]
    features = np.array([[
        float(row['CreditScore']), geo_encoded, gender_encoded,
        float(row['Age']), float(row['Tenure']), float(row['Balance']),
        float(row['NumOfProducts']), float(row['HasCrCard']),
        float(row['IsActiveMember']), float(row['EstimatedSalary'])
    ]])
    features_scaled = scaler.transform(features)
    prob = float(model.predict_proba(features_scaled)[0][1])
    pred = int(model.predict(features_scaled)[0])
    return pred, prob


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

st.session_state.lang = selected_lang


# ============================================================================
# NAVIGATION
# ============================================================================
st.sidebar.divider()
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "📊 Dashboard", "🔮 Predict", "👥 Customers", "ℹ️ About"],
    index=0
)

page_map = {
    "🏠 Home": "home",
    "📊 Dashboard": "dashboard",
    "🔮 Predict": "predict",
    "👥 Customers": "customers",
    "ℹ️ About": "about",
}

current_page = page_map[page]


# ============================================================================
# COMMON UTILITIES
# ============================================================================
def get_customer_dataframe(n_samples=5000):
    """Get the customer dataframe, using session state cache if available."""
    if st.session_state.customer_df is not None:
        return st.session_state.customer_df
    df = generate_sample_data(n_samples)
    st.session_state.customer_df = df
    return df


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

    with col2:
        st.markdown(f"""
        <div style="background-color: rgba(30, 30, 50, 0.85); border: 1px solid rgba(0, 119, 182, 0.2); border-radius: 16px; padding: 24px;">
            <h4 style="color: {ELECTRIC_BLUE_LIGHT}; margin-top: 0;">✨ Key Features</h4>
            <ul style="list-style: none; padding: 0;">
                <li style="margin-bottom: 12px;">🤖 <strong style="color: {TEXT_WHITE};">Real-time AI</strong> churn predictions</li>
                <li style="margin-bottom: 12px;">🌍 <strong style="color: {TEXT_WHITE};">Multi-language</strong> support (English, Hindi, Telugu)</li>
                <li style="margin-bottom: 12px;">📈 <strong style="color: {TEXT_WHITE};">Comprehensive</strong> analytics dashboard</li>
                <li style="margin-bottom: 12px;">🎯 <strong style="color: {TEXT_WHITE};">Feature importance</strong> analysis</li>
                <li style="margin-bottom: 12px;">👥 <strong style="color: {TEXT_WHITE};">Customer directory</strong> with search & filter</li>
                <li style="margin-bottom: 12px;">📂 <strong style="color: {TEXT_WHITE};">Upload your own</strong> dataset for analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<p style='text-align: center; color: {TEXT_MUTED};'>{get_text(lang, 'footer_text')}</p>", unsafe_allow_html=True)


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

    # Show dataset source info
    source = data.get('dataset_source', 'Synthetic')
    st.info(f"📂 Dataset: **{source}** | {len(df)} customers loaded")

    # Dataset upload section
    with st.expander("📂 Upload Your Own Dataset", expanded=False):
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type="csv",
            help="Required columns: CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary"
        )
        if uploaded_file is not None:
            try:
                upload_df = pd.read_csv(uploaded_file)
                required_cols = ['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure',
                                 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
                missing = [c for c in required_cols if c not in upload_df.columns]
                if missing:
                    st.error(f"Missing columns: {', '.join(missing)}")
                else:
                    # Add CustomerName if not present
                    if 'CustomerName' not in upload_df.columns and 'Surname' in upload_df.columns:
                        upload_df['CustomerName'] = upload_df['Surname']
                    elif 'CustomerName' not in upload_df.columns:
                        upload_df['CustomerName'] = generate_customer_names(len(upload_df))

                    # Run predictions
                    model, scaler, label_geo, label_gender = load_model_artifacts()
                    if model is not None:
                        with st.spinner("Processing dataset..."):
                            predictions = []
                            for _, row in upload_df.iterrows():
                                try:
                                    pred, prob = predict_customer(model, scaler, label_geo, label_gender, row)
                                    predictions.append(pred)
                                except Exception:
                                    predictions.append(0)
                            upload_df['Exited'] = predictions
                            upload_df['ChurnProbability'] = [f"{prob:.1f}%" for prob in upload_df.get('Exited', [0])]

                        st.session_state.customer_df = upload_df
                        st.session_state.uploaded_filename = uploaded_file.name
                        churned_count = int(upload_df['Exited'].sum())
                        total = len(upload_df)
                        st.success(f"✅ {total} customers processed! {churned_count} at risk ({round(churned_count/total*100, 1)}%). Navigate to Customers page to browse.")
                        st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

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
    tab1, tab2 = st.tabs(["📊 Charts", "📈 Feature Importance"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            # Churn distribution
            churn_data = pd.DataFrame({
                'Status': [get_text(lang, 'dashboard_retained'), get_text(lang, 'dashboard_churned')],
                'Count': [data['retained'], data['churned']]
            })
            fig = px.pie(churn_data, values='Count', names='Status',
                         title=get_text(lang, 'chart_churn_dist'),
                         color_discrete_map={'Retained': '#10b981', 'Churned': '#ef4444'})
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color=TEXT_WHITE,
                title_font_color=TEXT_WHITE,
            )
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
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color=TEXT_WHITE,
                title_font_color=TEXT_WHITE,
            )
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
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color=TEXT_WHITE,
                    title_font_color=TEXT_WHITE,
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Credit card distribution
            cc_data = pd.DataFrame({
                'Status': [get_text(lang, 'yes'), get_text(lang, 'no')],
                'Count': [data['has_credit_card'], data['no_credit_card']]
            })
            fig = px.pie(cc_data, values='Count', names='Status',
                         title="Credit Card Distribution",
                         color_discrete_map={'Yes': '#00b4d8', 'No': '#6b7280'})
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color=TEXT_WHITE,
                title_font_color=TEXT_WHITE,
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader(get_text(lang, 'chart_feature_importance'))
        fi_data = get_feature_importances()
        if fi_data:
            fi_df = pd.DataFrame(fi_data)
            fig = px.bar(fi_df, x='importance', y='feature',
                         orientation='h',
                         title="Feature Importance",
                         color='importance', color_continuous_scale='Blues')
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color=TEXT_WHITE,
                title_font_color=TEXT_WHITE,
                yaxis={'categoryorder': 'total ascending'},
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)

            with st.expander("📋 View Raw Importance Data"):
                st.dataframe(fi_df, use_container_width=True)


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
                st.metric(
                    "Risk Level",
                    "🔴 HIGH" if prediction == 1 else "🟢 LOW"
                )

            # Display message
            if prediction == 1:
                st.warning(get_text(lang, 'predict_risk_high'))
            else:
                st.success(get_text(lang, 'predict_risk_low'))

            # Display top risk factors based on feature importances
            fi_data = get_feature_importances()
            if fi_data:
                st.markdown("---")
                st.markdown("### ⚠️ Key Risk Factors")
                # Map input values to risk
                risk_factors = []
                if age > 50:
                    risk_factors.append(f"• **Age ({age})** - Customers over 50 have higher churn risk")
                if balance > 100000:
                    risk_factors.append(f"• **Balance (${balance:,.0f})** - High balance customers may churn")
                if is_active_member == 0:
                    risk_factors.append("• **Inactive Member** - Inactive members are more likely to churn")
                if num_products > 2:
                    risk_factors.append(f"• **{num_products} Products** - Customers with 3+ products show higher churn")
                if credit_score < 500:
                    risk_factors.append(f"• **Credit Score ({credit_score})** - Low credit score increases churn risk")
                if geography == 'Germany':
                    risk_factors.append("• **Germany** - German customers have higher churn rates")

                if risk_factors:
                    for factor in risk_factors:
                        st.markdown(factor)
                else:
                    st.markdown("*No major risk factors identified*")

        except Exception as e:
            st.error(f"Error making prediction: {e}")


# ============================================================================
# PAGE: CUSTOMERS
# ============================================================================
def show_customers():
    """Customer directory page with search and filter."""
    lang = st.session_state.get('lang', 'en')

    st.title("👥 Customer Directory")
    st.markdown("Search for a customer by name or filter by geography and churn status.")

    # Load customer data
    df = get_customer_dataframe()

    # Show upload info
    if st.session_state.uploaded_filename:
        st.info(f"📂 Currently using uploaded dataset: **{st.session_state.uploaded_filename}**")

    # Dataset upload
    with st.expander("📂 Upload Your Own Dataset", expanded=False):
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type="csv",
            key="customer_upload",
            help="Required columns: CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary"
        )
        if uploaded_file is not None:
            try:
                upload_df = pd.read_csv(uploaded_file)
                required_cols = ['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure',
                                 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
                missing = [c for c in required_cols if c not in upload_df.columns]
                if missing:
                    st.error(f"Missing columns: {', '.join(missing)}")
                else:
                    if 'CustomerName' not in upload_df.columns and 'Surname' in upload_df.columns:
                        upload_df['CustomerName'] = upload_df['Surname']
                    elif 'CustomerName' not in upload_df.columns:
                        upload_df['CustomerName'] = generate_customer_names(len(upload_df))

                    model, scaler, label_geo, label_gender = load_model_artifacts()
                    if model is not None:
                        with st.spinner("Processing dataset..."):
                            predictions = []
                            for _, row in upload_df.iterrows():
                                try:
                                    pred, prob = predict_customer(model, scaler, label_geo, label_gender, row)
                                    predictions.append({'exited': pred, 'probability': prob})
                                except Exception:
                                    predictions.append({'exited': 0, 'probability': 0.0})
                            upload_df['Exited'] = [p['exited'] for p in predictions]
                            upload_df['ChurnProbability'] = [f"{p['probability']*100:.1f}%" for p in predictions]

                        st.session_state.customer_df = upload_df
                        st.session_state.uploaded_filename = uploaded_file.name
                        churned_count = int(upload_df['Exited'].sum())
                        total = len(upload_df)
                        st.success(f"✅ {total} customers processed! {churned_count} at risk ({round(churned_count/total*100, 1)}%).")
                        st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")

    # Search and filter
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        search_query = st.text_input("🔍 Search by name", placeholder="Enter customer name...")

    with col2:
        geo_filter = st.selectbox("🌍 Geography", ["All", "France", "Spain", "Germany"])

    with col3:
        status_filter = st.selectbox("📊 Status", ["All", "Retained", "Churned"])

    # Apply filters
    filtered = df.copy()

    if search_query:
        filtered = filtered[filtered['CustomerName'].str.lower().str.contains(search_query.lower(), na=False)]

    if geo_filter != "All":
        filtered = filtered[filtered['Geography'] == geo_filter]

    if status_filter == "Retained":
        filtered = filtered[filtered['Exited'] == 0]
    elif status_filter == "Churned":
        filtered = filtered[filtered['Exited'] == 1]

    st.markdown(f"**{len(filtered)} customers found**")

    if len(filtered) > 0:
        # Prepare display dataframe
        display_df = filtered[['CustomerName', 'Age', 'Geography', 'CreditScore', 'Balance',
                                'NumOfProducts', 'IsActiveMember', 'Tenure', 'Exited']].copy()
        display_df['Balance'] = display_df['Balance'].apply(lambda x: f"${x:,.2f}")
        display_df['Status'] = display_df['Exited'].apply(lambda x: "🔴 Churned" if x == 1 else "🟢 Retained")
        display_df['Active'] = display_df['IsActiveMember'].apply(lambda x: "✅ Yes" if x == 1 else "❌ No")
        display_df = display_df.rename(columns={
            'CustomerName': 'Name',
            'CreditScore': 'Credit Score',
            'NumOfProducts': 'Products',
            'IsActiveMember': 'Active',
        })
        display_df = display_df.drop(columns=['Exited'])

        st.dataframe(display_df, use_container_width=True, height=min(600, 40 * len(display_df) + 40))
    else:
        st.info("No customers match your search criteria.")


# ============================================================================
# PAGE: ABOUT
# ============================================================================
def show_about():
    """About page."""
    lang = st.session_state.get('lang', 'en')

    st.title(f"ℹ️ {get_text(lang, 'about_title')}")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"""
        {get_text(lang, 'about_desc')}

        ### {get_text(lang, 'about_features')}
        - ✅ {get_text(lang, 'about_feature1')}
        - ✅ {get_text(lang, 'about_feature2')}
        - ✅ {get_text(lang, 'about_feature3')}
        - ✅ {get_text(lang, 'about_feature4')}
        - ✅ **Customer directory** with search and filter
        - ✅ **Dataset upload** for custom analysis

        ---

        {get_text(lang, 'about_team')}
        """)

    with col2:
        # Model info card
        st.markdown(f"""
        <div style="background-color: rgba(30, 30, 50, 0.85); border: 1px solid rgba(0, 119, 182, 0.2); border-radius: 16px; padding: 24px;">
            <h4 style="color: {ELECTRIC_BLUE_LIGHT}; margin-top: 0;">Model Details</h4>
            <div style="margin-bottom: 12px;">
                <span style="color: {TEXT_MUTED};">Algorithm</span><br>
                <strong style="color: {TEXT_WHITE};">Random Forest</strong>
            </div>
            <div style="margin-bottom: 12px;">
                <span style="color: {TEXT_MUTED};">Estimators</span><br>
                <strong style="color: {TEXT_WHITE};">200</strong>
            </div>
            <div style="margin-bottom: 12px;">
                <span style="color: {TEXT_MUTED};">Max Depth</span><br>
                <strong style="color: {TEXT_WHITE};">15</strong>
            </div>
            <div style="margin-bottom: 12px;">
                <span style="color: {TEXT_MUTED};">Training Data</span><br>
                <strong style="color: {TEXT_WHITE};">{len(pd.read_csv(DATASET_PATH)) if os.path.exists(DATASET_PATH) else 5000} samples</strong>
            </div>
            <div>
                <span style="color: {TEXT_MUTED};">Data Source</span><br>
                <strong style="color: {TEXT_WHITE};">{'Churn_Modelling.csv' if os.path.exists(DATASET_PATH) else 'Synthetic'}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# PAGE ROUTING
# ============================================================================
if current_page == "home":
    show_home()
elif current_page == "dashboard":
    show_dashboard()
elif current_page == "predict":
    show_predict()
elif current_page == "customers":
    show_customers()
elif current_page == "about":
    show_about()