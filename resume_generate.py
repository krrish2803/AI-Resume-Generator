from groq import Groq

import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


def generate_resume_from_jobs(job_title: str, job_listings: list) -> str:
    combined_text = ""
    for job in job_listings:
        combined_text += (
            f"Job Title: {job.get('job_title', 'N/A')}, "
            f"Company: {job.get('company_name', 'N/A')}, "
            f"Employment Type: {job.get('employment_type', 'N/A')}, "
            f"Seniority Level: {job.get('seniority_level', 'N/A')}, "
            f"Location: {job.get('location', 'N/A')}, "
            f"Industry: {job.get('industry', 'N/A')}\n"
        )

    prompt = f"""
    You are a professional resume writing assistant. Based on the job title '{job_title}' and the following job summaries:

    {combined_text}

    Generate a detailed and attractive resume including:
    - A compelling Summary
    - Skills inferred from the listings
    - Relevant Experience (fictional but aligned)
    - Education (typical for such roles)
    """
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ Error generating resume: {e}")
        return "Resume generation failed."


