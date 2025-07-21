import pyttsx3
import speech_recognition as sr

# speak() jo text ko bolayega aur eel frontend me display bhi karega
def speak(text, eel=None):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 174)
    engine.setProperty('voice', voices[1].id)

    if eel:
        eel.DisplayMessage(text)
        eel.receiverText(text)

    engine.say(text)
    engine.runAndWait()

# takecommand() jo awaz sunayega aur text return karega
def takecommand(eel=None):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        if eel: eel.DisplayMessage("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        try:
            audio = r.listen(source, timeout=4, phrase_time_limit=3)
        except Exception:
            if eel: eel.DisplayMessage("Timeout ya silence hua...")
            return "None"

    try:
        print("Recognizing...")
        if eel: eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("User said:", query)
        if eel: eel.DisplayMessage(query)
        speak(query, eel)
        return query.lower()
    except Exception as e:
        print(e)
        if eel: eel.DisplayMessage("Dobara bolo please...")
        return "None"
