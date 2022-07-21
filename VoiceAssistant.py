from types import NoneType
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import logging
import os

def SetupBrowser():
    # getting path
    brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    # First registers the new browser
    webbrowser.register('brave', None, 
                        webbrowser.BackgroundBrowser(brave_path))

# ==== Voice Control
def Speak(text):
    engine.say(text)
    engine.runAndWait()
    # ====Default Start

# ==== Take Command
def TakeCommand():
    nameAssistant = 'Silver'
    try:
        with sr.Microphone() as data_taker:
            voice = listener.listen(data_taker,timeout=5,phrase_time_limit=5)       
            instruction = listener.recognize_google(voice)
            instruction = instruction.lower()
            return instruction
    except Exception as ex:
        pass
    return ""
    # ==== Run command

def RunCommand():
    instruction = TakeCommand()
    result = True
    nameAssistant = 'Silver'
    try:  
        logging.info(f"Instruction: {instruction}")
        
        if instruction == "" or nameAssistant.lower() not in instruction:
            return True
        
        elif "who are you" in instruction:
            Speak(f"I am your python personal voice assistant")
            
        elif 'current time' in instruction:
            time = datetime.datetime.now().strftime('%I: %M')
            Speak('current time is' + time)
            
        elif "open music player" in instruction:
            Speak('Opening Music Player')
            # Windows only
            os.system(r'start "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\AIMP" AIMP')
            
        elif "open brave" in instruction:
            Speak('Opening Brave')
            webbrowser.get('brave').open('duckduckgo.com')
            
        elif "open youtube" in instruction:
            Speak('Opening Youtube')
            webbrowser.get('brave').open('youtube.com')

        elif "open gmail" in instruction:
            Speak('Opening Gmail')
            webbrowser.get('brave').open('gmail.com')

        elif "shutdown" in instruction:
            Speak('I am shutting down')
            result = False
        
        else:
            Speak('I did not understand, can you repeat again')
    except Exception as ex:
        logging.error(f"Run Command Exception: {ex}")
    return result


engine = pyttsx3.init()
voices = engine.getProperty('voices')  
rate = engine.getProperty('rate')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

engine.setProperty('rate', rate-50)
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. 0 for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

listener = sr.Recognizer()
SetupBrowser()

# ====To run assistance continuously
while RunCommand():
    pass
