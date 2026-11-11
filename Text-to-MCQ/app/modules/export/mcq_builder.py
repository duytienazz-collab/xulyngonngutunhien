import random

def build_mcq(question: str, correct_answer: str, distractors: list) -> dict:
    if not question or not question.strip():
        return None
    if not correct_answer or not correct_answer.strip():
        return None
    if not isinstance(distractors, list) or len(distractors) != 3:
        return None

    options = [correct_answer.strip()]
    seen = {correct_answer.strip().casefold()}
    
    for d in distractors:
        if not isinstance(d, str) or not d.strip():
            continue
        d = d.strip()
        key = d.casefold()
        if key not in seen:
            seen.add(key)
            options.append(d)

    if len(options) != 4:
        return None
        
    random.shuffle(options)
    labels = ['A', 'B', 'C', 'D']
    options_dict = dict(zip(labels, options))
    
    correct_label = next(
        label for label, value in options_dict.items()
        if value == correct_answer.strip()
    )
    
    return {
        "question": question.strip(),
        "options": options_dict,
        "correct_answer": correct_label,
        "correct_answer_text": correct_answer.strip()
    }