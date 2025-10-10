import pyttsx3
import speech_recognition as sr
from backend.utils.logger import logger
from backend.utils.eel_helpers import safe_eel_call

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
        query = r.recognize_google(audio, language='en-US')
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
