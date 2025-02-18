import pinecone
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys from environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate that keys are loaded
if not PINECONE_API_KEY or not OPENAI_API_KEY:
    raise ValueError("Missing API keys! Ensure they are set in the .env file.")

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Initialize Pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

# Define index name
INDEX_NAME = "rag-chatbot"

# Create index if it doesn't exist
if INDEX_NAME not in pinecone.list_indexes():
    pinecone.create_index(INDEX_NAME, dimension=1536, metric="cosine")

# Connect to the index
index = pinecone.Index(INDEX_NAME)

def get_embedding(text):
    """Generates embeddings for the given text using OpenAI's model."""
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response["data"][0]["embedding"]