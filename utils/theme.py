import streamlit as st

def apply_custom_theme():
    """Injects modern custom CSS, glassmorphism, gradient accents, and keyframe animations into Streamlit pages."""
    st.markdown("""
    <style>
    /* Google Font import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
    }

    /* Keyframe Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 5px rgba(99, 102, 241, 0.4); }
        50% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.8), 0 0 30px rgba(168, 85, 247, 0.5); }
        100% { box-shadow: 0 0 5px rgba(99, 102, 241, 0.4); }
    }

    @keyframes floatElement {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
        100% { transform: translateY(0px); }
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes scaleUp {
        from { transform: scale(0.95); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }

    /* Main Container Animation */
    .main .block-container {
        animation: fadeIn 0.6s ease-out forwards;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeIn 0.5s ease-out;
    }

    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 35px rgba(99, 102, 241, 0.25);
        border-color: rgba(129, 140, 248, 0.4);
    }

    /* Hero Gradient Text */
    .gradient-header {
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #EC4899 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -0.5px;
        animation: gradientShift 6s ease infinite;
    }

    /* Stat Box styling */
    .stat-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
        border-left: 4px solid #6366F1;
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
    }

    .stat-title {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stat-value {
        color: #F8FAFC;
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 4px;
    }

    /* Badge Pills */
    .skill-badge-found {
        display: inline-block;
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(52, 211, 153, 0.3);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.88rem;
        font-weight: 600;
        margin: 4px;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.1);
        transition: all 0.2s ease;
    }

    .skill-badge-found:hover {
        transform: scale(1.05);
        background: rgba(16, 185, 129, 0.25);
    }

    .skill-badge-missing {
        display: inline-block;
        background: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(248, 113, 113, 0.3);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.88rem;
        font-weight: 600;
        margin: 4px;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.1);
        transition: all 0.2s ease;
    }

    .skill-badge-missing:hover {
        transform: scale(1.05);
        background: rgba(239, 68, 68, 0.25);
    }

    /* Pulse Indicator */
    .pulse-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulseGlow 2s infinite;
        margin-right: 8px;
    }

    /* Streamlit custom element tweaks */
    div.stButton > button {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35);
        transition: all 0.25s ease;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #4338CA 0%, #6D28D9 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5);
        color: white;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: #0F172A;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Tab active highlight styling */
    button[data-baseweb="tab"] {
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
    }

    /* Metric Cards Glow */
    div[data-testid="stMetricValue"] {
        font-weight: 800 !important;
        color: #818CF8 !important;
    }

    </style>
    """, unsafe_allow_html=True)
