import re
from collections import Counter
from app.modules.document_processing.reader import extract_text_from_document
from app.modules.preprocessing.nlp_utils import clean_text
from app.modules.chunking.chunker import create_chunks
from app.modules.answer_extraction.extractor import extract_candidates
from app.modules.question_generation.generator import QuestionGenerator
from app.modules.distractor_generation.generator import generate_distractors_for_answer, embedder
from app.modules.export.mcq_builder import build_mcq
from app.modules.ranking.keyphrase_ranker import rank_candidates_by_salience
from underthesea import ner

class MCQService:
    def __init__(self):
        self.generator = QuestionGenerator(model_path="./models/vit5_qg")

    def is_question_hallucinated(self, generated_question: str, source_context: str) -> bool:
        q_entities = ner(generated_question)
        context_lower = source_context.lower()
        for ent in q_entities:
            word, pos, chunk, tag = ent
            if tag.startswith(("B-PER", "B-LOC", "B-ORG")):
                clean_word = word.replace("_", " ").lower()
                if clean_word not in context_lower:
                    print(f"   [HALLUCINATION] Bịa thực thể '{word}' không có trong bài.")
                    return True
        return False

    def is_valid_mcq(self, question: str, answer: str, context: str, distractors: list) -> bool:
        q_lower = question.lower()
        a_lower = answer.lower()
        if a_lower in q_lower:
            return False
        if self.is_question_hallucinated(question, context):
            return False
        if len(distractors) < 3:
            return False
        if any(d.lower() == a_lower for d in distractors):
            return False
        return True

    def process_document(self, file_path: str, max_questions: int = 12):
        # BỌC THÉP: Nếu max_questions bị None thì gán mặc định là 12
        if max_questions is None:
            max_questions = 12
            
        raw_text = extract_text_from_document(file_path)
        text_cleaned = clean_text(raw_text)
        if not text_cleaned:
            return []

        chunks = create_chunks(text_cleaned, max_tokens=150, overlap_sentences=1)
        if not chunks:
            return []

        global_candidates = []
        for ch in chunks:
            global_candidates.extend(extract_candidates(ch['text']))

        print("[INFO] Đang xếp hạng ứng viên theo độ quan trọng...")
        top_candidates = rank_candidates_by_salience(
            global_candidates, text_cleaned, embedder, top_k=20
        )

        print(f"[INFO] Chunks: {len(chunks)}, Tổng ứng viên: {len(global_candidates)}, Giữ lại Top: {len(top_candidates)}")
        print(f"[INFO] Phân bố loại: {dict(Counter(c['type'] for c in top_candidates))}")

        final_mcqs = []
        used_answers = set()
        
        for chunk in chunks:
            if len(final_mcqs) >= max_questions:
                break
                
            chunk_text = chunk['text']
            chunk_cands = [c for c in top_candidates if c['text'] in chunk_text]
            selected_cands = [c for c in chunk_cands if c['text'].casefold() not in used_answers][:3]
            
            for cand in selected_cands:
                if len(final_mcqs) >= max_questions:
                    break
                    
                answer = cand['text']
                answer_type = cand['type']
                
                questions = self.generator.generate_questions(chunk_text, answer, num_questions=3)
                
                for question in questions:
                    if len(final_mcqs) >= max_questions:
                        break

                    distractors = generate_distractors_for_answer(answer, answer_type, chunk_text, top_candidates)
                    
                    if not self.is_valid_mcq(question, answer, chunk_text, distractors):
                        continue
                        
                    mcq = build_mcq(question, answer, distractors)
                    if mcq is None:
                        continue

                    mcq['source_context'] = chunk_text
                    final_mcqs.append(mcq)
                    used_answers.add(answer.casefold())
                    
                    print(f"   [SUCCESS] Câu {len(final_mcqs)}: {question}")
                    break

        print("\n" + "="*55)
        print(f"KẾT QUẢ: Tạo được {len(final_mcqs)}/{max_questions} câu hỏi chuẩn.")
        print("="*55)
        return final_mcqs