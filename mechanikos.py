import sys,os
import time
import threading
import tkinter as tk

import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")

#Vague config class, will change asap
class Config():
    def __init__(self):
        self.delay=False
        self.miliseconds=False
        self.font="fixedsys"
        self.color="red"
        self.show=1
        self.offset=5
        self.size=32

    def valtype(self):
        self.show=int(self.show)
        self.offset=int(self.offset)
        self.size=int(self.size)

    def __str__(self):
        return "delay:{} mili:{} font:{} color:{} show:{} offset:{} size:{}".format(self.delay,
        self.miliseconds,self.font,self.color,self.show,self.offset,self.size)

class Timer():
    def __init__(self):
        self.first_time=time.time()

    def __call__(self):
        return time.time()-self.first_time

class shotcaller(threading.Thread):
    def run(self):
        pass
    def join(self):
        pass

class Timetable():
    "All the logic, updating and shotcalling"
    def __init__(self,timetables,config):
        self.timetables=timetables
        self.config=config
        self.waitfor=self.timetables[0][0]
        self.step=0
        self.ln=len(self.timetables)
        self.config=config
        self.shotcall=0

    def __call__(self,time,updateobject):
        if self.waitfor<time: # Time to change the text for the next mechanic
            updateobject.changeText(self.getnext()[1])
            self.step+=1
            self.waitfor=self.getnext()[0]
            self.shotcall=0 # You can shotcall again
            if self.step>self.ln: #Stop the program
                updateobject.destroy()
                sys.exit()

        elif self.waitfor<time+self.config.offset: #Time to shotcall
            if self.shotcall==0:
                self.shotcall=1 # You can't shotcall anymore
                print "Shotcalling"
                # Only shotcall the lines that exist
                print self.getnext()
        else:
            return None

    def getindex(self,index):
        try:
            return self.timetables[index]
        except:
            return [self.timetables[self.ln-1][0]+self.config.offset,"",""]

    def getnext(self):
        return self.getindex(self.step)

    def getnnext(self,nb):
        r=[]
        for i in range(nb):
            r.append(self.getindex(self.step+i))
        return r

#Utilities
def checkfile(f):
    'Check every line of the file for syntax errors and return the config, timetables'
    conf=f[0].split(";")
    timecheck=0
    table=[]
    try:
        config=load_conf(f[0])
    except:
        print('Error reading config')

    for i in range(1,len(f)):
        try:
            time,show,say=split_line(f[i])
            if time<timecheck:
                print("Error on the timetables line {}".format(i))
                raise AssertionError
            timecheck=time
            table.append([time,show,say])
        except:
            print("error line {} : {}".format(i,f[i]))
            sys.exit()
    return config,Timetable(table,config)

def load_conf(conf):
    "Load the confing in a line"
    C=Config()
    for line in conf.split(";"):
        if line=="delay":
            C.delay=True
        elif line=="miliseconds":
            C.miliseconds=True
        else:
            var,val=line.split('=')
            setattr(C,var,val)
    C.valtype()
    return C

def split_line(line):
    "Split lines according to the nominal format, return time as seconds"
    time,show,say=line.split("//")
    stime,time=time.split(":"),0
    for hms in stime:
        #Only powers of 60 so yeah; 1:12:33:11 will be incorrect, bite me
        time=time*60+int(hms)
    return time,show,say
# Init the thread for the TTS (can't have times offset by the wait)

# Load the Timetable
# First line should be config or empty
# Delay means delay mode instead of global time, miliseconds is miliseconds for time
# offset is the amount of time before the call (negative for precall)
# Every line Should look like Time (HH:MM:SS or SS) // Text to show // Text to say
try:
    print("Initialysing timer")
    gtimer=Timer()
    print("Opening Time Tables...")
    with open(sys.argv[1]) as f:
        time_data=f.read().splitlines()
    f.close()
    print("Cheking Time Data...")
    config,timetables=checkfile(time_data)
except:
    print "Error reading file"
    sys.exit()


class Application(tk.Frame):
    def __init__(self, master=None,gtimer=Timer(),config=None,shotcaller=None,timetables=None):
        self.timer=gtimer
        self.timetables=timetables
        self.gconfig=config
        tk.Frame.__init__(self, master)
        master.overrideredirect(True)
        master.geometry("+100+120")
        master.lift()
        master.wm_attributes("-topmost", True)
        master.wm_attributes("-disabled", True)
        master.wm_attributes("-transparentcolor", "white")
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.now = tk.StringVar()
        self.time = tk.Label(self,bg="white", height=2, width=30,bd=0,fg="red",font=("fixedsys", 22))
        self.time.pack(side="top")
        self.time["textvariable"] = self.now

        # initial time display
        self.onUpdate()

    def onUpdate(self):
        # update displayed time
        self.timetables(self.timer(),self)
        # schedule timer to call myself after 1 second
        self.after(100, self.onUpdate)

    def changeText(self,newtext):
        self.now.set(newtext)

root = tk.Tk()
app = Application(master=root,gtimer=gtimer,config=config,shotcaller=None,timetables=timetables)
root.mainloop()
