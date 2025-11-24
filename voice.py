import pyttsx3

engine = pyttsx3.init()

def speak(message):
    """
    Voice alert
    """
    engine.say(message)
    engine.runAndWait()
