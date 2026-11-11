from app.modules.preprocessing.nlp_utils import split_sentences

def create_chunks(text: str, max_tokens: int = 200, overlap_sentences: int = 1) -> list:
    """
    Chia văn bản thành các chunk dựa trên số câu và giới hạn token ước lượng.
    (Ở bước này ta ước lượng 1 token ~ 1 từ để đơn giản, sang bước train ViT5 sẽ dùng tokenizer chuẩn sau).
    """
    sentences = split_sentences(text)
    chunks = []
    
    current_chunk = []
    current_length = 0
    chunk_id = 1

    for sentence in sentences:
        # Đếm số từ trong câu (ước lượng token)
        sentence_length = len(sentence.split())
        
        # Nếu câu hiện tại làm vượt quá max_tokens và trong chunk đã có câu
        if current_length + sentence_length > max_tokens and current_chunk:
            # Lưu chunk hiện tại
            chunks.append({
                "chunk_id": f"chunk_{chunk_id:03d}",
                "text": " ".join(current_chunk),
                "token_count": current_length
            })
            chunk_id += 1
            
            # Xử lý overlap: Giữ lại N câu cuối của chunk trước cho chunk sau
            if overlap_sentences > 0 and len(current_chunk) >= overlap_sentences:
                overlap_part = current_chunk[-overlap_sentences:]
                current_chunk = overlap_part.copy()
                current_length = sum(len(s.split()) for s in current_chunk)
            else:
                current_chunk = []
                current_length = 0

        # Thêm câu hiện tại vào chunk
        current_chunk.append(sentence)
        current_length += sentence_length

    # Lưu chunk cuối cùng nếu còn sót
    if current_chunk:
        chunks.append({
            "chunk_id": f"chunk_{chunk_id:03d}",
            "text": " ".join(current_chunk),
            "token_count": current_length
        })

    return chunks