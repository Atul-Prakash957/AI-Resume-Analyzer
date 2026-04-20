import streamlit as st
from src.preprocess_pdf import preprocess_resume
from src.predict_role import predict_role
from src.matcher import match_skills

# -------- LOAD CSS --------
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

# -------- HEADER --------
st.markdown('<div class="title">📄 AI Resume Analyzer</div>', unsafe_allow_html=True)

# -------- INPUT --------
resume_file = st.file_uploader("📂 Upload Resume", type=["pdf"])
jd_text = st.text_area("📝 Paste Job Description")

# -------- BUTTON --------
if st.button("🚀 Analyze Resume"):

    if resume_file is None:
        st.warning("Please upload a resume first.")
        st.stop()

    # Save file
    with open("temp_resume.pdf", "wb") as f:
        f.write(resume_file.read())

    # -------- PROCESS --------
    with st.spinner("Analyzing Resume..."):
        resume_text = preprocess_resume("temp_resume.pdf")

        # Role prediction
        role = predict_role(resume_text)

        # Skill matching (UPDATED)
        resume_skills, jd_skills, matched, missing, score, courses = match_skills(resume_text, jd_text)

    st.markdown("---")

    # -------- RESULTS --------
    st.subheader("🎯 Predicted Role")
    st.success(role)

    st.subheader(" Match Score")
    st.progress(score / 100)
    st.write(f"{score}%")
    
    st.subheader("📄 Resume Skills")
    st.write(", ".join(resume_skills))

    st.subheader("📌 Job Description Skills")
    st.write(", ".join(jd_skills))

    st.subheader("✅ Matched Skills")
    st.write(", ".join(matched) if matched else "No match")

    st.subheader("❌ Missing Skills")
    st.write(", ".join(missing) if missing else "No missing skills 🎉")

    # 🔥 NEW: COURSE RECOMMENDATIONS
    st.subheader("📚 Course Recommendations")

    # ✅ Add this line (your idea, but polished)
    if courses:
        st.write(
            "If you want to improve your skills and better match the job description, here are some recommended courses:"
        )

        for skill, course_list in courses.items():
            st.markdown(f"### {skill.upper()}")

            for course in course_list:
                st.markdown(f"- [{course['name']}]({course['link']})")
    else:
        st.write("No course recommendations available")


