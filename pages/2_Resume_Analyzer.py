import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.auth import require_auth
from utils.resume_parser import extract_text_from_pdf, analyze_resume, ROLE_SKILL_PROFILES
from utils.theme import apply_custom_theme

# Page Configuration
st.set_page_config(
    page_title="AI Resume Analyzer | AI Career Navigator",
    page_icon="📄",
    layout="wide"
)

apply_custom_theme()
require_auth()

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 class="gradient-header" style="font-size: 2.8rem; margin-bottom: 0.5rem;">📄 AI Resume Analyzer</h1>
    <p style="color: #94A3B8; font-size: 1.1rem; max-width: 700px; margin: 0 auto;">
        Supercharge your career readiness! Upload your resume or paste your text to get an instant AI-powered ATS match score, detailed skill gap analysis, and tailored recommendations for your target role.
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar / Top Setup
col_setup1, col_setup2 = st.columns([1, 2])

with col_setup1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🎯 Select Target Role")
    selected_role = st.selectbox(
        "Choose the job profile you are targeting:",
        options=list(ROLE_SKILL_PROFILES.keys()),
        index=0
    )
    st.caption("Customized skill matching & ATS optimization criteria will be evaluated against this profile.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_setup2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📥 Provide Resume Input")
    
    input_method = st.radio("Choose input method:", ["Upload PDF File", "Paste Resume Text directly"], horizontal=True)
    
    resume_text = ""
    if input_method == "Upload PDF File":
        uploaded_file = st.file_uploader("Drag and drop your PDF Resume", type=["pdf"])
        if uploaded_file is not None:
            with st.spinner("Processing PDF document..."):
                resume_text = extract_text_from_pdf(uploaded_file)
                if not resume_text.strip():
                    st.error("⚠️ Could not extract text from this PDF. It might be scanned or image-based.")
                else:
                    st.success("✅ Resume PDF extracted successfully!")
    else:
        sample_text_demo = """Senior Software Engineer candidate with 3 years of experience.
Education: Bachelor of Technology in Computer Science (GPA: 3.8/4.0)
Skills: Python, Java, SQL, React, FastAPI, Docker, Git, AWS, REST API, Agile
Experience:
- Engineered RESTful microservices using FastAPI and Python, improving latency by 30%.
- Built interactive frontend dashboards with React and Redux for 50,000+ active users.
- Automated CI/CD deployment pipelines using Docker, AWS, and Git.
- Led sprint planning and code reviews in an Agile environment.
Projects:
- AI Resume Parser: Developed full-stack web app with Python and scikit-learn.
Certifications: AWS Certified Developer Associate"""

        if st.checkbox("Use Sample Resume for Demo", value=False):
            resume_text = sample_text_demo
        else:
            resume_text = st.text_area("Paste your resume content below:", height=180, placeholder="Paste plain text resume here...")

    st.markdown('</div>', unsafe_allow_html=True)

