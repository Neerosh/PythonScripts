import keyboard,time
from threading import Thread

def CheckAbbreviation():
    keyboard.add_abbreviation('neerosh-github', 'https://github.com/Neerosh')
    keyboard.add_abbreviation('neerosh-site', 'https://neerosh.github.io/')
    # use space after typing the abbreviation to make python replace the text
    while True:  
        time.sleep(1)
        
#creates a new thread to avoid termination from exceptions like KeyboardException
thread = Thread(target=CheckAbbreviation)
thread.start()
thread.join()