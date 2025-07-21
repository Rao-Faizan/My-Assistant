import os
import eel
import threading
from engine.command import playAssistantSound
from engine.hotword import hotword

# from engine.features import playAssistantSound
from engine.command import handleCommand
from engine.llm import get_llm_response  # <-- This is our Ollama handler

# Initialize Eel with the frontend folder
def start():
    eel.init("frontend")

    # Play startup sound

    # Open Edge browser in app mode (can replace with chrome or other)
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    # Start eel and expose functions
    register_eel_functions()

    # Run the app (non-blocking allows response handling in background)
    eel.start("index.html", mode=None, block=True)


# Function to expose all Eel-exposed functions
def register_eel_functions():
    @eel.expose
    def processUserMessage(message):
        print("User said:", message)
        
        eel.senderText(message)

        if message.strip() == "":
            eel.receiverText("Please enter something.")
            return

        try:
            # Handle custom commands first (YouTube, open apps, etc.)
            if handleCommand(message.lower()):
                eel.receiverText("Command executed.")
            else:
                # Get AI response from Ollama
                eel.receiverText("Thinking...")
                thread = threading.Thread(target=respond_using_llm, args=(message,))
                thread.start()
        except Exception as e:
            eel.receiverText("Sorry, an error occurred.")
            print("Error in processUserMessage:", e)


# This function calls Ollama's local model and returns the AI's response
def respond_using_llm(prompt):
    try:
        response = get_llm_response(prompt)
        eel.receiverText(response)
    except Exception as e:
        eel.receiverText("Error in generating response.")
        print("Ollama error:", e)
if __name__ == "__main__":
    hotword()