from underthesea import ner, pos_tag
import re

# Các tag không được phép ở CUỐI cụm danh từ
# V: Động từ, E: Giới từ, C: Liên từ, R: Phó từ, P: Đại từ, T: Trợ từ, X: Khác
INVALID_TAIL_TAGS = {"V", "E", "C", "R", "P", "T", "X"}
# Các tag không được phép ở ĐẦU cụm danh từ
INVALID_HEAD_TAGS = {"E", "C", "CC"}

# Regex dự phòng cho TIME và NUM
TIME_RE = re.compile(r'(?i)\b(?:ngày\s+\d{1,2}\s+)?(?:tháng\s+\d{1,2}\s+)?năm\s+\d{4}|\bthế kỷ\s+\d{1,2}\b')
NUM_RE = re.compile(r'(?i)\b\d+(?:[\.,]\d+)?\s*(?:ha|mw|mwp|km|m|mm|kg|tấn|%|độ C|triệu|tỷ|ngàn|nghìn|loài|cá thể)\b')

def is_syntactically_valid_candidate(phrase: str) -> bool:
    """Kiểm tra tính hoàn chỉnh về mặt cú pháp của ứng viên dựa trên POS tags."""
    if not phrase or len(phrase.split()) > 5:
        return False
        
    words_and_tags = pos_tag(phrase)
    if not words_and_tags:
        return False
        
    tags = [tag for _, tag in words_and_tags]
    first_tag = tags[0]
    last_tag = tags[-1]
    
    # Quy tắc 1: Từ kết thúc không được là Động từ/Giới từ/Liên từ...
    if last_tag in INVALID_TAIL_TAGS:
        return False
        
    # Quy tắc 2: Từ đầu không được là Giới từ/Liên từ
    if first_tag in INVALID_HEAD_TAGS:
        return False
        
    # Quy tắc 3: Phải chứa ít nhất một hạt nhân danh từ (N, Np, Nc, Nu)
    if not any(t in {"N", "Np", "Nc", "Nu"} for t in tags):
        return False
        
    return True

def extract_candidates(text: str) -> list:
    if not text:
        return []
        
    raw_candidates = []
    
    # 0. Quét Regex bắt buộc cho TIME và NUM
    for m in TIME_RE.finditer(text):
        raw_candidates.append({'text': m.group(0).strip(), 'ner_type': 'TIME'})
    for m in NUM_RE.finditer(text):
        raw_candidates.append({'text': m.group(0).strip(), 'ner_type': 'NUM'})
        
    # 1. Quét NER
    entities = ner(text)
    i = 0
    while i < len(entities):
        word, pos, chunk, label = entities[i]
        if label.startswith('B-'):
            current_ent = word
            current_label = label.replace('B-', '')
            j = i + 1
            while j < len(entities):
                next_word, next_pos, next_chunk, next_label = entities[j]
                if next_label == f'I-{current_label}':
                    current_ent += " " + next_word
                    j += 1
                elif next_word == '-' and j + 1 < len(entities):
                    lookahead_label = entities[j+1][3]
                    lookahead_word = entities[j+1][0]
                    if lookahead_label in (f'B-{current_label}', f'I-{current_label}'):
                        current_ent += " - " + lookahead_word
                        j += 2
                        continue
                    break
                else:
                    break
            raw_candidates.append({'text': current_ent.strip(), 'ner_type': current_label})
            i = j
        else:
            i += 1

    # 2. Quét Noun Phrases thô
    words_with_pos = pos_tag(text)
    current_phrase = []
    for word, pos in words_with_pos:
        if pos in ['N', 'Np', 'Nu', 'Nc', 'A', 'M', 'L']:
            current_phrase.append(word)
        else:
            if current_phrase:
                phrase = " ".join(current_phrase).strip()
                if 1 < len(current_phrase) <= 5:
                    raw_candidates.append({'text': phrase, 'ner_type': 'PHRASE'})
                current_phrase = []
    if current_phrase:
        phrase = " ".join(current_phrase).strip()
        if 1 < len(current_phrase) <= 5:
            raw_candidates.append({'text': phrase, 'ner_type': 'PHRASE'})

    # 3. Lọc bằng Cú pháp học
    valid_candidates = []
    for c in raw_candidates:
        cleaned_text = c['text'].strip(" .,;:\"'?!-–—()[]")
        if not cleaned_text:
            continue
            
        # Kiểm tra cú pháp bằng POS Grammar
        if not is_syntactically_valid_candidate(cleaned_text):
            continue
            
        # Nếu là TIME/NUM thì bỏ qua kiểm tra NP chặt chẽ
        valid_candidates.append({
            'text': cleaned_text,
            'type': c['ner_type']
        })
        
    # 4. Loại trùng
    unique_dict = {}
    for c in valid_candidates:
        unique_dict.setdefault(c['text'].casefold(), c)
        
    return list(unique_dict.values())