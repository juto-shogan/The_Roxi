from narwhals import Duration
import speech_recognition as sr
import pyttsx3

# Create a Recognizer instance
r = sr.Recognizer()
  
  
def speakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
    
with sr.Microphone() as source2:
    r.adjust_for_ambient_noise(source2, duration=0.2)
    
    audio2 = r.listen(source2)
    
    mytext = r.recognize_google(audio2)
    mytext = mytext.lower()
    
    print('did you say' +mytext)
    speakText(mytext)