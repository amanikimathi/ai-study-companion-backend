from pypdf import PdfReader
import os
print("Current folder:", os.getcwd())
print("Files here:", os.listdir())

def extract_text_from_pdf(file_path: str) -> str:
    """Opens a PDF and pulls out all readable text as one big string."""
    reader = PdfReader(file_path)
    
    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        full_text += page_text + "\n"
    
    return full_text

if __name__ == "__main__":
    # Replace this with your actual PDF's filename
    text = extract_text_from_pdf("my_lecture.pdf")
    print(text)
    print(f"\n--- Total characters extracted: {len(text)} ---")