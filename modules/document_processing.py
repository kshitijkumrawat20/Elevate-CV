import PyPDF2
from typing import Optional
import re

def preprocess_text(text: str) -> str:
    """Clean and normalize text by:
    1. Removing extra whitespace and newlines
    2. Removing special characters
    3. Standardizing spacing
    4. Converting to single line where appropriate
    """
    # Remove extra whitespace and newlines
    text = ' '.join(text.split())
    
    # Remove special characters except commas and periods
    text = re.sub(r'[^\w\s,.]', ' ', text)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Standardize periods and commas
    text = re.sub(r'\s*[.,]\s*', '. ', text)
    
    return text.strip()

def load_resume(pdf_path: str) -> Optional[str]:
    """Load and process PDF resume, returning cleaned text"""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
                
        if not text.strip():
            raise ValueError("No text could be extracted from the PDF")
            
        # Clean and preprocess the text
        cleaned_text = preprocess_text(text)
        
        return cleaned_text
        
    except Exception as e:
        raise Exception(f"Error processing PDF file: {str(e)}")
