import pdfplumber
import re

ROLE_SKILL_PROFILES = {
    "Software Engineer": {
        "Core Languages": ["Python", "Java", "C++", "JavaScript", "TypeScript", "Go", "C#"],
        "Frameworks & Web": ["React", "Node.js", "Django", "FastAPI", "Spring Boot", "Express", "REST API"],
        "Tools & Cloud": ["Git", "Docker", "Linux", "CI/CD", "AWS", "SQL", "PostgreSQL"],
        "Soft Skills & Methods": ["Agile", "Scrum", "Problem Solving", "Object-Oriented Design", "Data Structures"]
    },
    "Data Scientist / AI Engineer": {
        "Core Languages": ["Python", "R", "SQL", "C++"],
        "Frameworks & Web": ["PyTorch", "TensorFlow", "scikit-learn", "Pandas", "NumPy", "Keras", "FastAPI", "OpenCV"],
        "Tools & Cloud": ["Jupyter", "Docker", "AWS", "MLflow", "Git", "Spark", "Tableau", "Power BI"],
        "Soft Skills & Methods": ["Machine Learning", "Deep Learning", "NLP", "Statistics", "Data Mining", "A/B Testing"]
    },
    "Frontend Engineer": {
        "Core Languages": ["JavaScript", "TypeScript", "HTML5", "CSS3"],
        "Frameworks & Web": ["React", "Next.js", "Vue.js", "Angular", "TailwindCSS", "Redux", "Sass"],
        "Tools & Cloud": ["Webpack", "Vite", "Git", "Figma", "Jest", "npm/yarn", "REST API", "GraphQL"],
        "Soft Skills & Methods": ["Responsive Design", "Web Performance", "UI/UX Design", "Accessibility (a11y)", "Cross-Browser Compatibility"]
    },
    "Backend Engineer": {
        "Core Languages": ["Java", "Python", "Go", "Node.js", "C#", "SQL"],
        "Frameworks & Web": ["Spring Boot", "FastAPI", "Django", "Express", "Microservices", "gRPC", "GraphQL"],
        "Tools & Cloud": ["PostgreSQL", "MongoDB", "Redis", "Docker", "Kubernetes", "AWS", "Kafka", "RabbitMQ"],
        "Soft Skills & Methods": ["System Design", "Database Optimization", "API Design", "Security", "Caching"]
    },
    "Full Stack Developer": {
        "Core Languages": ["JavaScript", "TypeScript", "Python", "Java", "SQL", "HTML5", "CSS3"],
        "Frameworks & Web": ["React", "Node.js", "Next.js", "Django", "FastAPI", "Express", "TailwindCSS"],
        "Tools & Cloud": ["Git", "Docker", "PostgreSQL", "MongoDB", "AWS", "Vercel", "REST API"],
        "Soft Skills & Methods": ["Full Stack Architecture", "Agile", "CI/CD", "Authentication", "State Management"]
    },
    "DevOps / Cloud Engineer": {
        "Core Languages": ["Bash", "Python", "Go", "YAML"],
        "Frameworks & Web": ["Terraform", "Ansible", "Helm", "CloudFormation"],
        "Tools & Cloud": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "GitHub Actions", "Prometheus", "Grafana"],
        "Soft Skills & Methods": ["CI/CD", "Infrastructure as Code", "Site Reliability", "Security", "Monitoring"]
    },
    "Cybersecurity Analyst": {
        "Core Languages": ["Python", "Bash", "C", "SQL", "PowerShell"],
        "Frameworks & Web": ["Wireshark", "Metasploit", "Nmap", "Burp Suite", "SIEM", "Splunk"],
        "Tools & Cloud": ["Linux", "Network Security", "Firewalls", "Cryptography", "Identity Access Management"],
        "Soft Skills & Methods": ["Penetration Testing", "Vulnerability Assessment", "Incident Response", "Threat Intelligence", "ISO 27001"]
    }
}

ACTION_VERBS = [
    "achieved", "analyzed", "architected", "automated", "built", "created", "designed",
    "developed", "engineered", "established", "expanded", "generated", "implemented",
    "improved", "increased", "initiated", "integrated", "launched", "led", "managed",
    "optimized", "orchestrated", "reduced", "refactored", "restructured", "scaled",
    "spearheaded", "standardized", "transformed", "upgraded"
]

