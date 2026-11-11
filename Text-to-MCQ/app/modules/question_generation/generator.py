import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re

class QuestionGenerator:
    def __init__(self, model_path="./models/vit5_qg"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"[*] Đang tải mô hình ViT5 từ: {model_path}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path).to(self.device)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def generate_questions(self, context: str, answer: str, num_questions: int = 5) -> list:
        input_text = f"answer: {answer} context: {context}"
        inputs = self.tokenizer(input_text, max_length=512, truncation=True, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs.input_ids,
                max_length=64,
                num_beams=5,
                num_return_sequences=num_questions,
                no_repeat_ngram_size=3,
                min_length=6,
                early_stopping=True
            )
        
        questions = []
        for output in outputs:
            q = self.tokenizer.decode(output, skip_special_tokens=True).strip()
            q = self._post_process(q)
            if q:
                questions.append(q)
        return questions

    def _post_process(self, question: str) -> str:
        if not question:
            return ""
        
        # Viết hoa chữ đầu
        if question[0].islower():
            question = question[0].upper() + question[1:]
        
        # Đảm bảo kết thúc bằng ?
        if not question.endswith('?'):
            question = question.rstrip('.') + '?'
        
        # Loại bỏ từ thừa ở đầu
        bad_starts = ["và ", "hoặc ", "nhưng ", "vì ", "do "]
        for bs in bad_starts:
            if question.lower().startswith(bs):
                question = question[len(bs):]
        
        # Kiểm tra có từ để hỏi
        wh_words = ["ai", "gì", "nào", "đâu", "sao", "bao nhiêu", "khi nào", "thế nào", "vì sao", "tại sao", "ra sao"]
        if not any(re.search(r'\b' + re.escape(w) + r'\b', question.lower()) for w in wh_words) and "___" not in question:
            return ""
        
        # Loại câu hỏi quá ngắn (< 5 từ)
        if len(question.split()) < 5:
            return ""
        
        return question.strip()