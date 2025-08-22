# engine/chatbot_manager.py
from engine.utils.config import USE_OLLAMA
from engine.services.ollama_service import OllamaService
from engine.services.gpt_service import GPTService
from engine.utils.logger import logger

class ChatbotManager:
    def __init__(self, provider: str = None, stream: bool = True):
        self.stream = stream
        if provider:
            self.use_ollama = (provider.lower() == "ollama")
        else:
            self.use_ollama = USE_OLLAMA

        if self.use_ollama:
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
