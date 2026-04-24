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

st.markdown("""
<style>
.skill-match {
    background-color: #d4edda; color: #155724;
    padding: 5px 12px; border-radius: 20px;
    margin: 4px; display: inline-block; font-size: 14px;
}
.skill-missing {
    background-color: #f8d7da; color: #721c24;
    padding: 5px 12px; border-radius: 20px;
    margin: 4px; display: inline-block; font-size: 14px;
}
.bullet-old {
    background-color: #f8d7da; color: #721c24;
    padding: 10px; border-radius: 8px; margin: 5px 0;
}
.bullet-new {
    background-color: #d4edda; color: #155724;
    padding: 10px; border-radius: 8px; margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Resume & Job Match Analyzer")
st.markdown("Upload your resume and get AI-powered analysis, job comparison, and automatic bullet rewrites.")

mode = st.radio("How many jobs do you want to analyze?",
    ["🎯 Single Job", "⚖️ Compare 2-3 Jobs"], horizontal=True)

st.markdown("---")

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def analyze_resume(resume_text, job_desc):
    prompt = f"""
You are an expert resume analyst. Analyze the resume against the job description.

Return ONLY a valid JSON object:
{{
    "match_score": <0-100>,
    "matching_skills": ["skill1", "skill2", "skill3", "skill4", "skill5"],
    "missing_skills": ["skill1", "skill2", "skill3", "skill4", "skill5"],
    "recommendation": "2-3 sentence recommendation"
}}

RESUME: {resume_text}
JOB DESCRIPTION: {job_desc}
Return ONLY JSON.
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600
    )
    return response.choices[0].message.content

def explain_jd(job_desc):
    prompt = f"""
You are a career advisor helping an international student on OPT/F1 visa in the USA.

Return ONLY a valid JSON object:
{{
    "role_summary": "2 sentences explaining what this job does in simple words",
    "key_requirements": ["req 1", "req 2", "req 3", "req 4", "req 5"],
    "nice_to_have": ["nice 1", "nice 2", "nice 3"],
    "sponsorship_situation": "One clear sentence about visa sponsorship for this role",
    "company_expectations": "One sentence about what company really wants",
    "difficulty_level": "Easy or Medium or Hard",
    "apply_recommendation": "Yes or Maybe or No and one sentence why"
}}

JOB DESCRIPTION: {job_desc}
Return ONLY JSON.
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600
    )
    return response.choices[0].message.content

def rewrite_all_bullets(resume_text, job_desc):
    prompt = f"""
You are an expert resume writer.

Extract bullet points from this resume and rewrite each one to match the job description.
Make them impactful and ATS-friendly with strong action verbs.

Return ONLY a valid JSON array:
[
    {{"original": "original bullet", "rewritten": "rewritten bullet"}},
    {{"original": "original bullet 2", "rewritten": "rewritten bullet 2"}}
]

RESUME: {resume_text}
JOB DESCRIPTION: {job_desc}
Return ONLY the JSON array. Maximum 8 bullets.
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1200
    )
    return response.choices[0].message.content

