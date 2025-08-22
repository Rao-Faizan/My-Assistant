# engine/utils/config.py
import os
from dotenv import load_dotenv

load_dotenv()

USE_OLLAMA = os.getenv("USE_OLLAMA", "1").lower() in ("1", "true", "yes")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

FRONTEND_DIR = os.getenv("FRONTEND_DIR", "frontend")
INDEX_PAGE = os.getenv("INDEX_PAGE", "index.html")

DB_PATH = os.getenv("DB_PATH", "jarvis.db")
LOG_DIR = os.getenv("LOG_DIR", "logs")
