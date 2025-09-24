from google import genai
from google.genai import types

class GeminiClient:
    def __init__(self, api_key: str, system_prompt: str, model: str = "gemini-2.0-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.system_prompt = system_prompt

    def generate(self, user_prompt: str, response_schema=None, **kwargs):

        """
        Generate text from Gemini model.

        response_schema: dict → structure of expected response
        user_prompt: str → user input prompt
        temperature: float → controls randomness (float, usually 0–1).
        top_p: float → nucleus sampling probability cutoff
        candidate_count: int → number of responses to return
        stop_sequences: list[str] → sequences to stop generation
        max_output_tokens: int → length limit for response
        safety_settings: dict → content moderation rules
        tools: list → structured tool/function calling

        example,
        temperature=0.0,              # no randomness
        max_output_tokens=500         # cap length

        """
        cfg = types.GenerateContentConfig(
            # put the system prompt here (NOT as a system message)
            system_instruction=self.system_prompt,

            # decoding knobs
            temperature=kwargs.get("temperature", 0.7),
            top_p=kwargs.get("top_p", 0.9),
            max_output_tokens=kwargs.get("max_output_tokens", 200),

            # JSON mode (optional)
            response_mime_type="application/json" if response_schema else None,
            response_schema=response_schema,
        )

        try:
            resp = self.client.models.generate_content(
                model=self.model,
                contents=[
                    {"role": "user", "parts": [{"text": user_prompt}]},
                ],
                config=cfg,
            )
            return getattr(resp, "text", str(resp))
        except Exception as e:
            print(f"[GeminiClient] Generation failed: {e}")
            return None
