import threading
try:
    import win32com.client as wincl
    speak = wincl.Dispatch("SAPI.SpVoice")
    def speak_function(text):
        speak.Speak(text)
except:
    try:
        import pyttsx
        def speak_function(text):
            engine = pyttsx.init()
            engine.setProperty('rate', 170)
            engine.say(text)
            engine.runAndWait()
    except:
        print("No tts software was available, install either pywin32 or pyttsx")
        def speak_function(text):
            pass

class ttsObject():
    def __init__(self):
        self.wait=None

    def Speak(self,text):
        #if self.wait!=None:
        #    self.wait.join()
        #self.wait=threading.Thread(target=speak_function,args=(text,))
        #self.wait.start()
        #return self.wait
        try:
            speak_function(text)
        except:
            print("Error while calling tts function")

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
