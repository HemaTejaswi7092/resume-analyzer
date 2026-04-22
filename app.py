import streamlit as st
import PyPDF2
import io
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

# Page config
st.set_page_config(page_title="AI Resume Analyzer", page_icon="🤖", layout="wide")

# API key from .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

st.title("🤖 AI Resume & Job Match Analyzer")
st.markdown("Upload your resume and paste a job description to get an AI-powered match analysis.")

# Two columns
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
You are an expert resume analyst and career coach.

Analyze this resume against the job description and provide:

1. MATCH SCORE (out of 100)
2. TOP 5 MATCHING SKILLS found in both resume and job description
3. TOP 5 MISSING SKILLS from the resume that the job requires
4. 3 IMPROVED BULLET POINTS rewritten to better match the job
5. OVERALL RECOMMENDATION (2-3 sentences)

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_desc}

Be specific, actionable, and encouraging.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500
    )
    return response.choices[0].message.content

# Analyze button
if st.button("🔍 Analyze My Resume", type="primary"):
    if not uploaded_file:
        st.error("Please upload your resume PDF!")
    elif not job_description:
        st.error("Please paste a job description!")
    else:
        with st.spinner("AI is analyzing your resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            result = analyze_resume(resume_text, job_description)
        
        st.success("Analysis Complete!")
        st.markdown("---")
        st.markdown(result)