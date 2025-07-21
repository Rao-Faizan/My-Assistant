import os
import json
import sqlite3
import struct
import subprocess
import time
import webbrowser
from urllib.parse import quote
from engine.db import cursor
import requests
import pyautogui
import pywhatkit as kit
import eel
import pvporcupine
import pyaudio
from playsound import playsound
from engine.voice import speak
from engine.config import ASSISTANT_NAME
from engine.helper import extract_yt_term

# Global chat history
chat_history = []

# # Connect DB
# con = sqlite3.connect('jarvis.db')
# cursor = con.cursor()

def handleCommand(query):
    print(f">> Handling Command: {query}")
    allCommands(query)

def allCommands(query):
    query = query.lower()

    if "open" in query:
        openCommand(query)  # ✅ This triggers your working openCommand function
    elif "play" in query and "youtube" in query:
        playYoutube(query)
    elif "whatsapp" in query:
        # WhatsApp demo, actual number mapping can be added later
        whatsApp("+911234567890", "Hello", "message", "Demo User")
    else:
        chatBot(query)

def playYoutube(query):
    search_query = extract_yt_term(query)
    speak(f"Playing {search_query} on YouTube")
    kit.playonyt(search_query)

def whatsApp(mobile_no, message, flag, name):
    tabs = {'message': 12, 'call': 7, 'video': 6}
    jarvis_msg = {
        'message': f"Message sent successfully to {name}",
        'call': f"Calling {name}",
        'video': f"Starting video call with {name}"
    }

    target_tab = tabs.get(flag, 12)
    encoded_msg = quote(message or "")
    url = f"whatsapp://send?phone={mobile_no}&text={encoded_msg}"

    subprocess.run(f'start "" "{url}"', shell=True)
    time.sleep(5)
    subprocess.run(f'start "" "{url}"', shell=True)

    pyautogui.hotkey('ctrl', 'f')
    for _ in range(1, target_tab):
        pyautogui.hotkey('tab')
    pyautogui.hotkey('enter')

    speak(jarvis_msg.get(flag, "Done"))

def chatBot(query):
    global chat_history
    try:
        chat_history.append(f"User: {query}")
        prompt = "\n".join(chat_history) + "\nAI:"

        response = requests.post(
            'http://localhost:11434/api/generate',
            json={"model": "llama3", "prompt": prompt},
            stream=True
        )

        final_response = ""
        for line in response.iter_lines():
            if line:
                data = line.decode('utf-8')
                if 'response' in data:
                    msg = json.loads(data)["response"]
                    final_response += msg

        final_response = final_response.strip()
        chat_history.append(f"AI: {final_response}")
        eel.receiverText(final_response)
        speak(final_response)
        print(final_response)
        return final_response

    except Exception as e:
        speak("Sorry, something went wrong with the AI model.")
        print("ChatBot Error:", e)
        return "Error"
