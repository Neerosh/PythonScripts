import keyboard,time
from threading import Thread

def CheckAbbreviation():
    shortcuts = {
        "neerosh-github" : "https://github.com/Neerosh",
        "neerosh-site"   : "https://neerosh.github.io/"
    }
    for shortcut, fullText in shortcuts.items():
        keyboard.add_abbreviation(shortcut, fullText)
        # use space after typing the abbreviation to make python replace the text
    while True:  
        time.sleep(1)
        
# creates a new thread to avoid termination from exceptions like KeyboardException
thread = Thread(target=CheckAbbreviation)
thread.start()
thread.join()