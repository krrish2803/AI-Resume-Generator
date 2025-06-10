# backend/utils.py

from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

# Load Sentence Transformer model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str) -> list:
    try:
        embedding = model.encode(text)
        return embedding.tolist()
    except Exception as e:
        print(f"Embedding failed: {e}")
        return []

def get_mongo_connection():
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise ValueError("MONGODB_URI not found in .env file")

    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas!")
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        raise e

    return client

if __name__ == "__main__":
    client = get_mongo_connection()
    collection = client["joblens"]["jobs"]
    print("Total documents:", collection.count_documents({}))
    print("Documents with embeddings:", collection.count_documents({"embedding": {"$exists": True}}))
