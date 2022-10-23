import speech_recognition
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

def InitializeVoiceEngine():
    voiceEngine = pyttsx3.init()
    voices = voiceEngine.getProperty('voices')  
    rate = voiceEngine.getProperty('rate')

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    voiceEngine.setProperty('rate', rate-50)
    #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. 0 for male
    voiceEngine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
    return voiceEngine

# ==== Voice Control
def Speak(text,voiceEngine):
    voiceEngine.say(text)
    voiceEngine.runAndWait()
    # ====Default Start

# ==== Take Command
def TakeCommand(listener):
    try:
        with speech_recognition.Microphone() as data_taker:
            voice = listener.listen(data_taker,timeout=5,phrase_time_limit=5)       
            instruction = listener.recognize_google(voice)
            instruction = instruction.lower()
            return instruction
    except Exception as ex:
        pass
    return ""
    # ==== Run command

def RunCommand(listener,voiceEngine):
    instruction = TakeCommand(listener)
    result = True
    nameAssistant = 'Silver'
    try:  
        logging.info(f"Instruction: {instruction}")
        
        if instruction == "" or nameAssistant.lower() not in instruction:
            return True
        
        elif "who are you" in instruction:
            Speak(f"I am your python personal voice assistant",voiceEngine)
            
        elif 'current time' in instruction:
            time = datetime.datetime.now().strftime('%I: %M')
            Speak('current time is' + time,voiceEngine)
            
        elif "open music player" in instruction:
            Speak('Opening Music Player',voiceEngine)
            # Windows only
            os.system(r'start "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\AIMP" AIMP')
            
        elif "open brave" in instruction:
            Speak('Opening Brave',voiceEngine)
            webbrowser.get('brave').open('duckduckgo.com')
            
        elif "open youtube" in instruction:
            Speak('Opening Youtube',voiceEngine)
            webbrowser.get('brave').open('youtube.com')

        elif "open gmail" in instruction:
            Speak('Opening Gmail',voiceEngine)
            webbrowser.get('brave').open('gmail.com')

        elif "shutdown" in instruction:
            Speak('I am shutting down',voiceEngine)
            result = False
        
        else:
            Speak('I did not understand, can you repeat again',voiceEngine)
    except Exception as ex:
        logging.error(f"Run Command Exception: {ex}")
    return result

def Main():
    voiceEngine = InitializeVoiceEngine()
    listener = speech_recognition.Recognizer()
    
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    SetupBrowser()
    
    # ====To run assistance continuously
    while RunCommand(listener,voiceEngine):
        pass


if __name__ == "__main__":
    Main()
