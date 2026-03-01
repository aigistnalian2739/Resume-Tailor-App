# ResumeTailor-AI 🤖
A desktop-based Python application that uses simple NLP to tailor your resume to a specific job description instantly.

### How it works:
1. It scans the Job Description for high-frequency keywords.
2. It injects those keywords into your `master_resume.docx` using `{{TAGS}}`.
3. It creates a personalized version in the `/Tailored_Resumes` folder.

### Setup:
1. Clone this repo.
2. Run `pip install python-docx`.
3. Ensure your `master_resume.docx` uses the tags: `{{COMPANY}}`, `{{ROLE}}`, `{{SKILLS}}`, `{{YEARS_EXP}}`.
4. Run `python ResumeMaker.py`.
