import os
import pinecone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "my-index"

pinecone_client = pinecone.Pinecone(api_key=PINECONE_API_KEY)
index = pinecone_client.Index(INDEX_NAME)

# Get index stats
stats = index.describe_index_stats()
print("\n📊 Pinecone Index Stats:", stats)