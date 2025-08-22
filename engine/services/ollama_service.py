# engine/services/ollama_service.py
import requests
import json
from engine.utils.config import OLLAMA_API_URL, OLLAMA_MODEL
from engine.utils.logger import logger

class OllamaService:
    def __init__(self, model: str = None, api_url: str = None):
        self.model = model or OLLAMA_MODEL
        self.api_url = api_url or OLLAMA_API_URL

    def get_response(self, prompt: str, stream: bool = False, timeout: int = 60):
        payload = {"model": self.model, "prompt": prompt}
        try:
            resp = requests.post(self.api_url, json=payload, stream=stream, timeout=timeout)
            resp.raise_for_status()

            if not stream:
                # return raw text
                return resp.text
            else:
                for raw in resp.iter_lines(decode_unicode=True):
                    if not raw:
                        continue
                    line = raw.strip()
                    if line.startswith("data: "):
                        line = line[len("data: "):]
                    # Try JSON parse
                    try:
                        obj = json.loads(line)
                        if isinstance(obj, dict):
                            for k in ("response", "message", "content", "text"):
                                if k in obj:
                                    yield obj[k]
                                    break
                            else:
                                yield json.dumps(obj)
                        else:
                            yield str(obj)
                    except Exception:
                        yield line
        except Exception as e:
            logger.exception("OllamaService error")
            if stream:
                yield f"[Ollama error: {e}]"
            else:
                return f"[Ollama error: {e}]"
