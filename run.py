# # import multiprocessing
# # from hugchat import ChatBot
# # import os

# # def startJarvis():
# #     print("Starting process 01")
# #     from main import start
# #     start()

# # def hotwordDetection():
# #     print("Starting process 02")
# #     from engine.features import hotword
# #     hotword()

# # if __name__ == '__main__':
# #     # Optional: Set Hugging Face token here (you can set via environment variable too)
# #     token = "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"  # <- Replace with your actual token

# #     # create processes
# #     p1 = multiprocessing.Process(target=startJarvis)
# #     p2 = multiprocessing.Process(target=hotwordDetection)
# #     p1.start()
# #     p2.start()
# #     p1.join()

# #     if p2.is_alive():
# #         p2.terminate()
# #         p2.join()

# #     # Testing ChatBot
# #     chatbot = ChatBot(token=token)
# #     print(chatbot.chat("Hello Jarvis!"))

# #     print("All processes are done")
# import multiprocessing
# from main import start  # Jarvis main logic
# from engine.hotword import hotword

# # Process 1: Start Jarvis UI + listener
# def startJarvis():
#     print("🚀 Starting process 01 (Jarvis)")
#     start()

# # Process 2: Start Hotword Detection
# def startHotword():
#     print("🎙️ Starting process 02 (Hotword Listener)")
#     hotword()

# if __name__ == '__main__':
#     print(">>")
    
#     # Create and start processes
#     p1 = multiprocessing.Process(target=startJarvis)
#     p2 = multiprocessing.Process(target=startHotword)

#     p1.start()
#     p2.start()

#     # Wait for main Jarvis to finish
#     p1.join()

#     # Clean up hotword if still alive
#     if p2.is_alive():
#         p2.terminate()
#         p2.join()

#     print("✅ All processes are done")
# run.py
import multiprocessing
import sys
from main import start
from engine.hotword import hotword
from engine.utils.logger import logger

def startJarvis():
    try:
        start()
    except Exception as e:
        logger.exception("startJarvis error")

def startHotword():
    try:
        hotword()
    except Exception as e:
        logger.exception("hotword process error")

if __name__ == '__main__':
    multiprocessing.set_start_method("spawn", force=True)
    p1 = multiprocessing.Process(target=startJarvis, name="JarvisProcess")
    p2 = multiprocessing.Process(target=startHotword, name="HotwordProcess")
    p1.start()
    p2.start()
    try:
        p1.join()
    except KeyboardInterrupt:
        pass
    finally:
        if p2.is_alive():
            p2.terminate()
            p2.join(timeout=5)
        if p1.is_alive():
            p1.terminate()
            p1.join(timeout=5)
    sys.exit(0)
