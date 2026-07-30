import streamlit as st
import joblib
import os
import pandas as pd
import plotly.graph_objects as go
from utils.auth import require_auth
from utils.db import get_session, PredictionHistory
from utils.theme import apply_custom_theme

st.set_page_config(
    page_title="Placement Predictor | AI Career Navigator",
    page_icon="🎯",
    layout="wide"
)

apply_custom_theme()
require_auth()

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 class="gradient-header" style="font-size: 2.8rem; margin-bottom: 0.5rem;">🎯 AI Placement Predictor</h1>
    <p style="color: #94A3B8; font-size: 1.1rem; max-width: 700px; margin: 0 auto;">
        Input your academic, coding, and aptitude metrics below to calculate your estimated campus placement probability.
    </p>
</div>
""", unsafe_allow_html=True)

model_path = 'models/best_placement_model.pkl'

@st.cache_resource
def load_model():
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

model = load_model()

if model is None:
    st.error("⚠️ Placement model not found. Please ask an Administrator to train models in the Admin Panel.")
else:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    with st.form("placement_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            cgpa = st.number_input("CGPA (out of 10.0)", min_value=0.0, max_value=10.0, value=7.8, step=0.1)
            attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, value=85.0, step=1.0)
            aptitude = st.number_input("Aptitude Score (out of 100)", min_value=0, max_value=100, value=75)
            
        with col2:
            coding = st.number_input("Coding Assessment Score (out of 100)", min_value=0, max_value=100, value=80)
            communication = st.number_input("Communication Score (out of 100)", min_value=0, max_value=100, value=75)
            projects = st.number_input("Number of Completed Projects", min_value=0, max_value=20, value=3)
            
        submit = st.form_submit_button("🚀 Calculate Placement Probability")
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    if submit:
        input_data = pd.DataFrame([[cgpa, attendance, aptitude, coding, communication, projects]],
                                  columns=['CGPA', 'Attendance', 'Aptitude_Score', 'Coding_Score', 'Communication_Score', 'Number_of_Projects'])
        
        try:
            prob = model.predict_proba(input_data)[0][1] * 100
            prediction = model.predict(input_data)[0]
            
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📊 Prediction Results")
            
            res_col1, res_col2 = st.columns([1, 1])
            
            with res_col1:
                color = "#34D399" if prob >= 60 else "#F87171"
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: {color};">
                    <div class="stat-title">Estimated Placement Probability</div>
                    <div class="stat-value" style="color: {color};">{prob:.1f}%</div>
                    <div style="font-size: 0.9rem; margin-top: 5px; color: #CBD5E1;">
                        Status: <b>{'High Chance of Placement' if prediction == 1 else 'Needs Profile Enhancement'}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if prediction == 1:
                    st.success("🎉 Outstanding metrics! You are in a strong position for upcoming campus placements.")
                else:
                    st.warning("💪 Focus on improving coding scores and completing 1-2 more key projects to boost your chances.")

            with res_col2:
                fig_g = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = prob,
                    title = {'text': "Placement Probability", 'font': {'size': 14, 'color': "#94A3B8"}},
                    gauge = {
                        'axis': {'range': [0, 100]},
                        'bar': {'color': color},
                        'steps': [
                            {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.2)'},
                            {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.2)'},
                            {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.2)'}
                        ]
                    }
                ))
                fig_g.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#F8FAFC"), height=220, margin=dict(l=10, r=10, t=30, b=10))
                st.plotly_chart(fig_g, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)
                
            # Save to database history
            session = get_session()
            hist = PredictionHistory(
                username=st.session_state['username'],
                prediction_type="Placement",
                result=f"{'Placed' if prediction == 1 else 'Not Placed'} ({prob:.1f}%)"
            )
            session.add(hist)
            session.commit()
            session.close()
            
        except Exception as e:
            st.error(f"Error executing prediction: {e}")
