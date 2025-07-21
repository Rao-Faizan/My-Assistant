import os
import json
import webbrowser
import requests
import pywhatkit as kit
import eel
import speech_recognition as sr
from playsound import playsound
from engine.db import cursor
from engine.voice import speak, takecommand
from engine.config import ASSISTANT_NAME
from engine.helper import extract_yt_term

# Global chat history
chat_history = []

# === HOTWORD DETECTION ===
def hotword():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    print("🎙️ Hotword listener active... Say 'Jarvis' to activate.")
    speak("Say 'Jarvis' to activate me")

    while True:
        with mic as source:
            print("🔍 Listening for wake word...")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio).lower()
            print("You said:", text)

            if "jarvis" in text:
                print("✅ Hotword detected: JARVIS")
                speak("Yes, I am here")

                # Run allCommands in a new thread so hotword listener stays alive
                threading.Thread(target=allCommands).start()

        except sr.UnknownValueError:
            continue
        except Exception as e:
            print("Hotword error:", e)

# === OPEN COMMAND ===
def openCommand(query):
    try:
        query = query.replace("open", "").strip().lower()

        # Web command
        cursor.execute("SELECT url FROM web_command WHERE LOWER(name) = ?", (query,))
        web_result = cursor.fetchone()
        if web_result:
            url = web_result[0]
            speak(f"Opening {query}")
            webbrowser.open(url)
            print(f"Opening website: {url}")
            return

        # System app command
        cursor.execute("SELECT path FROM sys_command WHERE LOWER(name) = ?", (query,))
        sys_result = cursor.fetchone()
        if sys_result:
            path = sys_result[0]
            speak(f"Opening {query}")
            os.startfile(path)
            print(f"Launching system app: {path}")
            return

        # Not found
        speak(f"Sorry, I couldn't find {query}")
        print(f"[✘] No entry found for '{query}'")

    except Exception as e:
        print("OpenCommand‑Error:", e)
        speak("Error while trying to open the application.")

# === PLAY YOUTUBE ===
def playYoutube(query):
    search_query = extract_yt_term(query)
    speak(f"Playing {search_query} on YouTube")
    kit.playonyt(search_query)

# === CHATBOT ===
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

# === COMMAND ROUTING ===
def allCommands(query=None):
    if query is None:
        query = takecommand()
    
    query = query.lower()

    if "open" in query:
        openCommand(query)
    elif "play" in query and "youtube" in query:
        playYoutube(query)
    elif "whatsapp" in query:
        # Add WhatsApp logic here
        pass
    else:
        chatBot(query)

# === VOICE ACTIVATED LISTENER WRAPPER ===
def handleCommand(query):
    print(f">> Handling Command: {query}")
    allCommands(query)
