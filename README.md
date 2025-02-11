# Steps to build:
1. Preprocess the knowledge base:
    - Extract text and images from PDFs usling tools like PyPDF2, pdfplumber, or OCR(for scanned PDFs)
    - Clean and structure the data
        - split into chunks
        - remove irrelevant content
    
2. Set up a retrieval system:


## Algorithm/model to consider:
- BM25: ranking function used by search engines to rank matching documents according to their relevance to a given search query. 

- TF-IDF
- Word2Vec
- Doc2Vec
- BERT
- GPT-4
