# 🤖 AI Resume & Job Match Analyzer

An AI-powered web app that analyzes your resume against any job description and gives you a complete action plan — match score, skill gaps, rewritten bullets, and a personalized cover letter.

## 🚀 Live Demo
👉 **[Try it live here](https://hema-resume-analyzer.streamlit.app/)**

---

## ✨ Features

- 🎯 **AI Match Score** — Get a score out of 100 showing how well your resume matches the job
- ✅ **Skill Badges** — See matching skills in green and missing skills in red at a glance
- 📖 **JD Explainer** — Breaks down the job description in simple words for OPT/F1 students
- 🛂 **Visa & Sponsorship Info** — Clearly explains the sponsorship situation for each job
- ⚖️ **Multi-Job Comparison** — Compare up to 3 jobs and find your best match automatically
- ✍️ **Auto Bullet Rewriter** — AI rewrites all your resume bullets to match the job
- 📝 **Cover Letter Generator** — Generates a personalized cover letter with OPT authorization mention
- 📥 **Download** — Download your cover letter as a text file instantly

---

## 🛠️ Tech Stack

- **Python** — core language
- **Streamlit** — web UI framework
- **Groq API + LLaMA 3.1** — AI analysis engine
- **PyPDF2** — PDF text extraction
- **python-dotenv** — secure API key management

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/HemaTejaswi7092/resume-analyzer.git
cd resume-analyzer
pip install -r requirements.txt
# Create .env file and add your Groq API key
echo 'GROQ_API_KEY=your_key_here' > .env
streamlit run app.py
```

## 🔑 Setup

1. Get a free API key from [console.groq.com](https://console.groq.com)
2. Create a `.env` file in the project folder
3. Add: `GROQ_API_KEY=your_key_here`

---

## 📸 How It Works

1. Upload your resume as a PDF
2. Choose Single Job or Compare 2-3 Jobs
3. Paste job description(s)
4. Enter company name and job title for cover letter
5. Click Analyze — get everything in one shot

---

## 🔮 Coming Soon

- Interview question predictor based on job description
- LinkedIn profile optimizer
- Salary range estimator

---

## 👩‍💻 Built By

**Hema Tejaswi Manchikalapudi**  
MS CS @ UCF | OPT Authorized | Open to Work  
[LinkedIn](https://www.linkedin.com/in/hematejaswimanchikalapudi) · [GitHub](https://github.com/HemaTejaswi7092)
