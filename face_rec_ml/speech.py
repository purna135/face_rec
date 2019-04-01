import win32com.client as wincl
def speak(text):
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak(text)



# import pyttsx3
# engine = pyttsx3.init()

# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id) #change index to change voices

# engine.setProperty('rate',160)  #120 words per minute
# engine.setProperty('volume',0.9)

# def speak(text):
# 	engine.say(text)
# 	engine.runAndWait()