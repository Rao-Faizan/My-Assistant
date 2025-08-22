# engine/services/gpt_service.py
import os
from engine.utils.config import OPENAI_API_KEY, OPENAI_MODEL
from engine.utils.logger import logger

try:
    import openai
    openai.api_key = OPENAI_API_KEY
    openai_available = True
except Exception:
    openai_available = False
    logger = logger if 'logger' in globals() else None

class GPTService:
    def __init__(self, model: str = None):
        self.model = model or OPENAI_MODEL

    def get_response(self, prompt: str):
        if not openai_available:
            return "[GPT fallback] openai package not installed or API key missing."
        try:
            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role":"system","content":"You are a senior software engineer assistant."},
                          {"role":"user","content":prompt}],
                max_tokens=1024
            )
            return resp.choices[0].message.content
        except Exception as e:
            logger.exception("GPTService error")
            return f"[GPT error: {e}]"
