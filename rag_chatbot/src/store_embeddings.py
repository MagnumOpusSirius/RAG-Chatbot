import os
from pinecone import Pinecone, ServerlessSpec
import openai
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Retrieve API keys
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Initialize Pinecone Client
pc = Pinecone(api_key=PINECONE_API_KEY)
print(pc.list_indexes())

# Define the index if it doesn't exist
index_name = "my-index"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # Ensure this matches your embedding model's output dimension
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"  # Change this to your Pinecone region
        )
    )

index = pc.Index(name=index_name)  # Corrected

def get_embedding(text):
    """Generate embedding for a given text using OpenAI API (new syntax)."""
    response = openai.embeddings.create(
        input=text,  # Single text input (not a list)
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding  # Extract the embedding

def store_embeddings(text_chunks):
    """Stores text chunks as embeddings in Pinecone."""
    for i, chunk in enumerate(text_chunks):
        vector = get_embedding(chunk)
        print(f"Storing chunk-{i}: {chunk[:50]}...")  # Print first 50 characters
        index.upsert(vectors=[(f"chunk-{i}", vector, {"text": chunk})])

if __name__ == "__main__":
    # Load text chunks from JSON
    with open("processed_data/chunks.json", "r") as f:
        text_chunks = json.load(f)
    
    store_embeddings(text_chunks)
    print("✅ All embeddings stored in Pinecone!")