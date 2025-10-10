import speech_recognition as sr
from backend.voice import speak
from backend.features import allCommands

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
            print("Recognizing...")
            text = recognizer.recognize_google(audio).lower()
            print("You said:", text)

            if "jarvis" in text:
                print("✅ Hotword detected: JARVIS")
                speak("Yes, I am here. What can I do for you?")

                # 🎧 Listen to a single command only
                with mic as source:
                    print("🎧 Listening for your command...")
                    recognizer.adjust_for_ambient_noise(source)
                    command_audio = recognizer.listen(source)

                try:
                    query = recognizer.recognize_google(command_audio).lower()
                    print("User said:", query)

                    if "exit" in query or "stop" in query:
                        speak("Okay, stopping for now.")
                        break

                    allCommands(query)

                except sr.UnknownValueError:
                    speak("Sorry, I didn’t catch that. Please say the command again next time.")
                except Exception as e:
                    print("Command error:", e)
                    speak("Something went wrong while processing your command.")

        except sr.UnknownValueError:
            pass
        except Exception as e:
            print("Hotword error:", e)
