import os
import re
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import google.generativeai as genai
from docx import Document
from datetime import datetime

# --- SECURITY: Load API Key from Environment ---
# Ensure you have set GEMINI_API_KEY in your System Environment Variables
API_KEY = os.getenv("GEMINI_API_KEY")

class GeminiResumeTailor:
    def __init__(self):
        if not API_KEY:
            messagebox.showerror("Security Error", "API Key not found! Please set GEMINI_API_KEY in Environment Variables.")
            return
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def get_ai_tailoring(self, jd_text, company, role):
        """Uses Gemini to generate tailored content based on the JD."""
        prompt = f"""
        Act as a Senior IT Career Coach. I am applying for the {role} position at {company}.
        Based on this Job Description: {jd_text}
        
        Please provide:
        1. A list of the 6 most critical technical keywords found in the JD.
        2. A 2-sentence professional summary perfectly tailored to this role.
        
        Return ONLY in this format:
        KEYWORDS: word1, word2, word3...
        SUMMARY: [Your tailored summary here]
        """
        response = self.model.generate_content(prompt)
        return response.text

    def generate(self, template_path, company, role, jd_text, years_exp, industry):
        try:
            if not template_path or not os.path.exists(template_path):
                messagebox.showerror("Error", "Please select your master_resume.docx first!")
                return

            # Get AI Insights
            ai_output = self.get_ai_tailoring(jd_text, company, role)
            
            # Simple parsing of AI response
            keywords = re.search(r"KEYWORDS: (.*)", ai_output).group(1) if "KEYWORDS:" in ai_output else "N/A"
            ai_summary = re.search(r"SUMMARY: (.*)", ai_output).group(1) if "SUMMARY:" in ai_output else ""

            doc = Document(template_path)
            replacements = {
                "{{COMPANY}}": company,
                "{{ROLE}}": role,
                "{{SKILLS}}": keywords,
                "{{AI_SUMMARY}}": ai_summary, # New tag for the AI rewrite
                "{{YEARS_EXP}}": years_exp,
                "{{TARGET_INDUSTRY}}": industry,
                "{{DATE}}": datetime.now().strftime("%B %Y")
            }

            # Recursive replacement
            for p in doc.paragraphs:
                for key, val in replacements.items():
                    if key in p.text:
                        p.text = p.text.replace(key, val)

            output_folder = os.path.join(os.path.expanduser("~"), "Desktop", "Tailored_Resumes")
            if not os.path.exists(output_folder): os.makedirs(output_folder)

            output_path = f"{output_folder}/AI_Resume_{company.replace(' ', '_')}.docx"
            doc.save(output_path)
            messagebox.showinfo("Success", f"AI-Tailored Resume saved to Desktop!")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

# [GUI implementation follows same structure as previous turn, calling GeminiResumeTailor().generate]