def generate_cover_letter(resume_text, job_desc, company_name, job_title):
    prompt = f"""
Write a professional cover letter for an OPT/F1 student.

3 paragraphs only:
1. Opening — mention role at {company_name}, show enthusiasm
2. Match 3 skills from resume to job with examples
3. Closing — mention OPT authorization, call to action

Keep under 250 words. Sound human not robotic.

RESUME: {resume_text}
JOB: {job_desc}
COMPANY: {company_name}
TITLE: {job_title}

Write the letter directly.
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=700
    )
    return response.choices[0].message.content

def display_scores(data):
    score = data["match_score"]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Match Score", f"{score}/100")
    with col2:
        st.metric("✅ Matching Skills", len(data["matching_skills"]))
    with col3:
        st.metric("❌ Missing Skills", len(data["missing_skills"]))

    st.markdown("### 📊 Match Strength")
    st.progress(score / 100)
    if score >= 80:
        st.success("🟢 Strong Match — You're a great fit!")
    elif score >= 60:
        st.warning("🟡 Moderate Match — Some gaps to address")
    else:
        st.error("🔴 Weak Match — Significant skills missing")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ✅ Matching Skills")
        html = "".join([f'<span class="skill-match">✓ {s}</span>'
                        for s in data["matching_skills"]])
        st.markdown(html, unsafe_allow_html=True)
    with col2:
        st.markdown("### ❌ Missing Skills")
        html = "".join([f'<span class="skill-missing">✗ {s}</span>'
                        for s in data["missing_skills"]])
        st.markdown(html, unsafe_allow_html=True)

    st.markdown("---")
    st.info(f"💡 {data['recommendation']}")

def display_jd_explainer(job_desc):
    st.markdown("---")
    st.markdown("### 📖 JD Explainer — What This Job Actually Means")
    st.markdown("*Breaking this down in simple words for an OPT/F1 student*")

    with st.spinner("Analyzing job description..."):
        result = explain_jd(job_desc)

    try:
        clean = result.strip().replace("```json", "").replace("```", "")
        jd = json.loads(clean)

        st.markdown("#### 🗂️ What You'll Actually Do")
        st.info(jd["role_summary"])

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### ✅ Must Have")
            for req in jd["key_requirements"]:
                st.markdown(f"- {req}")
        with col2:
            st.markdown("#### 💡 Nice to Have")
            for req in jd["nice_to_have"]:
                st.markdown(f"- {req}")

        st.markdown("#### 🛂 Visa & Sponsorship Situation")
        st.warning(f"🛂 {jd['sponsorship_situation']}")

        st.markdown("#### 🏢 What The Company Really Wants")
        st.write(jd["company_expectations"])

        col1, col2 = st.columns(2)
        with col1:
            difficulty = jd["difficulty_level"]
            if "Easy" in difficulty:
                st.success(f"📊 Difficulty: {difficulty}")
            elif "Medium" in difficulty:
                st.warning(f"📊 Difficulty: {difficulty}")
            else:
                st.error(f"📊 Difficulty: {difficulty}")
        with col2:
            rec = jd["apply_recommendation"]
            if rec.startswith("Yes"):
                st.success(f"✈️ Apply? {rec}")
            elif rec.startswith("Maybe"):
                st.warning(f"✈️ Apply? {rec}")
            else:
                st.error(f"✈️ Apply? {rec}")

    except Exception as e:
        st.error(f"Error: {e}")

def display_bullet_rewrites(bullets):
    st.markdown("---")
    st.markdown("### ✍️ Auto-Rewritten Bullet Points")
    for i, item in enumerate(bullets, 1):
        st.markdown(f"**Bullet {i}:**")
        st.markdown(f'<div class="bullet-old">❌ Original: {item["original"]}</div>',
            unsafe_allow_html=True)
        st.markdown(f'<div class="bullet-new">✅ Rewritten: {item["rewritten"]}</div>',
            unsafe_allow_html=True)
        st.markdown("")

def display_cover_letter(cover_letter, company_name, key_suffix=""):
    st.markdown("---")
    st.markdown("### 📝 Your Cover Letter")
    st.success("✅ Cover Letter Ready!")
    st.markdown(cover_letter)
    st.download_button(
        label="📥 Download Cover Letter",
        data=cover_letter,
        file_name=f"cover_letter_{company_name}.txt",
        mime="text/plain",
        key=f"download_{key_suffix}"
    )

# ── SINGLE JOB MODE ──
if "Single" in mode:

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📄 Upload Your Resume")
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    with col2:
        st.subheader("💼 Paste Job Description")
        job_description = st.text_area("Job Description", height=150,
            placeholder="Paste the job description here...")

    st.markdown("### 📝 Cover Letter Details")
    st.markdown("*Fill these in now so your cover letter is ready after analysis*")
    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input("Company Name",
            placeholder="e.g. Google, Microsoft...")
    with col2:
        job_title_input = st.text_input("Job Title",
            placeholder="e.g. ML Engineer, Data Scientist...")

    if st.button("🔍 Analyze, Explain, Rewrite & Generate Cover Letter",
                 type="primary"):
        if not uploaded_file:
            st.error("Please upload your resume!")
        elif not job_description:
            st.error("Please paste a job description!")
        else:
            resume_text = extract_text_from_pdf(uploaded_file)

            with st.spinner("Step 1/3 — Analyzing resume match..."):
                result = analyze_resume(resume_text, job_description)
            try:
                clean = result.strip().replace("```json", "").replace("```", "")
                data = json.loads(clean)
            except:
                st.error("Error analyzing resume")
                st.stop()

            with st.spinner("Step 2/3 — Rewriting bullet points..."):
                bullets_raw = rewrite_all_bullets(resume_text, job_description)
                try:
                    bullets_clean = bullets_raw.strip().replace("```json","").replace("```","")
                    bullets = json.loads(bullets_clean)
                except:
                    bullets = []

            cover_letter = ""
            if company_name and job_title_input:
                with st.spinner("Step 3/3 — Generating cover letter..."):
                    cover_letter = generate_cover_letter(
                        resume_text, job_description,
                        company_name, job_title_input)

            st.session_state["single_analysis"] = data
            st.session_state["single_bullets"] = bullets
            st.session_state["single_jd"] = job_description
            st.session_state["single_cover_letter"] = cover_letter
            st.session_state["single_company"] = company_name

    if "single_analysis" in st.session_state:
        data = st.session_state["single_analysis"]
        bullets = st.session_state["single_bullets"]
        cover_letter = st.session_state["single_cover_letter"]
        company = st.session_state["single_company"]
        job_desc = st.session_state["single_jd"]

        st.markdown("---")
        display_scores(data)
        display_jd_explainer(job_desc)
        display_bullet_rewrites(bullets)
        if cover_letter:
            display_cover_letter(cover_letter, company, key_suffix="single")
        else:
            st.markdown("---")
            st.info("💡 Enter company name and job title before clicking analyze to get a cover letter!")

# ── MULTI JOB MODE ──
elif "Compare" in mode:

    st.subheader("📄 Upload Your Resume")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    st.subheader("💼 Paste Job Descriptions")
    col1, col2, col3 = st.columns(3)
    with col1:
        job1_title = st.text_input("Job 1 Title", placeholder="e.g. ML Engineer")
        job1 = st.text_area("Job 1 Description", height=150, placeholder="Paste job 1...")
    with col2:
        job2_title = st.text_input("Job 2 Title", placeholder="e.g. Data Engineer")
        job2 = st.text_area("Job 2 Description", height=150, placeholder="Paste job 2...")
    with col3:
        job3_title = st.text_input("Job 3 Title", placeholder="e.g. Backend Engineer")
        job3 = st.text_area("Job 3 Description", height=150, placeholder="Paste job 3...")

    if st.button("⚖️ Compare All Jobs", type="primary"):
        if not uploaded_file:
            st.error("Please upload your resume!")
        else:
            jobs = [
                (job1_title or "Job 1", job1),
                (job2_title or "Job 2", job2),
                (job3_title or "Job 3", job3)
            ]
            jobs = [(t, d) for t, d in jobs if d.strip()]

            if not jobs:
                st.error("Please paste at least one job description!")
            else:
                resume_text = extract_text_from_pdf(uploaded_file)
                results = []
                with st.spinner("Analyzing all jobs..."):
                    for title, desc in jobs:
                        result = analyze_resume(resume_text, desc)
                        try:
                            clean = result.strip().replace("```json","").replace("```","")
                            data = json.loads(clean)
                            results.append((title, desc, data))
                        except:
                            st.warning(f"Could not parse result for {title}")

                st.session_state["results"] = results
                st.session_state["resume_text"] = resume_text

    if "results" in st.session_state and st.session_state["results"]:
        results = st.session_state["results"]
        resume_text = st.session_state["resume_text"]
        best = max(results, key=lambda x: x[2]["match_score"])

        st.markdown("---")
        st.markdown("## 🏆 Job Comparison")

        cols = st.columns(len(results))
        for i, (title, desc, data) in enumerate(results):
            with cols[i]:
                score = data["match_score"]
                if title == best[0]:
                    st.success(f"🏆 {title}")
                    st.metric("Score", f"{score}/100")
                    st.success("⭐ BEST MATCH")
                else:
                    st.info(f"📋 {title}")
                    st.metric("Score", f"{score}/100")

        st.markdown("---")
        st.markdown("### 🎯 Which jobs do you want full analysis for?")

        selected_jobs = []
        check_cols = st.columns(len(results))
        for i, (title, desc, data) in enumerate(results):
            with check_cols[i]:
                checked = st.checkbox(
                    f"{title} ({data['match_score']}/100)",
                    value=(title == best[0]),
                    key=f"check_{i}"
                )
                if checked:
                    selected_jobs.append((title, desc, data))

        st.markdown("### 📝 Cover Letter Details")
        multi_company = st.text_input("Company Name",
            placeholder="e.g. Google")

        if st.button("📋 Get Full Analysis + Cover Letters", type="primary"):
            if not selected_jobs:
                st.error("Please select at least one job!")
            else:
                multi_bullets = {}
                multi_cover_letters = {}

                for title, desc, data in selected_jobs:
                    with st.spinner(f"Rewriting bullets for {title}..."):
                        bullets_raw = rewrite_all_bullets(resume_text, desc)
                        try:
                            bullets_clean = bullets_raw.strip().replace("```json","").replace("```","")
                            multi_bullets[title] = json.loads(bullets_clean)
                        except:
                            multi_bullets[title] = []

                    if multi_company:
                        with st.spinner(f"Generating cover letter for {title}..."):
                            letter = generate_cover_letter(
                                resume_text, desc, multi_company, title)
                            multi_cover_letters[title] = letter

                st.session_state["selected_jobs"] = selected_jobs
                st.session_state["multi_bullets"] = multi_bullets
                st.session_state["multi_cover_letters"] = multi_cover_letters
                st.session_state["multi_company"] = multi_company

    if "selected_jobs" in st.session_state and st.session_state["selected_jobs"]:
        resume_text = st.session_state["resume_text"]
        multi_bullets = st.session_state.get("multi_bullets", {})
        multi_cover_letters = st.session_state.get("multi_cover_letters", {})
        company = st.session_state.get("multi_company", "")

        for i, (title, desc, data) in enumerate(
                st.session_state["selected_jobs"]):
            st.markdown("---")
            st.markdown(f"## 📋 Full Analysis: {title}")
            display_scores(data)
            display_jd_explainer(desc)
            if title in multi_bullets:
                display_bullet_rewrites(multi_bullets[title])
            if title in multi_cover_letters:
                display_cover_letter(
                    multi_cover_letters[title], company,
                    key_suffix=f"multi_{i}")