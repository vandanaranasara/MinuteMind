from PyPDF2 import PdfReader
import os

def extract_text_from_file(filepath: str) -> str:
    if filepath.lower().endswith(".txt"):
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    elif filepath.lower().endswith(".pdf"):
        text_parts = []
        try:
            reader = PdfReader(filepath)
            for page in reader.pages:
                text_parts.append(page.extract_text() or "")
            return "\n".join(text_parts)
        except Exception as e:
            raise e
    else:
        raise ValueError("Unsupported file type")
