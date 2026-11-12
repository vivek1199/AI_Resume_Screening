
from pathlib import Path

import fitz
from docx import Document


def extract_text_from_pdf(file_path):
    """Extract text from a PDF resume."""
    text_parts = []

    with fitz.open(file_path) as document:
        for page in document:
            text_parts.append(page.get_text("text"))

    return "\n".join(text_parts).strip()


def extract_text_from_docx(file_path):
    """Extract paragraphs and table text from a DOCX resume."""
    document = Document(file_path)
    parts = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            parts.append(paragraph.text.strip())

    for table in document.tables:
        for row in table.rows:
            parts.append(" | ".join(cell.text.strip() for cell in row.cells))

    return "\n".join(parts).strip()


def extract_text_from_resume(file_path):
    """Automatically identify and extract a supported resume."""
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif extension == ".docx":
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Only PDF and DOCX resumes are supported.")

    if not text.strip():
        raise ValueError(
            "No readable text found. Please upload a text-based resume."
        )

    return text
