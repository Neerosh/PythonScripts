import keyboard,time
from threading import Thread

def CheckAbbreviation():
    abbreviations = {
        "neerosh-github" : "https://github.com/Neerosh",
        "neerosh-site"   : "https://neerosh.github.io"
    }
    for abbreviation, fullText in abbreviations.items():
        keyboard.add_abbreviation(abbreviation, fullText)
        # use space after typing the abbreviation to make python replace the text
    while True:  
        time.sleep(1)
       
def Main():
    # creates a new thread to avoid termination from exceptions like KeyboardException
    thread = Thread(target=CheckAbbreviation)
    thread.start()
    thread.join()
        
if __name__ == "__main__":
    Main()