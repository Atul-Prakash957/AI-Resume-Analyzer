import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Setup Gemini AI
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Use a standard flash model for fast text generation
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 1024,
}

def recommend_courses(missing_skills):
    """
    Calls Gemini AI to recommend courses based on the missing skills.
    Returns a dictionary of skills to a list of courses.
    """
    if not missing_skills:
        return {}

    recommendations = {}
    
    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-3.5-flash-lite', generation_config=generation_config)
        
        for skill in missing_skills[:3]: # Limit to top 3 missing skills to save time
            prompt = f"""
            You are a career advisor. The candidate is missing the skill '{skill}'.
            Provide exactly 2 highly rated, real online courses (from Udemy, Coursera, freeCodeCamp, etc.) to learn '{skill}'.
            
            Return the output STRICTLY in this exact format (no markdown, no extra text):
            Course Name 1 | URL 1
            Course Name 2 | URL 2
            """
            
            response = model.generate_content(prompt)
            text = response.text.strip().split('\n')
            
            courses = []
            for line in text:
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) == 2:
                        courses.append({
                            "name": parts[0].strip(),
                            "link": parts[1].strip()
                        })
            
            if courses:
                recommendations[skill] = courses
                
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        # Fallback if API fails or is not configured
        for skill in missing_skills[:3]:
            recommendations[skill] = [{"name": f"Search for {skill} on Coursera", "link": f"https://www.coursera.org/search?query={skill}"}]

    return recommendations

def get_ai_feedback(resume_text, jd_text, role, score):
    """
    Generates a personalized 2-3 sentence feedback summary.
    """
    try:
        if not os.environ.get("GOOGLE_API_KEY"):
            return "Configure your GOOGLE_API_KEY to receive personalized AI feedback!"
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        model = genai.GenerativeModel('gemini-3.5-flash-lite', generation_config=generation_config)
        prompt = f"""
        Act as an expert technical recruiter. 
        A candidate applied for a job with this description: "{jd_text[:500]}..."
        Their resume matched {score}% of the required skills. We predicted their best role is {role}.
        
        Write a short, professional, and encouraging 3-sentence summary of their fit for the role, and what they should focus on improving.
        Do not use bold text or markdown.
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Configure your GOOGLE_API_KEY to receive personalized AI feedback!"