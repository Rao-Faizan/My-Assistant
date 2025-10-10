import os
import sqlite3
import webbrowser
import requests
import pyautogui
import pywhatkit as kit
import eel
import pygame
from urllib.parse import quote
from backend.db import cursor
from backend.voice import speak, takecommand
from backend.config import ASSISTANT_NAME
from backend.helper import extract_yt_term
from backend.features import openCommand
from backend.chatbot_manager import ChatbotManager
from backend.utils.logger import logger

# Initialize chatbot
_voice_chatbot = ChatbotManager(provider="gemini", stream=False)

# # # DB connection
# # con = sqlite3.connect('jarvis.db', check_same_thread=False)
# # cursor = con.cursor()
# Duplicate function removed - see line 95

# def playYoutube(query):
#     term = extract_yt_term(query)
#     speak(f"Playing {term} on YouTube", eel)
#     kit.playonyt(term)

# def handleCommand(query):
#     q = query.lower()

#     if 'open' in q:
#         openCommand(q)
#         return True
    
#     if 'youtube' in q:
#         playYoutube(q)
#         return True

#     # Future: add WhatsApp, Instagram handling here
    
#     return False

# @eel.expose
# def allCommands(message=1):
#     if message == 1:
#         query = takecommand(eel)
#     else:
#         query = message

#     eel.senderText(query)

#     if not handleCommand(query):
#         chatBot(query)

#     eel.ShowHome()
# engine/command.py
import os
import webbrowser
import pywhatkit as kit
import eel
import pygame
from backend.db import cursor
from backend.voice import speak, takecommand
from backend.helper import extract_yt_term
from backend.file_tools import save_code_file
from backend.chatbot_manager import ChatbotManager
from backend.utils.logger import logger
_voice_chatbot = ChatbotManager(provider="gemini", stream=False)

# ---------------- Eel exposed functions ----------------

@eel.expose
def receiverText(message):
    """Send AI response to frontend."""
    print(f"AI: {message}")
    return message

@eel.expose
def senderText(message):
    """Send User message to frontend."""
    print(f"User: {message}")
    return message

@eel.expose
def playAssistantSound():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("frontend/assets/audio/start_sound.mp3")
        pygame.mixer.music.play()
    except Exception:
        pass

@eel.expose
def allCommands(message=1):
    """Main entry point for voice/text commands with multi-agent system."""
    if message == 1:
        query = takecommand(eel)
    else:
        query = message

    if not query or query == "None":
        eel.receiverText("No input detected.")
        return

    eel.senderText(query)

    try:
        # Use multi-agent system for better responses
        try:
            # Use orchestrator directly without circular import
            from backend.agents.orchestrator import AgentOrchestrator
            import os
            
            # Get API key from environment or use hardcoded
            api_key = os.getenv('GEMINI_API_KEY') or 'AIzaSyAZe8Oc30DZho82F0qE9Z-RzNiKSyxEw88'
            
            # Create temporary orchestrator for this request
            temp_orchestrator = AgentOrchestrator(api_key)
            result = temp_orchestrator.route_request(query)
            
            if result["status"] == "success":
                eel.receiverText(f"[{result['agent_used']}] {result['result']}")
                return
            else:
                logger.warning(f"Orchestrator failed: {result.get('message', 'Unknown error')}")
        except Exception as e:
            logger.error(f"Orchestrator error: {e}")
        
        # Fallback to original command handling only if orchestrator failed
        handled = handleCommand(query)
        
        if handled:
            eel.receiverText(f"✅ Command executed: {query}")
        else:
            # Use chatbot for general queries
            logger.info(f"Using chatbot for query: {query}")
            chatBot(query)
    except Exception:
        eel.receiverText("Sorry, an error occurred while processing your request.")

    try:
        eel.ShowHome()
    except:
        pass

# ---------------- Command Handlers ----------------

