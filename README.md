# Mechanikos

Dependencies:
* Python27+ (duh)
* tkinter
* pywin32 (via pip https://bootstrap.pypa.io/get-pip.py or easy_install)
* update ENV (check https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation)

Config:
''The first line of every project is a config containing some of the following info separated by semicolon, which overwrites personal configs. Leave empty unless needed.''
''Create a config file (config.txt) in the main directory, for your personal preferences as shown below. Every new argument must be separated with a line break.''
* delaymode=False     # Delay mode instead of absolute time mode
* calldelay=0         # A delay for announcing every mechanic
* delay=5             # Delay for calls calls, in seconds (use a negative value if they come by too late and vice versa)
* miliseconds=False   # Timetable format in ms instead of minutes:seconds
* quitbutton=False    # Add a quit button (the window is no longer disabled)
* ihateTTS=False      # Toggle callouts
* font=fixedsys       # Font to use for displayed
* color=red           # Font color
* border=0            # The border of the text, in px
* show=1              # Number of mechanics to show
* height=7            # Number of lines to show
* width=1000          # Width of the display
* size=32             # Size of the font
* x=220               # Position (x)
* y=220               # Position (y)
