import os
import pinecone
from dotenv import load_dotenv
import openai



# Load environment variables
load_dotenv()

# Get API key and index name
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "my-index"

# Initialize Pinecone client
pinecone_client = pinecone.Pinecone(api_key=PINECONE_API_KEY)

# Get index reference
index = pinecone_client.Index(INDEX_NAME)

# Fetch index statistics
stats = index.describe_index_stats()

print(f"✅ Pinecone Index '{INDEX_NAME}' Stats:")
print(stats)

# Check if vectors exist in a specific namespace
for namespace, data in stats.get("namespaces", {}).items():
    print(f"📂 Namespace '{namespace}': {data}")

# Confirm the embeddings are actually generated.
embedding = openai.embeddings.create(input=["test"], model="text-embedding-ada-002").data
print(embedding)

if stats["total_vector_count"] == 0:
    print("🚨 No embeddings found! Check if they were stored in a namespace.")