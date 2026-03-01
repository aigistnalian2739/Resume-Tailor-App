import os
import re
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from docx import Document
from collections import Counter
from datetime import datetime

class ResumeTailor:
    def __init__(self):
        self.stop_words = {'and', 'the', 'with', 'our', 'you', 'will', 'for', 'requirements', 'experience', 'ability', 'work', 'team'}
        self.industry_keywords = {'python', 'java', 'sql', 'project', 'management', 'agile', 'scrum', 'aws', 'cloud', 'data'}

    def extract_keywords(self, text, num=6):
        words = re.findall(r'\w+', text.lower())
        filtered = [w for w in words if w not in self.stop_words and len(w) > 3]
        counts = Counter(filtered)
        for word in counts:
            if word in self.industry_keywords:
                counts[word] *= 2
        return ", ".join([w[0].capitalize() for w in counts.most_common(num)])

    def generate(self, template_path, company, role, jd_text, years_exp, industry):
        try:
            if not template_path or not os.path.exists(template_path):
                messagebox.showerror("Error", "Please select a valid 'master_resume.docx' file first!")
                return

            skills = self.extract_keywords(jd_text)
            doc = Document(template_path)
            
            replacements = {
                "{{COMPANY}}": company,
                "{{ROLE}}": role,
                "{{SKILLS}}": skills,
                "{{YEARS_EXP}}": years_exp,
                "{{TARGET_INDUSTRY}}": industry,
                "{{DATE}}": datetime.now().strftime("%B %Y")
            }

            for p in doc.paragraphs:
                for key, val in replacements.items():
                    if key in p.text:
                        p.text = p.text.replace(key, val)

            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for key, val in replacements.items():
                            if key in cell.text:
                                cell.text = cell.text.replace(key, val)

            output_folder = os.path.join(os.path.expanduser("~"), "Desktop", "Tailored_Resumes")
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            output_path = f"{output_folder}/Resume_{company.replace(' ', '_')}.docx"
            doc.save(output_path)
            messagebox.showinfo("Success", f"Resume Generated on Desktop!\nFolder: {output_folder}")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

def launch_gui():
    root = tk.Tk()
    root.title("AI Resume Tailor")
    root.geometry("600x750")
    
    # Template Selection
    template_var = tk.StringVar()
    tk.Label(root, text="Step 1: Select Your Master Template", font=("Arial", 10, "bold")).pack(pady=5)
    
    def browse_file():
        filename = filedialog.askopenfilename(filetypes=[("Word files", "*.docx")])
        template_var.set(filename)

    tk.Button(root, text="Browse for master_resume.docx", command=browse_file).pack()
    tk.Label(root, textvariable=template_var, fg="blue", wraplength=500).pack(pady=5)

    # Inputs
    tk.
