import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import subprocess
import os
import joblib
from utils.auth import require_auth, register_user, update_user_role, reset_user_password, delete_user
from utils.db import get_session, User, PredictionHistory, Feedback
from utils.theme import apply_custom_theme

# Page Configuration
st.set_page_config(
    page_title="Admin Panel | AI Career Navigator",
    page_icon="⚙️",
    layout="wide"
)

apply_custom_theme()
require_auth(allowed_roles=['admin'])

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 class="gradient-header" style="font-size: 2.8rem; margin-bottom: 0.5rem;">⚙️ Administrator Control Center</h1>
    <p style="color: #94A3B8; font-size: 1.1rem; max-width: 700px; margin: 0 auto;">
        Manage registered platform users, monitor prediction analytics, retrain ML models, and maintain system health.
    </p>
</div>
""", unsafe_allow_html=True)

# Fetch Top Platform Stats
session = get_session()
total_users = session.query(User).count()
total_students = session.query(User).filter_by(role='student').count()
total_admins = session.query(User).filter_by(role='admin').count()
total_predictions = session.query(PredictionHistory).count()
placement_count = session.query(PredictionHistory).filter_by(prediction_type='Placement').count()
salary_count = session.query(PredictionHistory).filter_by(prediction_type='Salary').count()
total_feedback = session.query(Feedback).count()
session.close()

# Stat Summary Bar
col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
with col_s1:
    st.markdown(f"""
    <div class="stat-card" style="border-left-color: #6366F1;">
        <div class="stat-title">Total Users</div>
        <div class="stat-value">{total_users}</div>
        <div style="font-size: 0.8rem; color: #94A3B8;">{total_students} Students | {total_admins} Admins</div>
    </div>
    """, unsafe_allow_html=True)

with col_s2:
    st.markdown(f"""
    <div class="stat-card" style="border-left-color: #A855F7;">
        <div class="stat-title">Total Predictions</div>
        <div class="stat-value">{total_predictions}</div>
        <div style="font-size: 0.8rem; color: #94A3B8;">Executed on platform</div>
    </div>
    """, unsafe_allow_html=True)

with col_s3:
    st.markdown(f"""
    <div class="stat-card" style="border-left-color: #10B981;">
        <div class="stat-title">Placement Queries</div>
        <div class="stat-value">{placement_count}</div>
        <div style="font-size: 0.8rem; color: #94A3B8;">Probability checks</div>
    </div>
    """, unsafe_allow_html=True)

with col_s4:
    st.markdown(f"""
    <div class="stat-card" style="border-left-color: #F59E0B;">
        <div class="stat-title">Salary Predictions</div>
        <div class="stat-value">{salary_count}</div>
        <div style="font-size: 0.8rem; color: #94A3B8;">Package estimations</div>
    </div>
    """, unsafe_allow_html=True)

with col_s5:
    st.markdown(f"""
    <div class="stat-card" style="border-left-color: #EC4899;">
        <div class="stat-title">ML Model Status</div>
        <div class="stat-value" style="font-size: 1.2rem; margin-top: 10px;">
            <span class="pulse-dot"></span> Active
        </div>
        <div style="font-size: 0.8rem; color: #94A3B8;">v1.2 Trained</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "👥 User Management",
    "📈 Analytics & Activity Logs",
    "🤖 Machine Learning Models",
    "💬 Feedback & System Health"
])

