from typing import Optional, Dict
import json


def summarize_prompt(text: str) -> str:
    return f"Summarize this text in 3 bullet points:\n\n{text}"

def forcast_prompt(text: str) -> str:
    return f"Make forecast of the value for :\n\n{text} the next 3 months. Describe the trend with 3 bulelts why it will go up or down"

### Classification prompt

def sentiment_analysis_prompt(review: str) -> str:
    PROMPT_BASE = """
    Task: Label the restaurant review as POSITIVE, NEUTRAL, or NEGATIVE.
    Always output only valid JSON in this format:
    {"label": "<POSITIVE|NEUTRAL|NEGATIVE>", "confidence": <0..1>, "explanation": "<short reason, <=30 words>"}

    Rules:
    - If sentiment is mixed or unclear → NEUTRAL.
    - Mention the main evidence words in the explanation.
    - Confidence must be between 0 and 1, not exactly 0 or 1.
    - Explanations must be <= 120 characters. Be concise.
    - Never add extra commentary or formatting.

    Examples:
    Input: "Service was slow and the soup was cold."
    Output: {"label": "NEGATIVE", "confidence": 0.82, "explanation": "Slow service and cold soup are strong negatives."}

    Input: "Service was slow, but the staff fixed it quickly and the meal was great."
    Output: {"label": "POSITIVE", "confidence": 0.74, "explanation": "Despite slow start, good staff recovery and tasty meal."}

    Input: "It is difficult to say if it was good or bad."
    Output: {"label": "NEUTRAL", "confidence": 0.55, "explanation": "Ambiguous statement without clear positive or negative."}

    Input: "Portions generous; flavor was bland."
    Output: {"label": "NEGATIVE", "confidence": 0.67, "explanation": "Generous portions, but bland flavor dominates impression."}
    """
    ADD = f"""Input: "{review}" """
    return PROMPT_BASE + " " + ADD

### NER

def normalize_prompt(input_text: str, defaults: dict | None = None, entity_whitelist: list[str] | None = None) -> str:
    """
    defaults example:
      {
        "default_country": "US",
        "default_currency": "USD",
        "default_phone_country": "US",
        "locale": "en-US"
      }
    entity_whitelist example:
      ["date","amount","phone","email","url","iban","vat","zipcode","currency","country","name","address"]
    """
    return f"""
Extract and normalize entities from the text below.

Input:
{input_text}

Defaults (JSON, may be null):
{defaults or {}}

If provided, only normalize these entity types (whitelist); otherwise detect freely:
{entity_whitelist or []}

Return JSON with keys: entities (array), unparsed (array of leftover snippets).
"""

### judge

def make_judge_prompt(source_text: str, model_output_text: str, required):
    return f"""
Evaluate the normalized output.

SOURCE:
{source_text}

OUTPUT (may be JSON or text containing JSON):
{model_output_text}

Required fields: {required}

Checks (answer as JSON only):
- Score 1..10
- Verdict: "pass" if score>=9, "needs_revision" if 7-8, else "fail"
- Reasons: short bullets

Consider only:
1) JSON validity (parsable single JSON object)
2) Required fields present & non-empty
3) Values faithful to SOURCE (no invented facts)

Return JSON:
{{"score": <int>, "verdict": "<pass|needs_revision|fail>", "reasons": ["..."]}}
""".strip()