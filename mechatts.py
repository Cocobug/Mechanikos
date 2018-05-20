import threading
try:
    import win32com.client as wincl
    def speak_function(text):
        speak = wincl.Dispatch("SAPI.SpVoice")
        speak.Speak(text)
except:
    import pyttsx

    def speak_function(text):
        engine = pyttsx.init()
        engine.setProperty('rate', 170)
        engine.say(text)
        engine.runAndWait()

class ttsObject():
    def __init__(self):
        self.wait=None

    def Speak(self,text):
        if self.wait!=None:
            self.wait.join()
        self.wait=threading.Thread(target=speak_function,args=(text,))
        self.wait.start()
        return self.wait

if __name__ == '__main__':
    import sys,time

    tts=ttsObject()
    w=tts.Speak("A Very long text")
    print "Uninterupted function"
    w=tts.Speak("As I was Saying A")
    w=tts.Speak("While B")
    w.join()
    speak_function("While B")
    #w.join()
