import bcrypt
import streamlit as st
from utils.db import get_session, User

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def ensure_default_users():
    """Ensure default admin and student demo accounts exist in the database."""
    session = get_session()
    admin = session.query(User).filter_by(username='admin').first()
    if not admin:
        new_admin = User(
            username='admin',
            name='System Administrator',
            password_hash=hash_password('admin'),
            role='admin'
        )
        session.add(new_admin)
        
    student = session.query(User).filter_by(username='student').first()
    if not student:
        new_student = User(
            username='student',
            name='Demo Student',
            password_hash=hash_password('student'),
            role='student'
        )
        session.add(new_student)
        
    session.commit()
    session.close()

def register_user(username, name, password, role="student"):
    ensure_default_users()
    session = get_session()
    if session.query(User).filter_by(username=username).first():
        session.close()
        return False, "Username already exists."
    
    new_user = User(
        username=username,
        name=name,
        password_hash=hash_password(password),
        role=role
    )
    session.add(new_user)
    session.commit()
    session.close()
    return True, f"User '{username}' registered successfully."

def login_user(username, password):
    ensure_default_users()
    session = get_session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user and verify_password(password, user.password_hash):
        st.session_state['logged_in'] = True
        st.session_state['username'] = user.username
        st.session_state['name'] = user.name
        st.session_state['role'] = user.role
        return True, f"Welcome back, {user.name}!"
    return False, "Invalid username or password."

def logout_user():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state['name'] = None
    st.session_state['role'] = None

def update_user_role(username, new_role):
    session = get_session()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        session.close()
        return False, "User not found."
    user.role = new_role
    session.commit()
    session.close()
    return True, f"Role for '{username}' updated to {new_role}."

def reset_user_password(username, new_password):
    session = get_session()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        session.close()
        return False, "User not found."
    user.password_hash = hash_password(new_password)
    session.commit()
    session.close()
    return True, f"Password for '{username}' has been reset."

def delete_user(username):
    session = get_session()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        session.close()
        return False, "User not found."
    session.delete(user)
    session.commit()
    session.close()
    return True, f"User '{username}' deleted successfully."

def require_auth(allowed_roles=None):
    """
    Enforces authentication and role checks.
    Renders an inline login / demo login widget if user is not authenticated or lacks required role.
    """
    ensure_default_users()
    
    if not st.session_state.get('logged_in', False):
        st.markdown("""
        <div class="glass-card" style="max-width: 550px; margin: 40px auto;">
            <h3 style="color: #818CF8; text-align: center; margin-top:0;">🔐 Authentication Required</h3>
            <p style="color: #94A3B8; text-align: center; font-size: 0.95rem;">
                Please log in to your account or click a Quick Demo Login below to access this page.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            u_input = st.text_input("Username", key="inline_u")
            p_input = st.text_input("Password", type="password", key="inline_p")
            if st.button("🔑 Log In", key="inline_login_submit"):
                ok, msg = login_user(u_input, p_input)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
                    
        with col2:
            st.markdown("<p style='font-weight:600; color:#F8FAFC;'>⚡ One-Click Demo Access:</p>", unsafe_allow_html=True)
            if st.button("⚙️ Log In as Administrator", key="inline_admin_demo"):
                login_user('admin', 'admin')
                st.rerun()
            st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)
            if st.button("🎓 Log In as Student", key="inline_student_demo"):
                login_user('student', 'student')
                st.rerun()
                
        st.stop()

    if allowed_roles and st.session_state.get('role') not in allowed_roles:
        st.markdown(f"""
        <div class="glass-card" style="max-width: 550px; margin: 40px auto; text-align: center;">
            <h3 style="color: #F87171; margin-top:0;">🔒 Admin Access Required</h3>
            <p style="color: #CBD5E1;">
                You are currently logged in as <b>{st.session_state['name']}</b> ({st.session_state['role'].capitalize()}). 
                This page requires Administrator permissions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("⚙️ Switch to Admin Account", key="switch_admin_btn"):
                login_user('admin', 'admin')
                st.rerun()
        with c2:
            if st.button("🚪 Logout Current Account", key="logout_insufficient_role"):
                logout_user()
                st.rerun()
                
        st.stop()
