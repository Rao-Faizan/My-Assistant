# main.py - Multi-Agent AI Assistant
import os
import eel
import threading
import traceback
from dotenv import load_dotenv
from backend.command import playAssistantSound, allCommands
from backend.utils.config import FRONTEND_DIR, INDEX_PAGE
from backend.utils.logger import logger
from backend.agents.orchestrator import AgentOrchestrator

# Load environment variables
load_dotenv()

# Set Gemini API key directly (permanent solution)
os.environ['GEMINI_API_KEY'] = 'AIzaSyAZe8Oc30DZho82F0qE9Z-RzNiKSyxEw88'

# Initialize the multi-agent orchestrator
def initialize_orchestrator():
    """Initialize the multi-agent orchestrator"""
    try:
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")
            return None
        
        orchestrator = AgentOrchestrator(gemini_api_key)
        logger.info("Multi-agent orchestrator initialized successfully")
        return orchestrator
    except Exception as e:
        logger.error(f"Error initializing orchestrator: {e}")
        return None

# Global orchestrator instance
orchestrator = None

def start():
    global orchestrator
    
    try:
        # Initialize orchestrator
        orchestrator = initialize_orchestrator()
        
        if not os.path.isdir(FRONTEND_DIR):
            print(f"Frontend folder '{FRONTEND_DIR}' not found.")
            return

        eel.init(FRONTEND_DIR)

        # Play startup sound
        try:
            playAssistantSound()
        except:
            pass

        print("Starting Multi-Agent AI Assistant...")
        print("Opening browser at: http://localhost:8003")
        
        # Open in default browser
        try:
            import webbrowser
            webbrowser.open('http://localhost:8003')
        except:
            pass

        eel.start(INDEX_PAGE, mode=None, block=True, port=8003)

    except Exception as e:
        logger.exception("start() error")
        traceback.print_exc()

# Enhanced command processing with multi-agent system
def process_with_orchestrator(user_input: str):
    """Process user input using the multi-agent orchestrator"""
    global orchestrator
    
    if not orchestrator:
        logger.warning("Orchestrator not initialized")
        return None
    
    try:
        result = orchestrator.route_request(user_input)
        
        if result["status"] == "success":
            return f"[{result['agent_used']}] {result['result']}"
        else:
            return f"Error: {result.get('message', 'Unknown error')}"
            
    except Exception as e:
        logger.error(f"Error processing with orchestrator: {e}")
        return f"Error processing request: {e}"

# Expose orchestrator functions to Eel
@eel.expose
def process_orchestrator_request(user_input: str):
    """Expose orchestrator to frontend"""
    return process_with_orchestrator(user_input)

@eel.expose
def send_welcome_message():
    """Send welcome message on startup"""
    return "Welcome! I'm your Multi-Agent AI Assistant. I can help you with tasks, formal communication, opening apps, and voice commands. What would you like me to do?"


if __name__ == "__main__":
    start()