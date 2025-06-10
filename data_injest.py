# backend/injest.py

import pandas as pd
from tqdm import tqdm
from utils import get_embedding, get_mongo_connection

# Load CSV data
try:
    df = pd.read_csv('linkedin_jobs.csv')
    print(f"📄 Loaded dataset with {len(df)} job listings.")
except FileNotFoundError:
    print("❌ Error: File 'linkedin_jobs.csv' not found.")
    exit()

# MongoDB connection
client = get_mongo_connection()
collection = client["joblens"]["jobs"]

# Optional: Clean up previous data
delete_existing = input("Do you want to delete existing data? (y/n): ").lower()
if delete_existing == 'y':
    deleted = collection.delete_many({})
    print(f"🧹 Deleted {deleted.deleted_count} old documents.")

print(f"🚀 Processing and ingesting {len(df)} job listings...")

for _, row in tqdm(df.iterrows(), total=len(df)):
    job_title = row.get('job_title', '')
    company_name = row.get('company_name', '')
    location = row.get('location', '')
    hiring_status = row.get('hiring_status', '')
    date = row.get('date', '')
    seniority_level = row.get('seniority_level', '')
    employment_type = row.get('employment_type', '')
    industry = row.get('industry', '')

    # Create rich text for embedding
    text = (
        f"{job_title} at {company_name}, {employment_type}, "
        f"{seniority_level}, {location}. Industry: {industry}."
    )

    embedding = get_embedding(text)
    if not embedding:
        continue

    job_doc = {
        "job_title": job_title,
        "company_name": company_name,
        "location": location,
        "hiring_status": hiring_status,
        "date": date,
        "seniority_level": seniority_level,
        "employment_type": employment_type,
        "industry": industry,
        "embedding": embedding
    }

    try:
        result = collection.insert_one(job_doc)
    except Exception as e:
        print(f"⚠️ Error inserting document: {e}")
        continue
    