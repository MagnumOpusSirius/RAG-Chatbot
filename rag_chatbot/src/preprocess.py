import re
from pathlib import Path

def clean_text(text):
    """Cleans extracted text by removing noise and fixing formatting issues."""
    # Remove unnecessary spaces and special characters
    text = re.sub(r'\s+', ' ', text)  # Normalize multiple spaces
    text = re.sub(r'[\x00-\x1F\x7F]', ' ', text)  # Remove non-printable chars
    
    # Fix words stuck together (basic heuristic approach)
    text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)  # Add space between camel-case words
    text = re.sub(r'(?<=[a-zA-Z])(?=\d)', ' ', text)  # Add space between words & numbers
    text = re.sub(r'(?<=\d)(?=[a-zA-Z])', ' ', text)  # Add space between numbers & words
    
    return text.strip()

def preprocess_file(input_path, output_dir="processed_data"):
    """Reads a text file, cleans it, and saves the cleaned version."""
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    raw_text = input_path.read_text(encoding="utf-8")
    cleaned_text = clean_text(raw_text)

    output_file = output_dir / f"cleaned_{input_path.name}"
    output_file.write_text(cleaned_text, encoding="utf-8")
    print(f"✅ Cleaned text saved to {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python src/preprocess.py path/to/extracted_text.txt")
    else:
        preprocess_file(sys.argv[1])