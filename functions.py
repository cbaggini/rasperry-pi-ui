# Filename: functions.py

__version__ = '0.3'
__author__ = 'Alessio Deidda / Cecilia Baggini'

import subprocess

## App launcher functions ##############################
# Navit
def startNavit():
    app = '/usr/bin/navit'
    subprocess.Popen([app])
    
# dash camera, set mplayer to write a file in cycle
def dashCam():
    # -fs -> fullscreen
    # tv: -> source path
    subprocess.run(['mplayer', '-fs', 'tv:///dev/video0'])