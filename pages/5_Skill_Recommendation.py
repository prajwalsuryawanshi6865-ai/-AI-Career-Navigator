import streamlit as st
from utils.auth import require_auth
from utils.theme import apply_custom_theme

st.set_page_config(
    page_title="Skill Recommendation | AI Career Navigator",
    page_icon="💡",
    layout="wide"
)

apply_custom_theme()
require_auth()

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 class="gradient-header" style="font-size: 2.8rem; margin-bottom: 0.5rem;">💡 Industry Skill Roadmap</h1>
    <p style="color: #94A3B8; font-size: 1.1rem; max-width: 700px; margin: 0 auto;">
        Explore curated in-demand skill requirements and learning paths tailored for key tech career roles.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
role = st.selectbox("Select Target Role Profile:", [
    "Software Engineer",
    "Data Scientist / AI Engineer",
    "Full Stack Developer",
    "DevOps & Cloud Engineer",
    "Cybersecurity Analyst"
])
st.markdown('</div>', unsafe_allow_html=True)

if role == "Software Engineer":
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: #818CF8;">💻 Software Engineer Roadmap</h3>
        <p><b>Core Languages:</b> <span class="skill-badge-found">Python</span> <span class="skill-badge-found">Java</span> <span class="skill-badge-found">C++</span> <span class="skill-badge-found">TypeScript</span></p>
        <p><b>Frameworks & Tools:</b> <span class="skill-badge-found">React</span> <span class="skill-badge-found">FastAPI</span> <span class="skill-badge-found">Docker</span> <span class="skill-badge-found">Git</span> <span class="skill-badge-found">AWS</span></p>
        <p><b>Core Concepts:</b> Data Structures & Algorithms, Object-Oriented Design, System Design, REST APIs</p>
        <hr style="border-color: rgba(255,255,255,0.1);">
        <h4>Recommended Learning Resources:</h4>
        <ul>
            <li><a href="https://leetcode.com/" target="_blank" style="color: #60A5FA;">LeetCode</a> - Master Data Structures & Coding Interviews</li>
            <li><a href="https://fullstackopen.com/en/" target="_blank" style="color: #60A5FA;">Full Stack Open</a> - Deep Dive Modern Web Development</li>
            <li><a href="https://roadmap.sh/backend" target="_blank" style="color: #60A5FA;">Backend Developer Roadmap</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif role == "Data Scientist / AI Engineer":
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: #34D399;">🤖 Data Scientist / AI Engineer Roadmap</h3>
        <p><b>Core Languages:</b> <span class="skill-badge-found">Python</span> <span class="skill-badge-found">SQL</span> <span class="skill-badge-found">R</span></p>
        <p><b>ML Libraries:</b> <span class="skill-badge-found">PyTorch</span> <span class="skill-badge-found">TensorFlow</span> <span class="skill-badge-found">scikit-learn</span> <span class="skill-badge-found">Pandas</span></p>
        <p><b>Core Concepts:</b> Machine Learning, Deep Learning, Statistics, NLP, ML Architecture</p>
        <hr style="border-color: rgba(255,255,255,0.1);">
        <h4>Recommended Learning Resources:</h4>
        <ul>
            <li><a href="https://www.kaggle.com/" target="_blank" style="color: #34D399;">Kaggle Competitions & Datasets</a></li>
            <li><a href="https://www.fast.ai/" target="_blank" style="color: #34D399;">Fast.ai Practical Deep Learning</a></li>
            <li><a href="https://www.coursera.org/specializations/machine-learning-introduction" target="_blank" style="color: #34D399;">Andrew Ng Machine Learning Specialization</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif role == "Full Stack Developer":
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: #F59E0B;">🌐 Full Stack Developer Roadmap</h3>
        <p><b>Frontend:</b> <span class="skill-badge-found">React</span> <span class="skill-badge-found">Next.js</span> <span class="skill-badge-found">TypeScript</span> <span class="skill-badge-found">TailwindCSS</span></p>
        <p><b>Backend & DB:</b> <span class="skill-badge-found">Node.js</span> <span class="skill-badge-found">Express</span> <span class="skill-badge-found">PostgreSQL</span> <span class="skill-badge-found">MongoDB</span></p>
        <p><b>Core Concepts:</b> Full Stack Architecture, Authentication (OAuth/JWT), State Management, WebSockets</p>
        <hr style="border-color: rgba(255,255,255,0.1);">
        <h4>Recommended Learning Resources:</h4>
        <ul>
            <li><a href="https://fullstackopen.com/" target="_blank" style="color: #FBBF24;">Full Stack Open 2024</a></li>
            <li><a href="https://nextjs.org/learn" target="_blank" style="color: #FBBF24;">Next.js Official Interactive Tutorial</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif role == "DevOps & Cloud Engineer":
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: #EC4899;">☁️ DevOps & Cloud Engineer Roadmap</h3>
        <p><b>Tools & Platforms:</b> <span class="skill-badge-found">Docker</span> <span class="skill-badge-found">Kubernetes</span> <span class="skill-badge-found">Terraform</span> <span class="skill-badge-found">AWS</span> <span class="skill-badge-found">Ansible</span></p>
        <p><b>Scripting:</b> <span class="skill-badge-found">Bash</span> <span class="skill-badge-found">Python</span> <span class="skill-badge-found">YAML</span></p>
        <p><b>Core Concepts:</b> CI/CD Pipelines, Infrastructure as Code, Site Reliability, Monitoring (Prometheus/Grafana)</p>
        <hr style="border-color: rgba(255,255,255,0.1);">
        <h4>Recommended Learning Resources:</h4>
        <ul>
            <li><a href="https://roadmap.sh/devops" target="_blank" style="color: #F472B6;">DevOps Roadmap</a></li>
            <li><a href="https://aws.amazon.com/training/" target="_blank" style="color: #F472B6;">AWS Cloud Training</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif role == "Cybersecurity Analyst":
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: #60A5FA;">🛡️ Cybersecurity Analyst Roadmap</h3>
        <p><b>Tools:</b> <span class="skill-badge-found">Wireshark</span> <span class="skill-badge-found">Nmap</span> <span class="skill-badge-found">Metasploit</span> <span class="skill-badge-found">Burp Suite</span></p>
        <p><b>Core Concepts:</b> Penetration Testing, Network Security, Cryptography, Incident Response, SIEM</p>
        <hr style="border-color: rgba(255,255,255,0.1);">
        <h4>Recommended Learning Resources:</h4>
        <ul>
            <li><a href="https://tryhackme.com/" target="_blank" style="color: #60A5FA;">TryHackMe Cyber Hands-on Labs</a></li>
            <li><a href="https://www.hackthebox.com/" target="_blank" style="color: #60A5FA;">Hack The Box Penetration Testing</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
