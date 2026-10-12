
# 🌈 InclusiveCareer AI

### Skills Over Barriers, Opportunities for Everyone

InclusiveCareer AI is an inclusive career exploration platform that helps users discover roles based on their skills, identify skill gaps, and explore learning resources.

## 🎯 Problem Statement

People can struggle to identify suitable career opportunities and understand which skills they need to develop. Traditional job descriptions can make this process confusing, especially for beginners and career changers.

## 💡 Our Solution

InclusiveCareer AI provides a simple, skills-focused experience to help users explore career options and plan their learning journey.

## ✨ Key Features

- 📄 Resume upload and keyword-based skill detection
- 🧭 Career recommendations based on selected skills
- 📊 Skill-match scores for sample job roles
- 🪴 Skill-gap analysis for a selected career goal
- 🗺️ Personalized learning roadmap
- 🔗 Learning resources and practical project suggestions
- ♿ Friendly interface designed with readability in mind

## 🛠️ Technology Stack

- Python
- Streamlit
- Pandas (if used elsewhere in the project)
- PyMuPDF for PDF text extraction
- CSV sample job dataset

## 📁 Project Structure

```text
InclusiveCareerAI/
├── data/
│   └── jobs.csv
├── src/
│   ├── matching.py
│   ├── resume_parser.py
│   ├── skill_gap.py
│   └── roadmap.py
├── tests/
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## 🚀 How to Run

### 1. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Start the app

```bash
python -m streamlit run app.py
```

## 📊 How Matching Works

The prototype compares selected user skills with the skills listed for each sample job role.

The match score is calculated as:

Matched required skills ÷ Total listed required skills × 100

This is a skill-coverage score, not a probability of being hired.

## 🔒 Responsible Use and Limitations

- The current job dataset contains sample roles.
- Resume parsing uses keyword detection and may miss skills expressed differently.
- Scanned PDFs may require OCR.
- Recommendations are informational and do not guarantee employment.
- Users should review and confirm detected skills.

## 🔮 Future Enhancements

- Expand and validate the job dataset.
- Add more career paths and skill synonyms.
- Introduce accessible learning progress tracking.
- Improve resume parsing and skill extraction.
- Explore integration with SAP services where appropriate and available.

## 👥 Project

**Project name:** InclusiveCareer AI  
**Hackathon:** SAP HackFest 2026  
**Tagline:** Skills Over Barriers, Opportunities for Everyone.
