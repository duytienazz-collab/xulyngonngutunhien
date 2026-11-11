import re
import unicodedata
from underthesea import sent_tokenize

def clean_text(text: str) -> str:
    if not text:
        return ""
    # 1. Chuẩn hóa Unicode
    text = unicodedata.normalize('NFC', text)
    
    # 2. XÓA TIÊU ĐỀ VÀ SỐ THỨ TỰ (Văn bản 1, Chương 2, Phần 3...)
    text = re.sub(r'(?i)\b(Văn bản|Chương|Phần|Mục|Đoạn)\s*\d+[\:\-\.]?\s*', '', text)
    # Xóa các dòng tiêu đề in hoa hoàn toàn (thường là tiêu đề bài báo)
    text = re.sub(r'^[A-ZÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬĐÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ\s\-,\.]+$', '', text, flags=re.MULTILINE)

    # 3. Xóa ký tự rác
    text = re.sub(r'[^\w\s\.\,\?\!\:\;\-\(\)]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def split_sentences(text: str) -> list:
    if not text:
        return []
    return sent_tokenize(text)