# Run Analysis if text is present
if resume_text and resume_text.strip():
    results = analyze_resume(resume_text, role_name=selected_role)
    
    st.markdown("---")
    st.markdown(f"<h2 style='text-align: center; color: #F8FAFC;'>📊 Analysis Results for <span style='color: #818CF8;'>{selected_role}</span></h2>", unsafe_allow_html=True)
    
    # Metrics Row
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    with m_col1:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color: {results['rating_color']};">
            <div class="stat-title">Overall ATS Score</div>
            <div class="stat-value" style="color: {results['rating_color']};">{results['ats_score']}%</div>
            <div style="font-size: 0.85rem; color: #94A3B8;">Rating: <b>{results['rating']}</b></div>
        </div>
        """, unsafe_allow_html=True)
        
    with m_col2:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color: #6366F1;">
            <div class="stat-title">Skill Match Rate</div>
            <div class="stat-value">{results['skill_match_score']}%</div>
            <div style="font-size: 0.85rem; color: #94A3B8;">{len(results['found_skills'])} of {len(results['found_skills']) + len(results['missing_skills'])} matched</div>
        </div>
        """, unsafe_allow_html=True)

    with m_col3:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color: #EC4899;">
            <div class="stat-title">Section Completeness</div>
            <div class="stat-value">{results['section_score']}%</div>
            <div style="font-size: 0.85rem; color: #94A3B8;">Key sections detected</div>
        </div>
        """, unsafe_allow_html=True)

    with m_col4:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color: #10B981;">
            <div class="stat-title">Action Verbs Found</div>
            <div class="stat-value">{len(results['found_action_verbs'])}</div>
            <div style="font-size: 0.85rem; color: #94A3B8;">Strong impact words</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Two Main Visual Columns
    chart_col1, chart_col2 = st.columns([1, 1])

    with chart_col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 ATS Score Gauge")
        
        # Donut / Gauge Chart
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = results['ats_score'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"Target Match: {selected_role}", 'font': {'size': 16, 'color': "#94A3B8"}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
                'bar': {'color': results['rating_color']},
                'bgcolor': "rgba(15, 23, 42, 0.6)",
                'borderwidth': 2,
                'bordercolor': "rgba(255, 255, 255, 0.1)",
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.2)'},
                    {'range': [40, 75], 'color': 'rgba(245, 158, 11, 0.2)'},
                    {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.2)'}
                ],
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#F8FAFC", family="Plus Jakarta Sans"),
            height=260,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📑 Structural Section Checklist")
        
        for sec, status in results['sections_found'].items():
            if status:
                st.markdown(f"✅ **{sec}**: <span style='color: #34D399; font-weight:600;'>Present</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"❌ **{sec}**: <span style='color: #F87171; font-weight:600;'>Missing or Not Clearly Defined</span>", unsafe_allow_html=True)
                
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"**Quantified Accomplishments Detected:** `{results['quantified_count']}` metrics found")
        st.markdown('</div>', unsafe_allow_html=True)

    # Detailed Skill Breakdown
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 💡 Categorized Skill Match Breakdown")
    
    for cat in results['found_by_category'].keys():
        found = results['found_by_category'][cat]
        missing = results['missing_by_category'][cat]
        
        st.markdown(f"#### {cat}")
        
        pills_html = ""
        for sk in found:
            pills_html += f'<span class="skill-badge-found">✓ {sk}</span> '
        for sk in missing:
            pills_html += f'<span class="skill-badge-missing">✗ {sk}</span> '
            
        st.markdown(pills_html if pills_html else "*No skills listed in this category*", unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Actionable Recommendations Card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🚀 Actionable Recommendations to Improve Score")
    
    if results['suggestions']:
        for i, sugg in enumerate(results['suggestions'], 1):
            st.markdown(f"💡 **Suggestion {i}:** {sugg}")
    else:
        st.success("🎉 Outstanding job! Your resume meets high ATS standards for this target role!")
        
    st.markdown('</div>', unsafe_allow_html=True)

    # Export Report Button
    st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
    st.markdown("### 📥 Download Analysis Summary")
    report_md = f"""# AI Resume Analyzer Report
Target Role: {selected_role}
ATS Score: {results['ats_score']}%
Rating: {results['rating']}
Skill Match Rate: {results['skill_match_score']}%

## Found Skills
{', '.join(results['found_skills'])}

## Recommended Skills to Add
{', '.join(results['missing_skills'])}

## Actionable Suggestions
""" + "\n".join([f"- {s}" for s in results['suggestions']])
    
    st.download_button(
        label="Download Full Analysis Report (.md)",
        data=report_md,
        file_name=f"resume_analysis_{selected_role.lower().replace(' ', '_')}.md",
        mime="text/markdown"
    )
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👈 Upload a PDF resume or select 'Paste Resume Text' in the panel above to begin analysis!")
