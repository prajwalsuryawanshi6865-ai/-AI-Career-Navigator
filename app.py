import streamlit as st
from utils.auth import login_user, register_user, logout_user, ensure_default_users
from utils.theme import apply_custom_theme

st.set_page_config(
    page_title="AI Career Navigator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_theme()
ensure_default_users()

def show_landing_page():
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0 1.5rem 0;">
        <h1 class="gradient-header" style="font-size: 3.2rem; margin-bottom: 0.5rem;">🎓 AI Career Navigator</h1>
        <p style="color: #94A3B8; font-size: 1.25rem; font-weight: 500; max-width: 750px; margin: 0 auto;">
            Next-Generation AI & ML Platform for Student Placement Predictions, ATS Resume Analysis, & Salary Estimation.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: #818CF8; margin-top: 0;">✨ Core Features & Capabilities</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 15px;">
            <div style="background: rgba(15, 23, 42, 0.6); padding: 18px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
                <h4 style="color: #34D399; margin-top:0;">📄 ATS Resume Analyzer</h4>
                <p style="color: #CBD5E1; font-size: 0.92rem;">Upload your PDF resume to receive a real-time role-specific ATS match score, keyword breakdown, and actionable improvement recommendations.</p>
            </div>
            <div style="background: rgba(15, 23, 42, 0.6); padding: 18px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
                <h4 style="color: #60A5FA; margin-top:0;">🎯 Placement Predictor</h4>
                <p style="color: #CBD5E1; font-size: 0.92rem;">Leverage trained Machine Learning classifiers (XGBoost, Random Forest) to calculate your exact placement probability percentage.</p>
            </div>
            <div style="background: rgba(15, 23, 42, 0.6); padding: 18px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
                <h4 style="color: #F59E0B; margin-top:0;">💰 Salary Estimator</h4>
                <p style="color: #CBD5E1; font-size: 0.92rem;">Forecast your potential starting package based on CGPA, coding test scores, aptitude, and project experience metrics.</p>
            </div>
            <div style="background: rgba(15, 23, 42, 0.6); padding: 18px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
                <h4 style="color: #EC4899; margin-top:0;">⚙️ Admin Control Panel</h4>
                <p style="color: #CBD5E1; font-size: 0.92rem;">Comprehensive administrator portal to manage user permissions, monitor prediction logs, and trigger model retraining.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: #F8FAFC;">💡 About & Technology Stack</h3>
        <p style="color: #CBD5E1; line-height: 1.6;">
            <b>AI Career Navigator</b> is built using <b>Streamlit</b>, <b>scikit-learn</b>, <b>XGBoost</b>, <b>Plotly</b>, and <b>SQLite</b>. 
            All user authentication is encrypted using <b>bcrypt</b> password hashing.
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_auth():
    st.sidebar.markdown("### 🔐 User Portal")
    
    if st.session_state.get('logged_in', False):
        st.sidebar.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(52, 211, 153, 0.3); padding: 12px; border-radius: 10px; margin-bottom: 15px;">
            <div style="color: #34D399; font-weight: 700; font-size: 0.95rem;">Logged In</div>
            <div style="color: #F8FAFC; font-weight: 600;">{st.session_state['name']}</div>
            <div style="color: #94A3B8; font-size: 0.82rem; text-transform: uppercase;">Role: {st.session_state['role']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.sidebar.button("Logout Account"):
            logout_user()
            st.rerun()
    else:
        st.sidebar.markdown("**⚡ 1-Click Demo Login:**")
        col_sb1, col_sb2 = st.sidebar.columns(2)
        with col_sb1:
            if st.button("⚙️ Admin"):
                login_user('admin', 'admin')
                st.rerun()
        with col_sb2:
            if st.button("🎓 Student"):
                login_user('student', 'student')
                st.rerun()
                
        st.sidebar.divider()
        auth_mode = st.sidebar.radio("Manual Authentication", ["Login", "Register"])
        
        if auth_mode == "Login":
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type="password")
            if st.sidebar.button("Login to Platform"):
                success, msg = login_user(username, password)
                if success:
                    st.sidebar.success(msg)
                    st.rerun()
                else:
                    st.sidebar.error(msg)
        else:
            name = st.sidebar.text_input("Full Name")
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type="password")
            role = st.sidebar.selectbox("Role", ["student", "admin"])
            if st.sidebar.button("Create Account"):
                if len(username) < 3 or len(password) < 4:
                    st.sidebar.error("Username (min 3) and Password (min 4) are required.")
                else:
                    success, msg = register_user(username, name, password, role)
                    if success:
                        st.sidebar.success(msg)
                    else:
                        st.sidebar.error(msg)

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        
    show_auth()
    show_landing_page()

if __name__ == "__main__":
    main()
