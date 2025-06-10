# app.py

import streamlit as st
from resume_generate import generate_resume_from_jobs
from semantic_search import semantic_search
from fpdf import FPDF

# Streamlit UI
st.set_page_config(page_title="AI Resume Generator", layout="centered")
st.title("🧠 AI Resume Generator")
st.markdown("Generate a professional resume based on your job interest using real job listings.")

job_title = st.text_input("🎯 Enter your desired job title", placeholder="e.g., Data Scientist")

if st.button("Generate Resume"):
    if not job_title.strip():
        st.warning("Please enter a job title.")
    else:
        st.info("🔍 Searching job listings...")
        matches = semantic_search(job_title)

        if not matches:
            st.error("No matching jobs found. Try another title.")
        else:
            st.success(f"Found {len(matches)} matching jobs!")

            # Show preview of jobs
            for job in matches[:5]:
                st.write(f"**🏢 {job.get('company_name', 'N/A')} - {job.get('job_title', 'N/A')}**")
                st.write(
                    f"{job.get('employment_type', 'N/A')} | {job.get('seniority_level', 'N/A')} | {job.get('location', 'N/A')} | Industry: {job.get('industry', 'N/A')}"
                )
                st.markdown("---")

            st.info("📝 Generating resume...")

            try:
                # Generate resume using jobs
                resume_text = generate_resume_from_jobs(job_title, matches[:5])

                # Save resume to PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)

                for line in resume_text.split('\n'):
                    pdf.multi_cell(0, 10, line)

                filename = f"{job_title.replace(' ', '_').lower()}_resume.pdf"
                pdf.output(filename)

                st.success("✅ Resume generated and saved!")
                with open(filename, "rb") as f:
                    st.download_button("📄 Download Resume", f, file_name=filename)
            except Exception as e:
                st.error(f"❌ Error: {e}")

