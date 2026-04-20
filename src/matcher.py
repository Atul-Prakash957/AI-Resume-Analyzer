from src.skill_extractor import extract_skills
from src.recommender import recommend_courses


def match_skills(resume_text, jd_text):

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = list(set(resume_skills).intersection(set(jd_skills)))
    missing = list(set(jd_skills) - set(resume_skills))

    if len(jd_skills) == 0:
        score = 0
    else:
        score = (len(matched) / len(jd_skills)) * 100

    # 🔥 NEW: Course Recommendation (top 3 missing skills)
    top_missing = missing[:3]
    courses = recommend_courses(top_missing)

    return resume_skills, jd_skills, matched, missing, round(score, 2), courses