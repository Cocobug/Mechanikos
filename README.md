# Mechanikos

Dependencies:
* Python27+ (duh)
* tkinter
* pywin32 (via pip https://bootstrap.pypa.io/get-pip.py or easy_install)
* update ENV (check https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation)

Config:
''The first line of every project is a config containing some of the following info separated by semicolon''
* delay=False         # Delay mode instead of absolute time mode
* miliseconds=False   # Timetable format in ms instead of minutes:seconds
* font=fixedsys       # Font to use for displayed
* color=red           # Font color
* border=0            # The border of the text, in px
* show=1              # Number of mechanics to show
* height=7            # Number of lines to show
* width=30            # Width of the display
* offset=5            # Offset for calls, in seconds
* size=32             # Size of the font
* x=220               # Position (x)
* y=220               # Position (y)
