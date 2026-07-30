import streamlit as st
import joblib
import os
import pandas as pd
from utils.auth import require_auth
from utils.db import get_session, PredictionHistory
from utils.theme import apply_custom_theme

st.set_page_config(
    page_title="Salary Predictor | AI Career Navigator",
    page_icon="💰",
    layout="wide"
)

apply_custom_theme()
require_auth()

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 class="gradient-header" style="font-size: 2.8rem; margin-bottom: 0.5rem;">💰 AI Salary Estimator</h1>
    <p style="color: #94A3B8; font-size: 1.1rem; max-width: 700px; margin: 0 auto;">
        Estimate your expected annual salary package (CTC) based on academic excellence, project portfolio, and coding skills.
    </p>
</div>
""", unsafe_allow_html=True)

model_path = 'models/best_salary_model.pkl'

@st.cache_resource
def load_model():
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

model = load_model()

if model is None:
    st.error("⚠️ Salary model not found. Please ask an Administrator to train models in the Admin Panel.")
else:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    with st.form("salary_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            cgpa = st.number_input("CGPA (out of 10.0)", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
            attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, value=85.0, step=1.0)
            aptitude = st.number_input("Aptitude Score (out of 100)", min_value=0, max_value=100, value=75)
            
        with col2:
            coding = st.number_input("Coding Score (out of 100)", min_value=0, max_value=100, value=85)
            communication = st.number_input("Communication Score (out of 100)", min_value=0, max_value=100, value=80)
            projects = st.number_input("Number of Projects", min_value=0, max_value=20, value=4)
            
        submit = st.form_submit_button("💰 Predict Annual Package")
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    if submit:
        input_data = pd.DataFrame([[cgpa, attendance, aptitude, coding, communication, projects]],
                                  columns=['CGPA', 'Attendance', 'Aptitude_Score', 'Coding_Score', 'Communication_Score', 'Number_of_Projects'])
        
        try:
            prediction = model.predict(input_data)[0]
            prediction = max(200000, prediction) # Floor salary to realistic range
            lpa = prediction / 100000.0
            
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 💵 Estimated Annual Compensation")
            
            sc1, sc2 = st.columns(2)
            with sc1:
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: #F59E0B;">
                    <div class="stat-title">Estimated CTC Package</div>
                    <div class="stat-value" style="color: #FBBF24;">₹{prediction:,.0f} / yr</div>
                    <div style="font-size: 0.9rem; color: #CBD5E1; margin-top: 4px;">Approx. <b>{lpa:.2f} LPA</b></div>
                </div>
                """, unsafe_allow_html=True)
                
            with sc2:
                monthly = prediction / 12.0
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: #10B981;">
                    <div class="stat-title">Estimated Monthly In-Hand</div>
                    <div class="stat-value" style="color: #34D399;">₹{monthly:,.0f} / mo</div>
                    <div style="font-size: 0.9rem; color: #CBD5E1; margin-top: 4px;">Gross base estimate</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Save to database history
            session = get_session()
            hist = PredictionHistory(
                username=st.session_state['username'],
                prediction_type="Salary",
                result=f"₹{prediction:,.0f} ({lpa:.2f} LPA)"
            )
            session.add(hist)
            session.commit()
            session.close()
            
        except Exception as e:
            st.error(f"Error calculating salary prediction: {e}")
