import streamlit as st
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

# Load environment variables (for GOOGLE_API_KEY)
load_dotenv()

from src.preprocess_pdf import preprocess_resume
from src.predict_role import predict_role
from src.matcher import match_skills
from src.recommender import get_ai_feedback

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# -------- LOAD CSS --------
try:
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

# -------- HEADER --------
st.markdown('<div class="title">AI Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Powered by Gemini AI & Machine Learning</div>', unsafe_allow_html=True)

# -------- LAYOUT --------
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 1. Upload Resume")
    resume_file = st.file_uploader("", type=["pdf"])

with col2:
    st.markdown("### 2. Job Description")
    jd_text = st.text_area("", height=150, placeholder="Paste the job description here...")

# -------- BUTTON --------
st.markdown("<br>", unsafe_allow_html=True)
analyze_col1, analyze_col2, analyze_col3 = st.columns([1, 2, 1])
with analyze_col2:
    analyze_btn = st.button("Analyze Resume Fit")

if analyze_btn:
    if resume_file is None:
        st.warning("Please upload a resume first.")
        st.stop()
    if not jd_text.strip():
        st.warning("Please paste a job description.")
        st.stop()

    # Save file
    with open("temp_resume.pdf", "wb") as f:
        f.write(resume_file.read())

    # -------- PROCESS --------
    with st.spinner("Analyzing Resume & Generating AI Feedback..."):
        resume_text = preprocess_resume("temp_resume.pdf")

        # Role prediction (from ML model)
        role = predict_role(resume_text)

        # Skill matching & Course Recommendation (from Gemini API & Rules)
        resume_skills, jd_skills, matched, missing, score, courses = match_skills(resume_text, jd_text)
        
        # AI Personalized Feedback
        feedback = get_ai_feedback(resume_text, jd_text, role, score)

    st.markdown("---")

    # -------- RESULTS DASHBOARD --------
    res_col1, res_col2 = st.columns([1, 1.5], gap="large")

    with res_col1:
        st.markdown(f"### Predicted Role")
        st.info(f"**{role.upper()}**")
        
        st.markdown("### AI Feedback")
        st.write(f"*{feedback}*")

        st.markdown("### Skill Breakdown")
        st.success(f"**Matched ({len(matched)}):** {', '.join(matched) if matched else 'None'}")
        st.error(f"**Missing ({len(missing)}):** {', '.join(missing) if missing else 'None'}")

    with res_col2:
        # Beautiful Plotly Gauge Chart for Score
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            title = {'text': "ATS Match Score"},
            number = {'suffix': "%"},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#00ADB5"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 40], 'color': "rgba(255, 99, 132, 0.2)"},
                    {'range': [40, 75], 'color': "rgba(255, 206, 86, 0.2)"},
                    {'range': [75, 100], 'color': "rgba(75, 192, 192, 0.2)"}],
            }
        ))
        fig.update_layout(height=350, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
        st.plotly_chart(fig, use_container_width=True)

    # -------- AI COURSE RECOMMENDATIONS --------
    st.markdown("---")
    st.markdown("### AI Course Recommendations")
    
    if not os.environ.get("GOOGLE_API_KEY"):
        st.warning("**Note:** To see dynamic AI course recommendations, please add your `GOOGLE_API_KEY` to an `.env` file.")

    if courses:
        cols = st.columns(min(len(courses), 3))
        for idx, (skill, course_list) in enumerate(courses.items()):
            col = cols[idx % len(cols)]
            with col:
                st.markdown(f"**Improve {skill.upper()}:**")
                for c in course_list:
                    st.markdown(
                        f'''<div class="course-card">
                            <a href="{c['link']}" target="_blank">{c['name']}</a>
                        </div>''', 
                        unsafe_allow_html=True
                    )
    else:
        st.write("No missing skills to recommend courses for! Great job.")

