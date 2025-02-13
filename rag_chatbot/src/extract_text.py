import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from pathlib import Path

def extract_text_from_pdf(pdf_path, output_dir="processed_data"):
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    text_output = []
    
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        
        # If no text is found, use OCR on images
        if not text.strip():
            images = convert_from_path(pdf_path, first_page=page_num+1, last_page=page_num+1)
            for image in images:
                text += pytesseract.image_to_string(image)

        text_output.append(f"\n[Page {page_num+1}]\n{text}")

    output_file = output_dir / f"{pdf_path.stem}.txt"
    output_file.write_text("\n".join(text_output), encoding="utf-8")
    print(f"✅ Extracted text saved to {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python src/extract_text.py path/to/pdf")
    else:
        extract_text_from_pdf(sys.argv[1])