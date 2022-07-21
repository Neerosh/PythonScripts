import pyttsx3

# init function to get an engine instance for the speech synthesis
engine = pyttsx3.init()

voices = engine.getProperty('voices')  
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. 0 for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

print("\nType 'exit' to close this program.")
print(voices[0].languages)
while True:
    text = input('Please Type Some Text To Convert to Speech: \n')
    if text == 'exit' or text == '':
        print("Program closed...\n")
        break
    # say method on the engine that passing input text to be spoken
    engine.say(text)
    # run and wait method, it processes the voice commands.
    engine.runAndWait()

