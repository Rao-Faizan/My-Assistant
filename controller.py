import multiprocessing
from main import start
from engine.features import hotword

def startJarvis():
    print("Starting process 01 (JARVIS)")
    start()

def hotwordDetection():
    print("Starting process 02 (Hotword)")
    hotword()

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=startJarvis)
    p2 = multiprocessing.Process(target=hotwordDetection)

    p1.start()
    p2.start()
    p1.join()

    if p2.is_alive():
        p2.terminate()
        p2.join()

    print("All processes completed.")
