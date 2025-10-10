# engine/services/gemini_service.py
import os
import google.generativeai as genai
from backend.utils.logger import logger

class GeminiService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY') or 'AIzaSyAZe8Oc30DZho82F0qE9Z-RzNiKSyxEw88'
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            logger.info("GeminiService initialized successfully")
        else:
            logger.error("GEMINI_API_KEY not found")
            self.model = None

    def get_response(self, prompt: str, stream: bool = False):
        if not self.model:
            return "Error: Gemini API key not configured"
        
        try:
            if stream:
                response = self.model.generate_content(prompt, stream=True)
                return response
            else:
                response = self.model.generate_content(prompt)
                return response.text
        except Exception as e:
            logger.error(f"GeminiService error: {e}")
            return f"Error: {str(e)}"
