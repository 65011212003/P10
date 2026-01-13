"""Module for reading content from various file types."""

import os
from pathlib import Path

from config import SUPPORTED_EXTENSIONS


def read_text_file(file_path: str) -> str:
    """Read content from a plain text file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def read_pdf_file(file_path: str) -> str:
    """Read content from a PDF file."""
    try:
        import pypdf
        reader = pypdf.PdfReader(file_path)
        text_content = []
        for page in reader.pages:
            text_content.append(page.extract_text())
        return '\n'.join(text_content)
    except ImportError:
        raise ImportError("pypdf is required to read PDF files. Install with: pip install pypdf")


def read_docx_file(file_path: str) -> str:
    """Read content from a Word document."""
    try:
        from docx import Document
        doc = Document(file_path)
        paragraphs = [para.text for para in doc.paragraphs]
        return '\n'.join(paragraphs)
    except ImportError:
        raise ImportError("python-docx is required to read DOCX files. Install with: pip install python-docx")


def read_csv_file(file_path: str) -> str:
    """Read content from a CSV file."""
    import csv
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = [', '.join(row) for row in reader]
        return '\n'.join(rows)


def read_json_file(file_path: str) -> str:
    """Read content from a JSON file."""
    import json
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return json.dumps(data, indent=2)


def read_file(file_path: str) -> str:
    """
    Read content from a file based on its extension.
    
    Args:
        file_path: Path to the file to read.
        
    Returns:
        The content of the file as a string.
        
    Raises:
        ValueError: If the file type is not supported.
        FileNotFoundError: If the file does not exist.
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    extension = path.suffix.lower()
    
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {extension}. Supported types: {list(SUPPORTED_EXTENSIONS.keys())}")
    
    file_type = SUPPORTED_EXTENSIONS[extension]
    
    if file_type == 'pdf':
        return read_pdf_file(file_path)
    elif file_type == 'docx':
        return read_docx_file(file_path)
    elif file_type == 'csv':
        return read_csv_file(file_path)
    elif file_type == 'json':
        return read_json_file(file_path)
    else:
        # For text, markdown, python, xml, html - read as plain text
        return read_text_file(file_path)