# ----------------- TAB 1: USER MANAGEMENT -----------------
with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("👥 Registered User Accounts")
    
    session = get_session()
    users_list = session.query(User).all()
    session.close()

    if users_list:
        users_df = pd.DataFrame([{"ID": u.id, "Username": u.username, "Full Name": u.name, "Role": u.role.capitalize()} for u in users_list])
        
        search_query = st.text_input("🔍 Search user by name or username:", placeholder="Type username...")
        if search_query:
            users_df = users_df[users_df['Username'].str.contains(search_query, case=False) | users_df['Full Name'].str.contains(search_query, case=False)]

        st.dataframe(users_df, use_container_width=True)
    else:
        st.info("No registered users found in the database.")

    st.markdown("---")
    
    # User Control Actions (Create, Update Role, Reset Password, Delete)
    col_u1, col_u2 = st.columns(2)
    
    with col_u1:
        st.markdown("#### ➕ Create New User Account")
        with st.form("admin_create_user_form"):
            new_name = st.text_input("Full Name")
            new_username = st.text_input("Username")
            new_pass = st.text_input("Password", type="password")
            new_role = st.selectbox("Assign Role", ["student", "admin"])
            submitted = st.form_submit_button("Create Account")
            if submitted:
                if len(new_username) < 3 or len(new_pass) < 4:
                    st.error("Username (min 3 chars) and Password (min 4 chars) are required.")
                else:
                    ok, msg = register_user(new_username, new_name, new_pass, new_role)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

    with col_u2:
        st.markdown("#### ⚡ Admin User Actions")
        action_type = st.radio("Select Action:", ["Change User Role", "Reset User Password", "Delete Account"], horizontal=True)
        
        all_usernames = [u.username for u in users_list] if users_list else []
        selected_user = st.selectbox("Select Target Account:", options=all_usernames) if all_usernames else None
        
        if selected_user:
            if action_type == "Change User Role":
                target_role = st.selectbox("Select New Role:", ["student", "admin"])
                if st.button("Apply Role Change"):
                    ok, msg = update_user_role(selected_user, target_role)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                        
            elif action_type == "Reset User Password":
                reset_pass = st.text_input("New Password:", type="password", key="reset_pass_input")
                if st.button("Confirm Password Reset"):
                    if len(reset_pass) < 4:
                        st.error("Password must be at least 4 characters.")
                    else:
                        ok, msg = reset_user_password(selected_user, reset_pass)
                        if ok:
                            st.success(msg)
                        else:
                            st.error(msg)
                            
            elif action_type == "Delete Account":
                if selected_user == st.session_state['username']:
                    st.warning("⚠️ You cannot delete your own logged-in admin account.")
                else:
                    st.markdown(f"<span style='color: #F87171;'>Are you sure you want to permanently delete user <b>{selected_user}</b>?</span>", unsafe_allow_html=True)
                    if st.button("Confirm Delete User", type="primary"):
                        ok, msg = delete_user(selected_user)
                        if ok:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)

    st.markdown('</div>', unsafe_allow_html=True)


# ----------------- TAB 2: ANALYTICS & LOGS -----------------
with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📈 Platform Usage & Prediction Logs")
    
    session = get_session()
    history_records = session.query(PredictionHistory).order_by(PredictionHistory.timestamp.desc()).all()
    session.close()

    if history_records:
        history_df = pd.DataFrame([{
            "Log ID": h.id,
            "Username": h.username,
            "Type": h.prediction_type,
            "Result Summary": h.result,
            "Timestamp": h.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        } for h in history_records])

        # Charts Row
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            type_counts = history_df['Type'].value_counts().reset_index()
            type_counts.columns = ['Type', 'Count']
            fig_pie = px.pie(type_counts, values='Count', names='Type', title='Prediction Type Distribution', color_discrete_sequence=['#6366F1', '#EC4899'], hole=0.4)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#F8FAFC"))
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_c2:
            top_users = history_df['Username'].value_counts().reset_index().head(5)
            top_users.columns = ['Username', 'Activity Count']
            fig_bar = px.bar(top_users, x='Username', y='Activity Count', title='Top Active Students', color='Activity Count', color_continuous_scale='Purples')
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#F8FAFC"))
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("#### Complete Prediction History Records")
        st.dataframe(history_df, use_container_width=True)
        
        # CSV Export
        csv_data = history_df.to_csv(index=False)
        st.download_button(
            label="📥 Export Logs as CSV",
            data=csv_data,
            file_name="platform_prediction_logs.csv",
            mime="text/csv"
        )
    else:
        st.info("No prediction history recorded yet.")
        
    st.markdown('</div>', unsafe_allow_html=True)


