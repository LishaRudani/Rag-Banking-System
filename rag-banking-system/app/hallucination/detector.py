def detect_hallucination(answer, context, threshold=0.6):
    # simple check: answer words in context
    match_count = sum(1 for word in answer.split() if word in context)
    score = match_count / len(answer.split())

    if score < threshold:
        return True  # hallucination
    return False



