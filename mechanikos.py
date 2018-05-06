import sys,os
import time

from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format

import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")

#Vague config class, will change asap
class Config():
    def __init__(self):
        self.delay=False
        self.miliseconds=False
        self.font="big"
        self.color="white"
        self.on_color=None
        self.show=1

#Utilities
def checkfile(f):
    'Check every line of the file for syntax errors'
    conf=f[0].split(";")
    try:
        config=load_conf(f[0])
    except:
        print('Error reading config')

    for i in range(1,len(f)):
        try:
            time,show,say=split_line(f[i])
        except:
            print("error line {} : {}".format(i,f[i]))

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
    return C

def split_line(line):
    "Split lines according to the nominal format, return time as seconds"
    time,show,say=line.split("//")
    stime,time,i=time.split(":"),0,0
    for hms in stime:
        #Only powers of 60 so yeah; 1:12:33:11 will be incorrect, bite me
        time=time+int(hms)*(60**i)
        i+=1
    return time,show,say
# Init the thread for the TTS (can't have times offset by the wait)

# Load the Timetable
# First line should be config or empty
# Delay means delay mode instead of global time, miliseconds is miliseconds for time
# offset is the amount of time before the call (negative for precall)
# Every line Should look like Time (HH:MM:SS or SS) // Text to show // Text to say
try:
    with open(sys.argv[1]) as f:
        time_data=f.read().splitlines()
    f.close()
    if len(sys.argv)==2:
        checkfile(time_data)
except:
    print "Error reading file"

import Tkinter
root = Tkinter.Tk()

root.overrideredirect(True)

root.geometry("+100+120")
root.lift()
root.wm_attributes("-topmost", True)
root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "white")
T = Tkinter.Text(root, height=2, width=30,bd=0,fg="red",font=("fixedsys", 22))
T.pack()
T.insert(Tkinter.END, "Just a text Widget\nin two lines\n")

root.mainloop()
print "2"
