import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import PyPDF2

# Step 1: Extract normal text from PDF
def extract_text_from_pdf(pdf_path):
    """
    Extract normal text from a PDF using PyPDF2.
    :param pdf_path: Path to the input PDF file.
    :return: Extracted text.
    """
    extracted_text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            extracted_text += page.extract_text() + "\n"

    print("Normal text extraction complete.")
    return extracted_text


# Step 2: Extract images from PDF and apply OCR
def extract_images_and_ocr(pdf_path, output_folder):
    """
    Extract images from PDF and apply OCR to extract text.
    :param pdf_path: Path to the input PDF file.
    :param output_folder: Folder to save extracted images.
    :return: Extracted text from images.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert PDF to images
    images = convert_from_path(pdf_path)
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i + 1}.png")
        image.save(image_path, "PNG")
        image_paths.append(image_path)

    print(f"Extracted {len(image_paths)} images from PDF.")

    # Apply OCR to images
    extracted_text = ""
    for image_path in image_paths:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        extracted_text += text + "\n"

    print("OCR text extraction complete.")
    return extracted_text


# Step 3: Clean and save the combined text
def clean_and_save_text(text, output_file):
    """
    Clean the extracted text and save it to a file.
    :param text: Extracted text.
    :param output_file: Path to the output text file.
    """
    cleaned_text = " ".join(text.split())
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    print(f"Cleaned text saved to {output_file}.")


# Main function to process PDF with mixed content
def process_mixed_pdf(pdf_path, output_folder, output_text_file):
    """
    Process a PDF with both normal text and images.
    :param pdf_path: Path to the input PDF file.
    :param output_folder: Folder to save extracted images.
    :param output_text_file: Path to save the combined and cleaned text.
    """
    # Step 1: Extract normal text from PDF
    normal_text = extract_text_from_pdf(pdf_path)

    # Step 2: Extract text from images using OCR
    ocr_text = extract_images_and_ocr(pdf_path, output_folder)

    # Step 3: Combine normal text and OCR text
    combined_text = normal_text + "\n" + ocr_text

    # Step 4: Clean and save the combined text
    clean_and_save_text(combined_text, output_text_file)


# Run the mixed PDF processing pipeline
if __name__ == "__main__":
    # Input PDF file
    pdf_path = "multithreading.pdf"  # Replace with your PDF file path

    # Output folder for extracted images
    output_folder = "extracted_images"

    # Output text file for cleaned text
    output_text_file = "extracted_text.txt"

    # Run the mixed PDF processing pipeline
    process_mixed_pdf(pdf_path, output_folder, output_text_file)