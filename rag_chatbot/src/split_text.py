import re
import nltk
from nltk.tokenize import sent_tokenize
from pathlib import Path

def split_into_chunks(text, chunk_size=300):
    """Splits text into meaningful chunks based on headings and sentence boundaries."""
    
    # Step 1: Split by headings if present
    sections = re.split(r'(?m)^\s*(?:[A-Z][A-Za-z\s\d]+):\s*$', text)
    
    chunks = []
    for section in sections:
        sentences = sent_tokenize(section)
        
        chunk = []
        word_count = 0
        
        for sentence in sentences:
            words = sentence.split()
            word_count += len(words)
            chunk.append(sentence)
            
            # If chunk exceeds desired size, save and reset
            if word_count >= chunk_size:
                chunks.append(" ".join(chunk))
                chunk = []
                word_count = 0
        
        # Add remaining text in section
        if chunk:
            chunks.append(" ".join(chunk))
    
    return chunks

def process_and_save_chunks(input_path, output_dir="processed_data", chunk_size=300):
    """Reads cleaned text, splits it into chunks, and saves them."""
    
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    text = input_path.read_text(encoding="utf-8")
    chunks = split_into_chunks(text, chunk_size)

    output_file = output_dir / f"chunks_{input_path.stem}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            f.write(f"\n[Chunk {i+1}]\n{chunk}\n")
    
    print(f"✅ Chunked text saved to {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python src/split_text.py path/to/cleaned_text.txt")
    else:
        process_and_save_chunks(sys.argv[1])