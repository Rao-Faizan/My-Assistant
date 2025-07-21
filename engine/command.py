import os
import sqlite3
import webbrowser
import requests
import pyautogui
import pywhatkit as kit
import eel
from urllib.parse import quote
from playsound import playsound
from engine.db import cursor
from engine.voice import speak, takecommand
from engine.config import ASSISTANT_NAME
from engine.helper import extract_yt_term

# # DB connection
# con = sqlite3.connect('jarvis.db', check_same_thread=False)
# cursor = con.cursor()

@eel.expose
def playAssistantSound():
    playsound("frontend/assets/audio/start_sound.mp3")

def openCommand(query):
    try:
        query = query.replace("open", "").strip().lower()

        # Check for web commands first
        cursor.execute("SELECT url FROM web_command WHERE LOWER(name) = ?", (query,))
        web_result = cursor.fetchone()
        if web_result:
            url = web_result[0]
            speak(f"Opening {query}")
            webbrowser.open(url)
            print(f"Opening website: {url}")
            return

        # Else check for system apps
        cursor.execute("SELECT path FROM sys_command WHERE LOWER(name) = ?", (query,))
        sys_result = cursor.fetchone()
        if sys_result:
            path = sys_result[0]
            speak(f"Opening {query}")
            os.startfile(path)
            print(f"Launching system app: {path}")
            return

        # If not found in both
        speak(f"Sorry, I couldn't find {query}")
        print(f"[✘] No entry found for '{query}'")

    except Exception as e:
        print("OpenCommand‑Error:", e)
        speak("Error while trying to open the application.")

def playYoutube(query):
    term = extract_yt_term(query)
    speak(f"Playing {term} on YouTube", eel)
    kit.playonyt(term)

def chatBot(query):
    # your chatbot logic here
    pass

def handleCommand(query):
    q = query.lower()
    if 'open' in q:
        openCommand(q); return True
    if 'youtube' in q:
        playYoutube(q); return True
    # add whatsapp, instagram etc similarly
    return False

@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand(eel)
    else:
        query = message
    eel.senderText(query)
    if not handleCommand(query):
        chatBot(query)
    eel.ShowHome()
