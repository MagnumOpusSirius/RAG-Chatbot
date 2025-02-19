# RAG Chatbot for PDF Document Processing

This project is a Retrieval-Augmented Generation (RAG) Chatbot designed to process and query knowledge bases stored in PDF documents. The system extracts text and images from PDFs, preprocesses the data, and stores it in a vector database (Pinecone) for efficient retrieval. The chatbot uses LLM's and other techniques to provide meaningful responses to user queries.

## Steps to Build

1. Preprocess the Knowledge Base
     - Extract Text and Images from PDFs:
       - Use tools like PyPDF2, pdfplumber, or OCR (e.g., Tesseract) for scanned PDFs.
       - File: src/extract_text.py
     - Clean and Structure the Data:
       - Split text into chunks.
       - Remove irrelevant content (e.g., headers, footers, special characters).
       - File: src/preprocess.py

2. Set Up a Retrieval System
     - Store Embeddings in Pinecone:
       - Convert cleaned text into embeddings using models like OpenAI's GPT-4 or BERT.
       - Store embeddings in Pinecone for efficient retrieval.
       - File: src/store_embeddings.py
     - Query the Vector DB:
       - Retrieve relevant chunks from Pinecone based on user queries.
       - File: src/query_pinecone.py

3. Build the Chatbot
    - Integrate Retrieval and Generation:
      - Use retrieved chunks as context for generating responses using OpenAI's GPT-4.
      - File: src/vector_db.py


NOTE: Due to proprietary reasons, cannot share the document/PDF to public. Please use your own PDF as input, OpenAI API Key and Pinecone API to test.

## Project structure:
```
rag_chatbot/
│── data/                   # Stores raw PDFs  
│── processed_data/         # Stores cleaned text files  
│── src/                    # Source code  
│   ├── extract_text.py     # Extracts text from PDFs  
│   ├── preprocess.py       # Cleans and chunks text   
│   ├── query_pinecone.py   # Main chatbot logic  
│   ├── split.py            # Splits text logic
│   ├── store_embeddings.py # Stores embedding logic
│   ├── vector_db.py        # Retrieves data from vector DB 
│── venv/                       # Virtual env for dependencies
│── config.yaml                 # Configuration settings  
│── requirements.txt            # Python dependencies
│── example_workflow_OCR.py     # Example of OCR usage
│── README.md                   # Project documentation 
```

---
## Detailed Steps

### Step 1: Extracting Text from PDFs

  - Tools:
    - PyMuPDF (fitz) for structured text extraction.
    - Tesseract OCR for extracting text from images in scanned PDFs.

  - File: src/extract_text.py

### Step 2: Clean & Preprocess Extracted Text

  - Tasks:

    - Remove noise (extra spaces, broken words, special characters).
    - Fix line breaks (combine fragmented sentences).
    - Normalize spacing (ensure words aren’t stuck together).
    - Lowercase text (optional, depends on use case).
    - Chunk text into meaningful sections.

- File: src/preprocess.py


### Step 3: Splitting Text into Chunks
- Why Chunking?:
  - Improves retrieval accuracy in a vector DB. 
  - Ensures meaningful responses when querying the chatbot.
  - Maintains context in long documents (avoids incomplete sentences).

- Approach:
  - Split by headings and sections (if present).
  - Split by sentence boundaries (using nltk library).
  - Maintain a reasonable chunk size (e.g., 200-500 words).
- Dependencies: nltk
- File: src/split_text.py

### Step 4: Store Embeddings in Pinecone
- Tasks:
  - Convert cleaned and chunked text into embeddings using OpenAI's GPT-4 or BERT.
  - Store embeddings in Pinecone for efficient retrieval.

- File: src/store_embeddings.py

### Step 5: Query the Vector Database
- Tasks:
  - Retrieve relevant chunks from Pinecone based on user queries.
  - Use retrieved chunks as context for generating responses using OpenAI's GPT-4.

- File: src/query_pinecone.py

---
## Algorithms/Models to Consider

* BM25: Ranking function used by search engines to rank matching documents.

* TF-IDF: Term Frequency-Inverse Document Frequency for text retrieval.

* Word2Vec: Word embeddings for semantic similarity.

* Doc2Vec: Document embeddings for semantic similarity.

* BERT: Contextual embeddings for improved retrieval.

* GPT-4: Generative model for response generation.

* Pinecone: Vector database for efficient storage and retrieval of embeddings.

---

## Setup Instructions:

#### Install dependencies:
Create a virtual environment:

``` 
source venv/bin/activate 
```
Use requirements.txt:

```
# Core dependencies
python-dotenv==1.0.0         # For managing API keys & environment variables
PyMuPDF==1.23.7             # PDF text extraction (fitz)
pdfplumber==0.10.2          # Alternative PDF extraction (tables & text)
pytesseract==0.3.10         # OCR for scanned PDFs (requires Tesseract installed)
opencv-python==4.9.0.80     # Image processing (for OCR preprocessing)
numpy==1.26.3               # Numerical operations

# Text processing & chunking
nltk==3.8.1                 # Natural language processing
sentence-transformers==2.2.2 # BERT-based embeddings
tiktoken==0.5.2             # Tokenization for GPT models

# Vector database
pinecone-client==3.0.0      # Pinecone for vector storage & retrieval

# OpenAI API
openai==1.11.1              # GPT-4 & embeddings API

# Web framework (Optional: If planning a FastAPI-based chatbot)
fastapi==0.110.0            # Web API framework
uvicorn==0.27.1             # ASGI server for FastAPI

# Extra utilities
scikit-learn==1.4.1.post1   # TF-IDF, BM25, and other NLP techniques
torch==2.1.2               # Required for sentence-transformers
```
To run:
``` 
pip install -r requirements.txt
```

Configure your API Keys:
- Add your OpenAI and Pinecone API keys to .env, or you can use config.yaml

```
openai_api_key: "your_openai_api_key"
pinecone_api_key: "your_pinecone_api_key"
```

#### Run the workflow in this order:
- ``` python src/extract_text.py ```
- ``` python src/preprocess.py ```
- ``` python src/preprocess.py ```
- ``` python src/store_embeddings.py ```
- ``` python src/query_pinecone.py ```

---
## NOTE
- Due to proprietary reasons, the document/PDF used in this project cannot be shared publicly. Please use your own PDF, OpenAI API Key, and Pinecone API to test.

## Extra resources:
During/or prior to chunks clean file creation make sure we are running the nltk resources in the /src folder.
1. in a python bash:
    1. import nltk
    2. nltk.download('punkt')
    3. nltk.download('punkt_tab')


