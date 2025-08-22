# engine/models.py
from typing import Iterator, List, Dict, Optional
import os

USE_OLLAMA = bool(int(os.getenv("USE_OLLAMA", "0")))
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-coder:6.7b") if USE_OLLAMA else os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def stream_reply(messages: List[Dict[str, str]]) -> Iterator[str]:
    if USE_OLLAMA:
        import ollama  # pip install ollama
        # stream tokens
        for chunk in ollama.chat(model=MODEL_NAME, messages=messages, stream=True):
            if "message" in chunk and "content" in chunk["message"]:
                yield chunk["message"]["content"]
    else:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        with client.chat.completions.stream.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.2
        ) as stream:
            for event in stream:
                if event.type == "token":
                    yield event.token
