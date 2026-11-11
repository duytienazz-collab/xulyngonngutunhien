import fitz  # Thư viện PyMuPDF
import docx
from pathlib import Path

def read_pdf(file_path: str) -> str:
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text() + "\n"
    except Exception as e:
        print(f"Lỗi đọc PDF: {e}")
    return text

def read_docx(file_path: str) -> str:
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Lỗi đọc DOCX: {e}")
    return text

def read_txt(file_path: str) -> str:
    text = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Lỗi đọc TXT: {e}")
    return text

def extract_text_from_document(file_path: str) -> str:
    """Hàm tổng hợp: Tự nhận diện đuôi file và trích xuất text"""
    ext = Path(file_path).suffix.lower()
    if ext == '.pdf':
        return read_pdf(file_path)
    elif ext == '.docx':
        return read_docx(file_path)
    elif ext == '.txt':
        return read_txt(file_path)
    else:
        raise ValueError(f"Không hỗ trợ định dạng file: {ext}")