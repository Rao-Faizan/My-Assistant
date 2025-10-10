# engine/chatbot_manager.py
from backend.utils.config import USE_OLLAMA
from backend.services.ollama_service import OllamaService
from backend.services.gpt_service import GPTService
from backend.services.gemini_service import GeminiService
from backend.utils.logger import logger

class ChatbotManager:
    def __init__(self, provider: str = None, stream: bool = True):
        self.stream = stream
        if provider:
            self.use_ollama = (provider.lower() == "ollama")
            self.use_gemini = (provider.lower() == "gemini")
        else:
            self.use_ollama = USE_OLLAMA
            self.use_gemini = True  # Default to Gemini

        if self.use_gemini:
            self.service = GeminiService()
            logger.info("ChatbotManager using GeminiService")
        elif self.use_ollama:
            self.service = OllamaService()
            logger.info("ChatbotManager using OllamaService")
        else:
            self.service = GPTService()
            logger.info("ChatbotManager using GPTService")

    def ask(self, prompt: str):
        try:
            if self.stream and hasattr(self.service, "get_response"):
                result = self.service.get_response(prompt, stream=True)
                if hasattr(result, "__iter__") and not isinstance(result, (str, bytes)):
                    return result
                else:
                    return str(result)
            else:
                return self.service.get_response(prompt, stream=False)
        except Exception as e:
            logger.exception("ChatbotManager ask error")
            return f"[Chatbot error: {e}]"