def playYoutube(query):
    term = extract_yt_term(query) or query
    speak(f"Playing {term} on YouTube", eel)
    kit.playonyt(term)

def openCommand(query):
    try:
        q = query.replace("open", "").strip().lower()

        # Web command
        cursor.execute("SELECT url FROM web_command WHERE LOWER(name)=?", (q,))
        web_result = cursor.fetchone()
        if web_result:
            url = web_result[0]
            speak(f"Opening {q}", eel)
            webbrowser.open(url)
            return True

        # System command
        cursor.execute("SELECT path FROM sys_command WHERE LOWER(name)=?", (q,))
        sys_result = cursor.fetchone()
        if sys_result:
            path = sys_result[0]
            speak(f"Opening {q}", eel)
            os.startfile(path)
            return True

        return False

    except Exception as e:
        logger.exception("openCommand error")
        speak("Error while opening the app.", eel)
        return False

def handleCommand(query):
    q = query.lower()

    if 'open' in q:
        return openCommand(q)
    if 'youtube' in q:
        playYoutube(q)
        return True
    if 'whatsapp' in q:
        speak("Opening WhatsApp Web", eel)
        webbrowser.open("https://web.whatsapp.com/")
        return True
    if 'instagram' in q:
        speak("Opening Instagram", eel)
        webbrowser.open("https://www.instagram.com/")
        return True
    if q.startswith("save file:") or q.startswith("savefile:"):
        try:
            parts = query.split(":", 2)
            if len(parts) >= 3:
                _, path, code = parts
                path = path.strip()
                code = code.strip()
                result = save_code_file(path, code)
                if result.get("ok"):
                    eel.receiverText("File saved successfully.")
                    logger.info("File saved: %s", result.get("backup"))
                    return True
                else:
                    eel.receiverText(f"Save failed: {result.get('error')}")
                    return True
        except Exception as e:
            logger.exception("save file error")
            eel.receiverText("Error saving file.")
            return True

    return False

# ---------------- Chatbot ----------------

chat_history = []

def chatBot(query):
    global chat_history
    try:
        logger.info(f"Processing chat query: {query}")
        chat_history.append(f"User: {query}")
        prompt = "\n".join(chat_history) + "\nAI:"
        
        # Use multi-agent system for better responses
        try:
            # Use orchestrator directly without circular import
            from backend.agents.orchestrator import AgentOrchestrator
            import os
            
            # Get API key from environment or use hardcoded
            api_key = os.getenv('GEMINI_API_KEY') or 'AIzaSyAZe8Oc30DZho82F0qE9Z-RzNiKSyxEw88'
            
            # Create temporary orchestrator for this request
            temp_orchestrator = AgentOrchestrator(api_key)
            result = temp_orchestrator.route_request(query)
            
            if result["status"] == "success":
                final_response = f"[{result['agent_used']}] {result['result']}"
            else:
                # Fallback to original chatbot
                response = _voice_chatbot.ask(prompt)
                final_response = ""
                if hasattr(response, "__iter__") and not isinstance(response, (str, bytes)):
                    for chunk in response:
                        final_response += str(chunk)
                else:
                    final_response = str(response)
                final_response = final_response.strip()
        except Exception as e:
            logger.error(f"Orchestrator error in chatBot: {e}")
            # Fallback to original chatbot
            response = _voice_chatbot.ask(prompt)
            final_response = ""
            if hasattr(response, "__iter__") and not isinstance(response, (str, bytes)):
                for chunk in response:
                    final_response += str(chunk)
            else:
                final_response = str(response)
            final_response = final_response.strip()

        chat_history.append(f"AI: {final_response}")

        try:
            eel.receiverText(final_response)
            logger.info(f"Sent response: {final_response}")
        except Exception as e:
            logger.error(f"Error sending response to frontend: {e}")

        speak(final_response, eel)
        return final_response

    except Exception as e:
        logger.exception("chatBot error")
        speak("Sorry, something went wrong with the AI model.", eel)
        return "Error"
