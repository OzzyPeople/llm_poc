from src.clients.gemini_client import GeminiClient
from src.prompts.prompt_tasks import *
from src.prompts.system_prompt import *
from src.schemas.summary import RichSummary
from src.schemas.forecast import Forecast
from src.schemas.classifier import SentimentResult
from src.utils.fixes import fix_explanation_length
from src.evaluation.judge import LLMJudge
from pydantic import ValidationError
import json
import os
import json

def ner_with_judge(
    api_key: str,
    ner_text: str,
    defaults_vals: dict,
    entity_whitelist: dict,
    required_fields: list[str] = ["date", "amount", "currency"]
):
    # 1. Produce normalized output
    client = GeminiClient(api_key=api_key, system_prompt=SYSTEM_PROMPT_NORMALIZE)
    prompt = normalize_prompt(ner_text, defaults_vals, entity_whitelist)

    output = client.generate(
        prompt,
        response_schema=None,
        response_mime_type="application/json",
        temperature=0.7, top_p=0.9, max_output_tokens=200,
    )

    # 2. Pretty print and prepare for judge
    try:
        obj = json.loads(output) if isinstance(output, str) else output
        print("=== PRODUCER OUTPUT ===")
        print(json.dumps(obj, ensure_ascii=False, indent=2))
        output_text_for_judge = json.dumps(obj, ensure_ascii=False)
    except Exception:
        print("=== PRODUCER OUTPUT (raw) ===")
        print(output)
        output_text_for_judge = output if isinstance(output, str) else str(output)

    # 3. Run judge
    judge = LLMJudge(api_key=api_key)
    jp = make_judge_prompt(ner_text, output_text_for_judge, required_fields)
    verdict = judge.judge(jp)

    print("\n=== JUDGMENT ===")
    print(json.dumps(verdict, ensure_ascii=False, indent=2))

    # 4. Gatekeeping
    if verdict.get("verdict") == "fail":
        raise SystemExit(f"[BLOCKED] {verdict.get('reasons')}")

    return {"normalized": output_text_for_judge, "judgment": verdict}


def sentiment_with_repair(api_key: str, text: str) -> dict:
    """Run sentiment analysis with auto-repair if schema validation fails."""

    client = GeminiClient(api_key=api_key, system_prompt=RESTRAUNT_EXPERT)
    prompt = sentiment_analysis_prompt(text)
    schema = SentimentResult

    # 1. Generate output
    output = client.generate(
        prompt,
        response_schema=schema,
        temperature=0.7, top_p=0.9, max_output_tokens=200,
    )

    # 2. Try schema validation
    try:
        if output and schema:
            parsed = schema.model_validate_json(output)
            result = parsed.model_dump()
            print("=== SENTIMENT RESULT ===")
            print(result)
            return result

    # 3. Auto-repair on validation error
    except ValidationError as e:
        print("[Validation failed, trying auto-fix]:", e)
        obj = json.loads(output) if isinstance(output, str) else output
        obj = fix_explanation_length(obj)     # truncate explanation if too long
        result = SentimentResult(**obj).model_dump()
        print("=== SENTIMENT RESULT (REPAIRED) ===")
        print(result)
        return result

def forecast_simple(api_key: str, text: str) -> dict | str:
    """Run a simple forecast pipeline. Returns dict if JSON is valid, else raw string."""

    client = GeminiClient(api_key=api_key, system_prompt=PROMPT_ANALYST)
    prompt = forcast_prompt(text)

    output = client.generate(
        prompt,
        response_schema=Forecast,
        response_mime_type="application/json",
        temperature=0.7, top_p=0.9, max_output_tokens=200,
    )
    # Try to parse clean JSON
    try:
        obj = json.loads(output) if isinstance(output, str) else output
        print("=== FORECAST RESULT ===")
        print(json.dumps(obj, ensure_ascii=False, indent=2))
        return obj
    except Exception:
        print("=== FORECAST RESULT (RAW) ===")
        print(output)
        return output