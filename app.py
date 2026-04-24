import streamlit as st
import PyPDF2
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

st.set_page_config(page_title="AI Resume Analyzer", page_icon="🤖", layout="wide")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# Custom CSS
st.markdown("""
<style>
.score-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
}
.score-number {
    font-size: 60px;
    font-weight: bold;
}
.skill-match {
    background-color: #d4edda;
    color: #155724;
    padding: 5px 12px;
    border-radius: 20px;
    margin: 4px;
    display: inline-block;
    font-size: 14px;
}
.skill-missing {
    background-color: #f8d7da;
    color: #721c24;
    padding: 5px 12px;
    border-radius: 20px;
    margin: 4px;
    display: inline-block;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Resume & Job Match Analyzer")
st.markdown("Upload your resume and paste a job description to get an AI-powered match analysis.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload Your Resume")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

with col2:
    st.subheader("💼 Paste Job Description")
    job_description = st.text_area("Job Description", height=200, placeholder="Paste the job description here...")

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def analyze_resume(resume_text, job_desc):
    prompt = f"""
You are an expert resume analyst. Analyze the resume against the job description.

Return ONLY a valid JSON object with exactly this structure:
{{
    "match_score": <number between 0-100>,
    "matching_skills": ["skill1", "skill2", "skill3", "skill4", "skill5"],
    "missing_skills": ["skill1", "skill2", "skill3", "skill4", "skill5"],
    "improved_bullets": [
        "Improved bullet point 1",
        "Improved bullet point 2", 
        "Improved bullet point 3"
    ],
    "recommendation": "2-3 sentence overall recommendation here"
}}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_desc}

Return ONLY the JSON, no other text.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500
    )
    return response.choices[0].message.content

if st.button("🔍 Analyze My Resume", type="primary"):
    if not uploaded_file:
        st.error("Please upload your resume PDF!")
    elif not job_description:
        st.error("Please paste a job description!")
    else:
        with st.spinner("AI is analyzing your resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            result = analyze_resume(resume_text, job_description)

        try:
            # Clean and parse JSON
            clean = result.strip().replace("```json", "").replace("```", "")
            data = json.loads(clean)

            score = data["match_score"]

            # Score card
            st.markdown("---")
            col1, col2, col3 = st.columns([1,1,1])

            with col1:
                st.markdown(f"""
                <div class="score-card">
                    <div>Match Score</div>
                    <div class="score-number">{score}</div>
                    <div>out of 100</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.metric("Matching Skills", len(data["matching_skills"]))

            with col3:
                st.metric("Missing Skills", len(data["missing_skills"]))

            # Progress bar
            st.markdown("### 📊 Match Strength")
            st.progress(score / 100)

            if score >= 80:
                st.success("🟢 Strong Match — You're a great fit for this role!")
            elif score >= 60:
                st.warning("🟡 Moderate Match — Some gaps to address")
            else:
                st.error("🔴 Weak Match — Significant skills missing")

            # Skills columns
            st.markdown("---")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### ✅ Matching Skills")
                skills_html = ""
                for skill in data["matching_skills"]:
                    skills_html += f'<span class="skill-match">✓ {skill}</span>'
                st.markdown(skills_html, unsafe_allow_html=True)

            with col2:
                st.markdown("### ❌ Missing Skills")
                skills_html = ""
                for skill in data["missing_skills"]:
                    skills_html += f'<span class="skill-missing">✗ {skill}</span>'
                st.markdown(skills_html, unsafe_allow_html=True)

            # Improved bullets
            st.markdown("---")
            st.markdown("### ✍️ AI-Improved Bullet Points")
            for i, bullet in enumerate(data["improved_bullets"], 1):
                st.markdown(f"**{i}.** {bullet}")

            # Recommendation
            st.markdown("---")
            st.markdown("### 💡 Overall Recommendation")
            st.info(data["recommendation"])

        except Exception as e:
            st.error(f"Error parsing response: {e}")
            st.markdown(result)