import random
import torch
from transformers import pipeline
from sentence_transformers import util
from app.modules.distractor_generation.distractor_fallback import fallback_distractors

print("Đang tải mô hình Embedding cho Distractor...")
from sentence_transformers import SentenceTransformer
embedder = SentenceTransformer('keepitreal/vietnamese-sbert')

print("Đang tải mô hình PhoBERT Fill-Mask...")
# Khởi tạo PhoBERT Fill-Mask
try:
    fill_mask = pipeline("fill-mask", model="vinai/phobert-base-v2", top_k=20)
except Exception as e:
    print(f"Lỗi khởi tạo PhoBERT: {e}")
    fill_mask = None

def generate_distractors_mlm(sentence: str, target_answer: str, num_distractors: int = 3) -> list:
    """Sinh đáp án nhiễu bằng PhoBERT Masked LM."""
    if fill_mask is None:
        return []
        
    masked_sentence = sentence.replace(target_answer, "<mask>", 1)
    if "<mask>" not in masked_sentence:
        return []
        
    try:
        predictions = fill_mask(masked_sentence)
    except Exception:
        return []

    ans_emb = embedder.encode(target_answer, convert_to_tensor=True)
    distractors = []
    dist_embs = []
    
    for p in predictions:
        token = p['token_str'].strip()
        if token.lower() == target_answer.lower() or len(token) < 2:
            continue
            
        # Tính độ tương đồng với đáp án đúng
        tok_emb = embedder.encode(token, convert_to_tensor=True)
        score = util.cos_sim(ans_emb, tok_emb).item()
        
        # Lọc theo ngưỡng (0.40 - 0.85)
        if 0.40 <= score <= 0.85:
            # Chống trùng lặp distractor
            if dist_embs:
                sim_to_dist = util.cos_sim(tok_emb, torch.stack(dist_embs))[0]
                if torch.max(sim_to_dist).item() > 0.90:
                    continue
                    
            distractors.append(token)
            dist_embs.append(tok_emb)
            
        if len(distractors) == num_distractors:
            break
            
    return distractors

def generate_distractors_for_answer(answer_text: str, answer_type: str, context: str, all_doc_candidates: list) -> list:
    """Sinh đáp án nhiễu với cơ chế Fallback nhiều tầng."""
    
    # 1. Ưu tiên PhoBERT MLM (Nếu là dạng cần sinh từ vựng)
    if answer_type in ('TERM', 'BIO', 'MISC'):
        mlm_distractors = generate_distractors_mlm(context, answer_text, num_distractors=3)
        if len(mlm_distractors) == 3:
            return mlm_distractors

    # 2. Tìm trong văn bản (cùng loại)
    same_type = [
        c['text'] for c in all_doc_candidates
        if c['type'] == answer_type and c['text'].lower() != answer_text.lower()
    ]
    valid_pool = list(dict.fromkeys(same_type))
    
    if len(valid_pool) >= 3:
        random.shuffle(valid_pool)
        return valid_pool[:3]

    # 3. Fallback Gazetteer cùng loại
    fallbacks = fallback_distractors(answer_text, answer_type)
    for fb in fallbacks:
        if fb.lower() != answer_text.lower() and fb not in valid_pool:
            valid_pool.append(fb)
        if len(valid_pool) >= 3:
            break
            
    if len(valid_pool) < 3:
        return []
        
    random.shuffle(valid_pool)
    return valid_pool[:3]