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
from engine.features import openCommand


# # DB connection
# con = sqlite3.connect('jarvis.db', check_same_thread=False)
# cursor = con.cursor()
@eel.expose
def playAssistantSound():
    playsound("frontend/assets/audio/start_sound.mp3")

def playYoutube(query):
    term = extract_yt_term(query)
    speak(f"Playing {term} on YouTube", eel)
    kit.playonyt(term)

def handleCommand(query):
    q = query.lower()

    if 'open' in q:
        openCommand(q)
        return True
    
    if 'youtube' in q:
        playYoutube(q)
        return True

    # Future: add WhatsApp, Instagram handling here
    
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