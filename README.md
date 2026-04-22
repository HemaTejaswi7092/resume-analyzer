# 🤖 AI Resume & Job Match Analyzer

An AI-powered web app that analyzes your resume against any job description and gives you a detailed match report.

## ✨ Features
- 📄 Upload your resume as PDF
- 💼 Paste any job description
- 🎯 Get a match score out of 100
- ✅ See your top matching skills
- ❌ See missing skills you need to add
- 📝 Get AI-rewritten bullet points tailored to the job
- 💡 Overall recommendation from AI

## 🛠️ Tech Stack
- **Python** — core language
- **Streamlit** — web UI framework
- **Groq API + LLaMA 3.3** — AI analysis engine
- **PyPDF2** — PDF text extraction
- **python-dotenv** — secure API key management

## 🚀 How to Run Locally
```bash
git clone https://github.com/HemaTejaswi7092/resume-analyzer.git
cd resume-analyzer
pip install -r requirements.txt
# Add your Groq API key to .env file
streamlit run app.py
```

## 🔑 Setup
1. Get a free API key from [console.groq.com](https://console.groq.com)
2. Create a `.env` file in the project folder
3. Add: `GROQ_API_KEY=your_key_here`

## 📸 Demo
> Upload your resume PDF + paste a job description → get instant AI analysis

## 🔮 Coming Soon
- Visual score cards with color coding
- Resume bullet point rewriter
- Multi-job comparison
- Cover letter generator
