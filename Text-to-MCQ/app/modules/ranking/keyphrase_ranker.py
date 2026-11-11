import torch
from sentence_transformers import util

def rank_candidates_by_salience(candidates: list, doc_text: str, embedder, top_k: int = 18) -> list:
    """Xếp hạng ứng viên dựa trên độ tương đồng ngữ nghĩa với toàn bộ văn bản."""
    if not candidates:
        return []
        
    # Tách riêng TIME, NUM để không bị loại oan (vì chúng ít gắn với ngữ nghĩa toàn bài)
    special_candidates = [c for c in candidates if c['type'] in ('TIME', 'NUM')]
    text_candidates = [c for c in candidates if c['type'] not in ('TIME', 'NUM')]
    
    ranked_text = []
    if text_candidates:
        doc_embedding = embedder.encode(doc_text, convert_to_tensor=True)
        texts = [c['text'] for c in text_candidates]
        candidate_embeddings = embedder.encode(texts, convert_to_tensor=True)
        
        # Tính Cosine Similarity giữa từng ứng viên và toàn bộ bài đọc
        scores = util.cos_sim(candidate_embeddings, doc_embedding).squeeze(1)
        
        # Ghép điểm và sắp xếp giảm dần
        scored = list(zip(text_candidates, scores.tolist()))
        scored.sort(key=lambda x: x[1], reverse=True)
        ranked_text = [c for c, score in scored[:top_k]]
        
    # Gộp lại và giới hạn số lượng
    final_candidates = special_candidates + ranked_text
    return final_candidates[:top_k + len(special_candidates)]