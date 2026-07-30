import streamlit as st
import pandas as pd
import plotly.express as px
from utils.auth import require_auth
from utils.db import get_session, PredictionHistory
from utils.theme import apply_custom_theme
import os

st.set_page_config(
    page_title="Dashboard | AI Career Navigator",
    page_icon="📊",
    layout="wide"
)

apply_custom_theme()
require_auth()

st.markdown(f"""
<div style="margin-bottom: 2rem;">
    <h1 class="gradient-header" style="font-size: 2.6rem;">Welcome back, {st.session_state['name']}! 👋</h1>
    <p style="color: #94A3B8; font-size: 1.05rem;">
        Logged in as <b style="color: #818CF8;">{st.session_state['username']}</b> ({st.session_state['role'].capitalize()})
    </p>
</div>
""", unsafe_allow_html=True)

# Main Metrics Row
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Placement Model Accuracy")
    if os.path.exists('models/clf_metrics.csv'):
        clf_df = pd.read_csv('models/clf_metrics.csv')
        fig = px.bar(clf_df, x='Model', y='Accuracy', title='Placement Classification Models', color='Accuracy', color_continuous_scale='Viridis', text_auto='.2%')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#F8FAFC"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Classification metrics not available. Train the models first.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 💰 Salary Model Performance")
    if os.path.exists('models/reg_metrics.csv'):
        reg_df = pd.read_csv('models/reg_metrics.csv')
        fig2 = px.bar(reg_df, x='Model', y='R2_Score', title='Salary Regression Models (R2 Score)', color='R2_Score', color_continuous_scale='Magma', text_auto='.2f')
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#F8FAFC"))
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Regression metrics not available. Train the models first.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### 📜 Your Recent Prediction History")

session = get_session()
history = session.query(PredictionHistory).filter_by(username=st.session_state['username']).order_by(PredictionHistory.timestamp.desc()).limit(10).all()
session.close()

if history:
    data = []
    for h in history:
        data.append({
            "Timestamp": h.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "Prediction Type": h.prediction_type,
            "Result": h.result
        })
    df_history = pd.DataFrame(data)
    st.dataframe(df_history, use_container_width=True)
else:
    st.info("You haven't made any predictions yet. Head over to Placement or Salary Predictor to get started!")

st.markdown('</div>', unsafe_allow_html=True)
