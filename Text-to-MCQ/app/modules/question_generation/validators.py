"""Bộ lọc luật (rule-based) cho câu hỏi đã sinh."""
import re
from typing import Tuple

# Từ để hỏi tương ứng với từng loại đáp án
WH_RULES = {
    "PER": r"(?<!\w)(ai|người nào|nhân vật nào|vị nào)(?!\w)",
    "LOC": r"(ở đâu|đâu|nơi nào|địa phương nào|vùng nào|tỉnh nào|địa điểm nào|huyện nào)",
    "ORG": r"(tổ chức nào|cơ quan nào|đơn vị nào|(?<!\w)ai(?!\w))",
    "DATE": r"(năm nào|khi nào|bao giờ|tháng nào|thời gian nào|năm bao nhiêu)",
}

# Câu hỏi về nguyên nhân/cách thức không hợp với đáp án là thực thể
BAD_FOR_ENTITY = re.compile(
    r"(nguyên nhân|vì sao|tại sao|lý do|như thế nào|bằng cách nào)", re.IGNORECASE
)


def _has_repeated_trigram(words: list) -> bool:
    seen = set()
    for i in range(len(words) - 2):
        tri = tuple(words[i:i + 3])
        if tri in seen:
            return True
        seen.add(tri)
    return False


def validate_question(question: str, answer: str, answer_type: str) -> Tuple[bool, str]:
    """Trả về (hợp lệ?, lý do nếu loại)."""
    q = question.strip()
    if not q:
        return False, "câu hỏi rỗng"

    if "?" not in q and "___" not in q:
        return False, "không phải câu hỏi"

    words = q.lower().split()
    if not (5 <= len(words) <= 30):
        return False, "độ dài bất thường"

    if _has_repeated_trigram(words):
        return False, "lặp từ"

    # Lộ đáp án: toàn bộ từ của đáp án đã xuất hiện trong câu hỏi
    ans_tokens = answer.lower().split()
    if ans_tokens and all(t in words for t in ans_tokens):
        return False, "câu hỏi chứa đáp án"
    if answer.lower() in q.lower():
        return False, "câu hỏi chứa đáp án"

    if answer_type in WH_RULES:
        if BAD_FOR_ENTITY.search(q):
            return False, f"lệch pha (hỏi nguyên nhân/cách thức - đáp án {answer_type})"
        if not re.search(WH_RULES[answer_type], q, re.IGNORECASE):
            return False, f"lệch pha (thiếu từ để hỏi cho loại {answer_type})"

    return True, ""