# backend/pdf_generator.py

from fpdf import FPDF

def save_resume_to_pdf(resume_text: str, filename: str = "resume.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in resume_text.split("\n"):
        pdf.multi_cell(0, 10, txt=line, align='L')
    pdf.output(filename)
    print(f"✅ Resume saved as {filename}")

