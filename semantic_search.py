# backend/semantic_search.py

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from utils import get_embedding
import numpy as np

load_dotenv()

# MongoDB connection
def get_mongo_connection():
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise ValueError("❌ MONGODB_URI not found in environment variables.")

    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas!")
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        raise e

    return client

# Cosine similarity calculator
def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Semantic search function
def semantic_search(query: str, top_k: int = 5):
    client = get_mongo_connection()
    collection = client["joblens"]["jobs"]

    query_embedding = get_embedding(query)
    if not query_embedding:
        print("⚠️ Could not compute query embedding.")
        return []

    documents = collection.find({"embedding": {"$exists": True}})
    results = []

    for doc in documents:
        doc_embedding = doc["embedding"]
        score = cosine_similarity(query_embedding, doc_embedding)

        # Add the score to each document
        doc["score"] = score
        results.append(doc)

    # Sort documents by score
    top_matches = sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]
    return top_matches

# Test/CLI usage
if __name__ == "__main__":
    query = input("Enter your job interest or skill (e.g., 'data science in healthcare'): ")
    top_matches = semantic_search(query)

    print(f"\n🔍 Top matching jobs for: '{query}' ({len(top_matches)} found)\n")
    for job in top_matches:
        print(
            f"🏢 {job.get('company_name', 'N/A')} - {job.get('job_title', 'N/A')} - "
            f"{job.get('location', 'N/A')} - {job.get('seniority_level', 'N/A')} - "
            f"{job.get('employment_type', 'N/A')} - {job.get('industry', 'N/A')}"
        )
        print(f"🎯 Score: {round(job.get('score', 0.0), 4)}")
        print("-" * 60)
