import sys,os
import time
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

from mechatts import ttsObject as tts
speak = tts()

#Vague config class, will change asap
def checktrue(a):
    if a=="True" or a==True:
        return True
    return False

class Config():
    def __init__(self):
        self.delaymode=False
        self.miliseconds=False
        self.quitbutton=True
        self.ihateTTS=False
        self.font="fixedsys"
        self.color="red"
        self.show=1
        self.height=7
        self.width=30
        self.calldelay=5
        self.size=32
        self.border=0
        self.delay=0
        self.x=220
        self.y=220

    def valtype(self):
        self.show=int(self.show)
        self.calldelay=int(self.calldelay)
        self.size=int(self.size)
        self.height=int(self.height)
        self.width=int(self.width)
        self.delay=int(self.delay)
        self.delaymode=checktrue(self.delay)
        self.ihateTTS=checktrue(self.ihateTTS)
        self.miliseconds=checktrue(self.miliseconds)
        self.quitbutton=checktrue(self.quitbutton)
        self.x=int(self.x)
        self.y=int(self.y)

    def __str__(self):
        return "delaymode:{} mili:{} quitB:{} font:{} color:{} show:{} calldelay:{} delay:{} size:{} height:{} width:{} x,y={},{} tts={}".format(self.delaymode,
        self.miliseconds,self.miliseconds,self.font,self.color,self.show,self.calldelay,self.delay,self.size,self.height,self.width,self.x,self.y,self.ihateTTS)

class Timer():
    def __init__(self):
        self.first_time=time.time()

    def __call__(self):
        return time.time()-self.first_time

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
        if self.waitfor<time-self.config.delay: # Time to change the text for the next mechanic
            self.step+=1
            self.updateText(updateobject,time)
            if self.config.delaymode:
                self.waitfor+=self.getnext()[0]
            else:
                self.waitfor=self.getnext()[0]
            self.shotcall=0 # You can shotcall again
            if self.step>self.ln: #Stop the program
                print ("Timetable finished, shutting down")
                updateobject.destroy()
                sys.exit()

        elif self.waitfor<time+self.config.calldelay-self.config.delay: #Time to shotcall
            if self.shotcall==0:
                self.shotcall=1 # You can't shotcall anymore
                # Only shotcall the lines that exist
                text=self.getnext()[2]
                if text!="" and not self.config.ihateTTS:
                    print (" > [{}] Shotcalling {} at {}".format(self.step,text,time-self.config.delay))
                    speak.Speak(text)
        else:
            return None

    def updateText(self,updateobject,time):
        "Update the text with the next X mechanics" #Ending are weird, but I can't bother right now
        print (" > [{}] Showing next {} lines at {}".format(self.step,self.config.show,time-self.config.delay))
        lines=""
        for a,text,b in self.getnnext(self.config.show):
            lines=lines+text.replace(";","\n   ")+'\n'
        updateobject.changeText(lines)

    def getindex(self,index):
        try:
            return self.timetables[index]
        except:
            return [self.timetables[self.ln-1][0]+self.config.calldelay,"",""]

    def getnext(self):
        return self.getindex(self.step)

    def getnnext(self,nb):
        r=[]
        for i in range(nb):
            r.append(self.getindex(self.step+i))
        return r

#Utilities
def checkfile(f,config):
    'Check every line of the file for syntax errors and return the config, timetables'
    conf=f[0].split(";")
    timecheck=0
    table=[]
    try:
        config=load_conf(f[0].split(";"),config)
    except:
        print('Error while reading file config, using user config instead')

    for i in range(1,len(f)):
        try:
            time,show,say=split_line(f[i])
            if time<timecheck:
                print("Error on the timetables line {} time went from {} to {}".format(i+1,time,timecheck))
                raise AssertionError
            timecheck=time
            table.append([time,show,say])
        except:
            print("Error line {} : {}".format(i,f[i]))
            sys.exit()
    return config,Timetable(table,config)

def load_conf(table,config=Config()):
    "Load the confing in a line"
    if len(table)==1 and table[0]=="": # Let's not load empty configs
        return config
    for line in table:
        var,val=line.split('=')
        setattr(config,var,val)
    config.valtype()
    return config

def split_line(line):
    "Split lines according to the nominal format, return time as seconds"
    time,show,say=line.split("//")
    show,say=show.strip(" "),say.strip(" ")
    stime,time=time.split(":"),0
    for hms in stime:
        #Only powers of 60 so yeah; 1:12:33:11 will be incorrect, bite me
        time=time*60+int(hms)
    return time,show,say
# Init the thread for the TTS (can't have times calldelay by the wait)

# Load the Timetable
# First line should be config or empty
# Delay means delay mode instead of global time, miliseconds is miliseconds for time
# calldelay is the amount of time before the call (negative for late call (why ?))
# Every line Should look like Time (HH:MM:SS or SS) // Text to show // Text to say
try:
    print("Initialysing timer")
    gtimer=Timer()
    print("Opening Time Tables...")
    base_path=os.path.split(sys.argv[0])[0]
    data_path=os.path.join(base_path,sys.argv[1])
    main_config=os.path.join(base_path,"config.txt")
    with open(data_path) as f:
        time_data=f.read().splitlines()
    f.close()
    try:
        with open(main_config) as f:
            config_data=f.read().splitlines()
        f.close()
        base_config=load_conf(config_data)
    except:
        print("Could not load {}, using default config instead".format(main_config))
        base_config=Config()
    print("Cheking Time Data...")
    config,timetables=checkfile(time_data,base_config)
except:
    print("Error reading file {}".format(data_path))
    sys.exit()


class Application(tk.Frame):
    def __init__(self, master=None,gtimer=Timer(),config=None,shotcaller=None,timetables=None):
        self.timer=gtimer
        self.timetables=timetables
        self.gconfig=config
        if config.color=="white":
            self.bgcolor="black"
        else:
            self.bgcolor="white"
        tk.Frame.__init__(self, master)
        master.overrideredirect(True)
        master.geometry("+{}+{}".format(config.x,config.y))
        master.lift()
        master["bg"] = self.bgcolor
        master.wm_attributes("-topmost", True)
        try:
            master.wm_attributes("-disabled", not config.quitbutton)
        except:
            if not config.quitbutton:
                print("Warning: Impossible to disable window")
        try:
            master.wm_attributes("-transparentcolor", self.bgcolor)
        except:
            print("Warning: Impossible to make the background transparent")
        if config.quitbutton:
            B=tk.Button(master, bg=config.color,text="X",anchor='w',justify=tk.LEFT, command=master.destroy)
            B.grid(row=0,sticky='w')
        self.createWidgets()
        self.grid()

    def createWidgets(self):
        self.now = tk.StringVar()
        self.time = tk.Label(self,bg=self.bgcolor, height=config.height, justify=tk.LEFT,anchor='nw',width=config.width,bd=config.border,fg=config.color,font=(config.font, config.size))
        self.time.grid(row=1,sticky='w')
        self.time["textvariable"] = self.now
        self.timetables.updateText(self,self.timer())
        # initial time display
        self.onUpdate()

    def onUpdate(self):
        # update displayed time
        self.timetables(self.timer(),self)
        self.after(100, self.onUpdate)

    def changeText(self,newtext):
        self.now.set(newtext)

root = tk.Tk()
app = Application(master=root,gtimer=gtimer,config=config,shotcaller=None,timetables=timetables)
root.mainloop()
