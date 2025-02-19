import os
import pinecone
import openai
from dotenv import load_dotenv 

# Load environment variables from .env file
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENVIRONMENT")  # Example: "gcp-starter"
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")  # find tje index name in Pinecone when you create it
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Initialize Pinecone client (NEW v3+ method)
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

try:
    index = pc.Index(PINECONE_INDEX_NAME)
    print(f"✅ Connected to Pinecone index: {PINECONE_INDEX_NAME}")
except Exception as e:
    print(f"❌ Error connecting to Pinecone: {e}")
    exit(1)

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_embedding(text):
    """Generate embedding using OpenAI's API."""
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding  

def query_pinecone(embedding, top_k=5):
    """Query Pinecone and return relevant documents."""
    try:
        results = index.query(vector=embedding, top_k=top_k, include_metadata=True, timeout=10)
        return results
    except pinecone.core.client.exceptions.PineconeException as e:
        print(f"❌ Pinecone query error: {e}")
        return None

def generate_answer(question, context):
    """Use OpenAI to generate a concise response based on retrieved context."""
    prompt = f"""
    You are an intelligent chatbot. Answer the following question in 1-2 sentences based on the given context.
    If the context does not provide enough information, say "I don't have enough information to answer that."

    Question: {question}
    
    Context: {context}

    Answer:
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Get user query
query = input("Enter your search query: ")

# Generate query embedding
query_embedding = get_embedding(query)

# Retrieve relevant results from Pinecone
results = query_pinecone(query_embedding)

if not results or not results.matches:
    print("❌ No relevant information found.")
else:
    # Extract top matches as context
    context = " ".join([match.metadata["text"] for match in results.matches])

    # Generate an answer based on context
    answer = generate_answer(query, context)
    print("\n💡 **Answer:**", answer)