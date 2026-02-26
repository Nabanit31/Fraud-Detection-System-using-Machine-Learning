import streamlit as st
import pandas as pd
import joblib
import time

# 1. Page Configuration
st.set_page_config(
    page_title="FraudGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS for Animations and Premium Feel
st.markdown("""
<style>
    /* Glowing title */
    .title-glow {
        font-family: 'Inter', sans-serif;
        background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem !important;
        margin-bottom: 0rem;
    }
    
    /* Subtitle styling */
    .subtitle {
        color: #8fa3b0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Animated Button Hover */
    .stButton>button {
        transition: all 0.3s ease;
        border-radius: 8px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 210, 255, 0.4);
    }
    
    /* Result Box Animations */
    .fraud-box {
        background: rgba(255, 65, 108, 0.1);
        border: 1px solid rgba(255, 65, 108, 0.3);
        border-left: 5px solid #ff416c;
        padding: 20px;
        border-radius: 8px;
        animation: pulse-red 2s infinite;
    }
    .safe-box {
        background: rgba(0, 210, 255, 0.1);
        border: 1px solid rgba(0, 210, 255, 0.3);
        border-left: 5px solid #00d2ff;
        padding: 20px;
        border-radius: 8px;
        animation: fade-in 0.5s ease-out;
    }
    
    @keyframes pulse-red {
        0% { box-shadow: 0 0 0 0 rgba(255,65,108, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(255,65,108, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255,65,108, 0); }
    }
    
    @keyframes fade-in {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    /* Card-like containers for inputs */
    .css-1r6slb0, .css-12oz5g7 {
        background-color: #15232d;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

# 3. Cached Model Loading for Performance
@st.cache_resource(show_spinner="Loading Security Models...")
def load_model():
    return joblib.load("fraud_detection_pipeline.pkl")

try:
    model = load_model()
except Exception as e:
    st.error(f"Error initializing AI Engine: {e}")
    st.stop()

# 4. Header Section
st.markdown('<h1 class="title-glow">🛡️ FraudGuard AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Next-Generation Financial Transaction Monitoring & Anomaly Detection</p>', unsafe_allow_html=True)
st.write("---")

# 5. Input Forms in Columns
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 📋 Transaction Details")
    transaction_type = st.selectbox(
        "Transaction Type",
        ["PAYMENT", "TRANSFER", "CASH_OUT", "CASH_IN", "DEBIT"],
        help="Select the classification of the current transaction."
    )
    
    amount = st.number_input("Transaction Amount ($)", min_value=0.0, value=1500.0, step=100.0)

with col2:
    st.markdown("### 🏦 Entity Balances")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Sender (\u2191)**")
        oldbalanceOrg = st.number_input("Initial Balance", min_value=0.0, value=50000.0, key="ob_org")
        newbalanceOrig = st.number_input("New Balance", min_value=0.0, value=48500.0, key="nb_org")
    with c2:
        st.markdown("**Receiver (\u2193)**")
        oldbalanceDest = st.number_input("Initial Balance", min_value=0.0, value=10000.0, key="ob_dest")
        newbalanceDest = st.number_input("New Balance", min_value=0.0, value=11500.0, key="nb_dest")

st.write("---")

# 6. Prediction Area
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    predict_clicked = st.button("🔍 Analyze Transaction Risk", use_container_width=True, type="primary")

if predict_clicked:
    # Gather inputs
    input_data = pd.DataFrame([{
        "type": transaction_type,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest
    }])

    # Simulated loading effect for "AI Processing" user experience
    with st.spinner("Neural networks analyzing transaction parameters..."):
        time.sleep(0.8) # Artificial delay to make it feel like "heavy processing"
        try:
            prediction = model.predict(input_data)[0]
        except Exception as e:
            st.error(f"Prediction failed: {e}")
            prediction = None
    
    st.write("") # Spacer
    
    if prediction is not None:
        if prediction == 1:
            st.markdown("""
            <div class="fraud-box">
                <h3 style='margin:0; color:#ff416c;'>⚠️ CRITICAL: FRAUD DETECTED</h3>
                <p style='margin-top:8px; font-size:16px; color:#e0e6ed;'>
                The AI model has flagged this transaction as highly anomalous.
                Immediate action is required to verify the sender's identity and freeze the transfer of funds. 
                Patterns match known fraudulent behavioral profiles.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="safe-box">
                <h3 style='margin:0; color:#00d2ff;'>✅ TRANSACTION VERIFIED SECURE</h3>
                <p style='margin-top:8px; font-size:16px; color:#e0e6ed;'>
                All neural network parameters indicate this transaction follows standard behavioral patterns. 
                No structural anomalies detected. Safe to proceed.
                </p>
            </div>
            """, unsafe_allow_html=True)