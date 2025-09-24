


def fix_explanation_length(data: dict, max_len: int = 120) -> dict:
    """
    Auto-fix for SentimentResult.explanation:
    - Truncate if longer than max_len
    - Leave untouched if None or already short
    """
    if data.get("explanation") and isinstance(data["explanation"], str):
        if len(data["explanation"]) > max_len:
            data["explanation"] = data["explanation"][: max_len - 1].rstrip() + "…"
    return data