REQUIRED_SECTIONS = {
    "Contact Info": [r'\bemail\b', r'\bphone\b', r'\blinkedin\b', r'\bgithub\b', r'@'],
    "Education": [r'\beducation\b', r'\buniversity\b', r'\bcollege\b', r'\bdegree\b', r'\bbachelor\b', r'\bmaster\b', r'\bgpa\b'],
    "Experience": [r'\bexperience\b', r'\bwork\b', r'\binternship\b', r'\bemployment\b', r'\brole\b'],
    "Projects": [r'\bprojects?\b', r'\bportfolio\b', r'\bbuilt\b', r'\bgithub\b'],
    "Skills": [r'\bskills?\b', r'\btechnologies\b', r'\bcompetencies\b', r'\btools\b'],
    "Certifications": [r'\bcertificat(e|ion)s?\b', r'\bcourses?\b', r'\blicenses?\b']
}

def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def analyze_resume(text, role_name="Software Engineer"):
    text_lower = text.lower()
    words = re.findall(r'\w+', text_lower)
    word_count = len(words)
    
    # Get profile skills
    profile = ROLE_SKILL_PROFILES.get(role_name, ROLE_SKILL_PROFILES["Software Engineer"])
    
    found_by_category = {}
    missing_by_category = {}
    all_target_skills = []
    all_found_skills = []
    all_missing_skills = []

    for cat, skills in profile.items():
        found = []
        missing = []
        for skill in skills:
            all_target_skills.append(skill)
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found.append(skill)
                all_found_skills.append(skill)
            else:
                missing.append(skill)
                all_missing_skills.append(skill)
        found_by_category[cat] = found
        missing_by_category[cat] = missing

    # Calculate skill match percentage
    skill_match_score = (len(all_found_skills) / len(all_target_skills) * 100) if all_target_skills else 0

    # Section Detection
    sections_found = {}
    for sec, patterns in REQUIRED_SECTIONS.items():
        found = any(re.search(pat, text_lower) for pat in patterns)
        sections_found[sec] = found

    section_score = (sum(sections_found.values()) / len(sections_found)) * 100

    # Action Verbs Count
    found_action_verbs = [verb for verb in ACTION_VERBS if re.search(r'\b' + verb + r'\b', text_lower)]
    action_verb_score = min(100, (len(found_action_verbs) / 6) * 100)

    # Quantified Metrics Detection (numbers with %, $, +, k, m)
    quantified_matches = re.findall(r'\b\d+\s*%|\$\s*\d+|\b\d+\s*\+|\b\d+\s*(users|clients|projects|ms|sec|x)\b', text_lower)
    quantified_count = len(quantified_matches)
    metric_score = min(100, (quantified_count / 3) * 100)

    # Weighted Overall ATS Score
    overall_ats = (skill_match_score * 0.50) + (section_score * 0.20) + (action_verb_score * 0.15) + (metric_score * 0.15)
    overall_ats = round(overall_ats, 1)

    # Rating
    if overall_ats >= 80:
        rating = "Excellent"
        rating_color = "#34D399"
    elif overall_ats >= 60:
        rating = "Good"
        rating_color = "#60A5FA"
    elif overall_ats >= 40:
        rating = "Average"
        rating_color = "#FBBF24"
    else:
        rating = "Needs Improvement"
        rating_color = "#F87171"

    # Generate Recommendations
    suggestions = []
    if not sections_found.get("Certifications", True):
        suggestions.append("Add a 'Certifications' section to showcase verified skills and credentials.")
    if not sections_found.get("Projects", True):
        suggestions.append("Add a dedicated 'Projects' section with GitHub or live demo links.")
    if len(found_action_verbs) < 5:
        suggestions.append(f"Use more strong action verbs (e.g. {', '.join(ACTION_VERBS[:4])}) to start bullet points.")
    if quantified_count < 2:
        suggestions.append("Quantify your achievements with numbers (e.g. 'Improved speed by 35%', 'Managed 5+ projects').")
    if word_count < 150:
        suggestions.append("Your resume text appears very short. Consider adding more details about your responsibilities.")

    return {
        "role_name": role_name,
        "ats_score": overall_ats,
        "rating": rating,
        "rating_color": rating_color,
        "word_count": word_count,
        "skill_match_score": round(skill_match_score, 1),
        "section_score": round(section_score, 1),
        "found_by_category": found_by_category,
        "missing_by_category": missing_by_category,
        "found_skills": all_found_skills,
        "missing_skills": all_missing_skills,
        "sections_found": sections_found,
        "found_action_verbs": found_action_verbs,
        "quantified_count": quantified_count,
        "suggestions": suggestions
    }
