from typing import Dict
from google import genai
from google.genai import types
import json

class LLMJudge:
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def judge(self, prompt: str) -> dict:
        cfg = types.GenerateContentConfig(
            temperature=0.0, top_p=1, max_output_tokens=200, #don’t truncate the probability mass, full distribution for best accuracy
            response_mime_type="application/json"
        )
        resp = self.client.models.generate_content(
            model=self.model,
            contents=[{"role": "user", "parts": [{"text": prompt}]}],
            config=cfg
        )
        text = resp.text or ""
        # Handle cases where model wraps JSON in ```json ... ```
        text = text.strip()
        if text.startswith("```"):
            text = text.strip("`")
            if text.startswith("json"):
                text = text[4:].lstrip()
        return json.loads(text)