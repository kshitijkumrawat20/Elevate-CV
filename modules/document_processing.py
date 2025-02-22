import PyPDF2
from typing import Optional

# Load the resume PDF
def load_resume(pdf_path: str) -> Optional[str]:
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        if not text.strip():
            raise ValueError("No text could be extracted from the PDF")
        return text
    except Exception as e:
        raise Exception(f"Error processing PDF file: {str(e)}")