# ----------------- TAB 3: MACHINE LEARNING MODELS -----------------
with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🤖 Machine Learning Model Performance & Retraining")
    
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        st.markdown("#### Placement Classification Models")
        if os.path.exists('models/clf_metrics.csv'):
            clf_df = pd.read_csv('models/clf_metrics.csv')
            fig_clf = px.bar(clf_df, x='Model', y='Accuracy', text_auto='.2%', title='Model Accuracy Comparison', color='Accuracy', color_continuous_scale='Viridis')
            fig_clf.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#F8FAFC"))
            st.plotly_chart(fig_clf, use_container_width=True)
        else:
            st.warning("No classification metrics found. Retrain models below.")

    with col_m2:
        st.markdown("#### Salary Regression Models")
        if os.path.exists('models/reg_metrics.csv'):
            reg_df = pd.read_csv('models/reg_metrics.csv')
            fig_reg = px.bar(reg_df, x='Model', y='R2_Score', text_auto='.2f', title='Model R2 Score Comparison', color='R2_Score', color_continuous_scale='Magma')
            fig_reg.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#F8FAFC"))
            st.plotly_chart(fig_reg, use_container_width=True)
        else:
            st.warning("No regression metrics found. Retrain models below.")

    # Feature Importance Section
    if os.path.exists('models/best_placement_model.pkl'):
        try:
            model = joblib.load('models/best_placement_model.pkl')
            if hasattr(model, 'feature_importances_'):
                features = ['CGPA', 'Attendance', 'Aptitude_Score', 'Coding_Score', 'Communication_Score', 'Number_of_Projects']
                importances = model.feature_importances_
                imp_df = pd.DataFrame({'Feature': features, 'Importance': importances}).sort_values('Importance', ascending=True)
                fig_imp = px.bar(imp_df, x='Importance', y='Feature', orientation='h', title='Feature Importance for Placement Model', color='Importance', color_continuous_scale='Teal')
                fig_imp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#F8FAFC"))
                st.plotly_chart(fig_imp, use_container_width=True)
        except Exception as e:
            pass

    st.markdown("---")
    
    # Dataset Generation & Retraining Controls
    st.markdown("#### ⚡ Retrain Pipeline Controls")
    ctl_col1, ctl_col2 = st.columns(2)
    
    with ctl_col1:
        st.markdown("##### 1. Generate Synthetic Training Data")
        sample_size = st.slider("Select Dataset Size (rows):", min_value=500, max_value=5000, value=1000, step=500)
        if st.button("⚡ Generate Dataset"):
            with st.spinner("Generating synthetic student records..."):
                try:
                    from data.generate_data import generate_data
                    generate_data(num_samples=sample_size)
                    st.success(f"Successfully generated dataset with {sample_size} records in `data/dataset.csv`!")
                except Exception as e:
                    st.error(f"Error generating data: {e}")

    with ctl_col2:
        st.markdown("##### 2. Execute Model Training")
        st.caption("Train Logistic Regression, Random Forest, XGBoost & SVM models on generated data.")
        if st.button("🚀 Retrain All ML Models"):
            with st.spinner("Training placement classification & salary regression models..."):
                try:
                    result = subprocess.run(["python", "models/train_model.py"], capture_output=True, text=True)
                    if result.returncode == 0:
                        st.success("🎉 ML Models trained, evaluated, and saved to `models/` directory!")
                        with st.expander("📄 View Detailed Training Execution Output"):
                            st.code(result.stdout)
                    else:
                        st.error(f"Training failed: {result.stderr}")
                except Exception as e:
                    st.error(f"Execution error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)


# ----------------- TAB 4: FEEDBACK & SYSTEM -----------------
with tab4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("💬 Student Feedback & Database Status")
    
    session = get_session()
    feedback_records = session.query(Feedback).order_by(Feedback.timestamp.desc()).all()
    session.close()

    if feedback_records:
        fb_df = pd.DataFrame([{
            "ID": fb.id,
            "Username": fb.username,
            "Rating ⭐": f"{fb.rating}/5",
            "Feedback Message": fb.feedback_text,
            "Submitted On": fb.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        } for fb in feedback_records])
        st.dataframe(fb_df, use_container_width=True)
    else:
        st.info("No feedback entries submitted by users yet.")

    st.markdown("---")
    st.markdown("#### 🛠️ System Health & Database Diagnostics")
    
    db_size = os.path.getsize('data/app.db') / 1024 if os.path.exists('data/app.db') else 0
    st.markdown(f"- **SQLite Database Path:** `data/app.db` ({db_size:.2f} KB)")
    st.markdown(f"- **Python Version:** {subprocess.getoutput('python --version')}")
    st.markdown(f"- **Streamlit Server Status:** Running (Port 8501)")
    
    st.markdown('</div>', unsafe_allow_html=True)
