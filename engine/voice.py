# import pyttsx3
# import speech_recognition as sr

# # speak() jo text ko bolayega aur eel frontend me display bhi karega
# def speak(text, eel=None):
#     text = str(text)
#     engine = pyttsx3.init('sapi5')
#     voices = engine.getProperty('voices')
#     engine.setProperty('rate', 174)
#     engine.setProperty('voice', voices[1].id)

#     if eel:
#         eel.DisplayMessage(text)
#         eel.receiverText(text)

#     engine.say(text)
#     engine.runAndWait()

# # takecommand() jo awaz sunayega aur text return karega
# def takecommand(eel=None):
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         if eel: eel.DisplayMessage("Listening...")
#         r.pause_threshold = 1
#         r.adjust_for_ambient_noise(source)

#         try:
#             audio = r.listen(source, timeout=4, phrase_time_limit=3)
#         except Exception:
#             if eel: eel.DisplayMessage("Timeout ya silence hua...")
#             return "None"

#     try:
#         print("Recognizing...")
#         if eel: eel.DisplayMessage("Recognizing...")
#         query = r.recognize_google(audio, language='en-in')
#         print("User said:", query)
#         if eel: eel.DisplayMessage(query)
#         speak(query, eel)
#         return query.lower()
#     except Exception as e:
#         print(e)
#         if eel: eel.DisplayMessage("Dobara bolo please...")
#         return "None"
# engine/voice.py
import pyttsx3
import speech_recognition as sr
from engine.utils.logger import logger
from engine.utils.eel_helpers import safe_eel_call

def speak(text: str, eel=None):
    text = str(text)
    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 170)

        if eel:
            safe_eel_call("DisplayMessage", text)

        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        logger.exception("speak error")


def takecommand(eel=None, timeout=6, phrase_time_limit=5):
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            if eel:
                try: eel.DisplayMessage("Listening...")
                except: pass
            r.adjust_for_ambient_noise(source, duration=0.6)
            r.pause_threshold = 0.7
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    except Exception as e:
        if eel:
            try: eel.DisplayMessage("Timeout or no input.")
            except: pass
        return "None"

    try:
        query = r.recognize_google(audio, language='en-in')
        if eel:
            try: eel.DisplayMessage(query)
            except: pass
        speak(query, eel)
        return query.lower()
    except sr.UnknownValueError:
        if eel:
            try: eel.DisplayMessage("Didn't catch that.")
            except: pass
        return "None"
    except Exception as e:
        logger.exception("takecommand error")
        return "None"
